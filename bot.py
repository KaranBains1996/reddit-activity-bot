import os

from dotenv import load_dotenv
import praw

CLIENT_ID = ''
CLIENT_SECRET = ''
USERNAME = ''
PASSWORD = ''


def main():
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


def check_mentions(reddit):
    for msg in reddit.inbox.unread(limit=25):
        if valid_msg(msg.body):
            response = parse_msg(reddit, msg.body)
            msg.reply(response)
            # msg.mark_read()


def valid_msg(body):
    if not body.startswith('u/reddit-activity-bot'):
        return False

    words = body.split(' ')

    if len(words) != 3:
        return False

    print(words)

    return True


def parse_msg(reddit, body):
    words = body.split(' ')
    user = words[1]
    community = words[2]

    post_count = 0
    comment_count = 0

    for submission in reddit.redditor(user).submissions.new(limit=None):
        if community in "r/"+submission.subreddit.display_name:
            post_count += 1

    for comment in reddit.redditor(user).comments.new(limit=None):
        if community in "r/"+comment.subreddit.display_name:
            comment_count += 1

    return '{} has {} post(s) and {} comment(s) in {}'.format(user, post_count, comment_count, community)


if __name__ == '__main__':
    load_dotenv()
    main()
