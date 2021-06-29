import os
import time

import praw
import schedule
from dotenv import load_dotenv


SCHEDULE_TIME = 60
REDDIT_NAME = ''


def job():
    print('Job running')
    try:
        CLIENT_ID = os.getenv('CLIENT_ID')
        CLIENT_SECRET = os.getenv('CLIENT_SECRET')
        USERNAME = os.getenv('REDDIT_USERNAME')
        PASSWORD = os.getenv('REDDIT_PWD')

        reddit = praw.Reddit(
            user_agent='Activity Bot',
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            username=USERNAME,
            password=PASSWORD,
        )

        check_mentions(reddit)
    except Exception as ex:
        print('Error in job:', str(ex))


def check_mentions(reddit):
    for msg in reddit.inbox.unread(limit=25):
        if valid_msg(msg.body):
            response = parse_msg(reddit, msg.body)
            msg.reply(response)
            msg.mark_read()


def valid_msg(body):
    if not (body.startswith('u/post-history-bot') or body.startswith('/u/post-history-bot')):
        return False

    words = body.split(' ')

    if len(words) != 3:
        return False

    return True


def parse_msg(reddit, body):
    words = body.strip().split(' ')
    user = words[1].replace('\\', '').lower()
    community = words[2].lower()

    post_count = 0
    comment_count = 0

    if not community.startswith('r/'):
        community = f'r/{community}'

    for submission in reddit.redditor(user).submissions.new(limit=None):
        if community in f'r/{submission.subreddit.display_name}'.lower():
            post_count += 1

    for comment in reddit.redditor(user).comments.new(limit=None):
        if community in f'r/{comment.subreddit.display_name}'.lower():
            comment_count += 1

    return f'{user} has {post_count} post(s) and {comment_count} comment(s) in {community}'


if __name__ == '__main__':
    load_dotenv()
    schedule.every(SCHEDULE_TIME).seconds.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
