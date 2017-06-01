import praw
import pickle
import time
import csv
from datetime import datetime

reddit = praw.Reddit(client_id='client_id',
                     client_secret='client_secret',
                     user_agent='RPMBP:com.rudypikulik.RedditUpvoteData:v1.1.2',
                     username='xxxxxxxx',
                     password='xxxxxxxx')

try:
    data = pickle.load(open('data_copy.p', 'rb'))
except:
    data = []
try:
    posts = pickle.load(open('posts.p', 'rb'))
except:
    posts = []

sub = reddit.subreddit("all")

# Initializes csv file.
csv_file = open('csv_data_%s-%s_(%s).csv' % (time.localtime()[1], time.localtime()[2], time.localtime()[3]), 'w')
csv_out = csv.writer(csv_file)
csv_out.writerow(['ID', 'HOUR', 'MINUTE', 'SCORE'])

def save_to_csv(post):
    # Data to save: (ID, HOUR, MINUTE, SCORE)
    # Saved both to csv file and data (list).
    submission = praw.models.Submission(reddit, post[0])
    data_tup = (post[0], post[2], post[3], submission.score)
    csv_out.writerow(data_tup)
    data.append(data_tup)
    pickle.dump(data, open('data_copy.p', 'wb'))


def time_value(DAY, HOUR):
    return DAY*24+HOUR

def evaluate_post(post):
    # If it has been at least 12 hours since the post was logged,
    # save its information and remove it from posts.
    day = time.localtime()[2]
    hour = time.localtime()[3]
    if time_value(day, hour) > (time_value(post[1], post[2])+12):
        save_to_csv(post)
        posts.remove(post)


def register_post(post):
    # Appends tuple of (ID, DAY, HOUR, MINUTE) to posts.

    # Checks if the post is already in posts
    ids = map(lambda x: x[0], posts)
    if post.id not in ids:
        posts.append((post.id, time.localtime()[2], time.localtime()[3], time.localtime()[4]))
        pickle.dump(posts, open('posts.p', 'wb'))


def start_stream():
    # Starts the post stream, called in the while loop below.
    post_stream = sub.stream.submissions()
    for post in post_stream:
        if time.localtime()[4]%5 == 0 and time.localtime()[5] == 0:
            print('> %s - There are %s posts queued and %s posts saved.' % (datetime.now(), str(len(posts)), str(len(data))))
        register_post(post)
        evaluate_post(posts[0])


while True:
    try:
        print("Starting stream at %s" % (datetime.now()))
        start_stream()
    except Exception as e:
        print("> %s - Connection lost. Restarting in 5s... %s" % (datetime.now(), e))
        posts.remove(posts[0])
        time.sleep(5)
        continue
