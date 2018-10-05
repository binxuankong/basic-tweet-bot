import time
import tweepy
from credentials import *
from apscheduler.schedulers.blocking import BlockingScheduler

# Access and authorize Twitter credentials
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Text file containing the mention tweet ids history so that the program will not
# reply to any mentions repeatedly when the program is rebooted
tweet_history_file = open('tweet_history.txt', 'r+')
tweet_history = tweet_history_file.readlines()

# Add the previous mentioned tweets into a list
responded_tweets = []
for tw in tweet_history:
    responded_tweets.append(int(tw))

# The tweet text
tweet_text = "Replace this text with something you want to tweet"

# Hashtag to retweet, favourite or follow
hashtag_retweet = "tweetbot"
hashtag_favourite = "tweetbot"
hashtag_follow = "tweetbot"
# Number of tweets to retweet, favourite or follow
limit_retweet = 10
limit_favourite = 10
limit_follow = 10

# Regular tweet
def tweet():
    api.update_status(tweet_text)
    print('Tweeted: ' + this_tweet)

# Tweet with mention
def tweet(username):
    api.update_status(tweet_text, status='@{0}'.format(username))
    print('Tweeted: @' + username + ' ' + tweet_text)

# Retweet tweets with certain hashtag
def retweet():
    target = '#' + hashtag_retweet
    # Change the value of hashtag_limit to determine number of tweets to retweet
    for tw in tweepy.Cursor(api.search, q=target).items(limit_retweet):
        try:
            print('Tweet by @' + tw.user.screen_name + ' ' + tw.text)
            tw.retweet()
            print('Retweeted')
            # Wait for a moment after retweeting before proceeding
            time.sleep(5)
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break

# Favourite tweets with certain hashtag
def favourite():
    target = '#' + hashtag_favourite
    # Change the value of hashtag_limit to determine number of tweets to retweet
    for tw in tweepy.Cursor(api.search, q=target).items(limit_favourite):
        try:
            print('Tweet by @' + tw.user.screen_name + ' ' + tw.text)
            tw.favorite()
            print('Favourited')
            # Wait for a moment after favouriting before proceeding
            time.sleep(5)
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break

# Follow users who tweets with certain hashtag
def follow():
    target = '#' + hashtag_follow
    # Change the value of hashtag_limit to determine number of tweets to retweet
    for tw in tweepy.Cursor(api.search, q=target).items(limit_follow):
        try:
            print('Tweet by @' + tw.user.screen_name + ' ' + tw.text)
            # Only follow if already not following the user
            if not tw.user.following:
                tw.user.follow()
                print('Followed')
            # Wait for a moment after retweeting before proceeding
            time.sleep(5)
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break

# Reply to a mention
def reply(username, mention_id):
    api.update_status(tweet_text, status='@{0}'.format(username), in_reply_to_status_id=status_id)
    print('Tweeted: @' + username + ' ' + tweet_text)

# Reply to all mentions
def reply_all():
    for mention in api.mentions_timeline():
        if mention.id not in responded_tweets:
            print('Found mention - {}'.format(mention.text))
            try:
                reply(mention.user.screen_name, mention.id)
                # Wait for a moment after tweeting before proceeding
                time.sleep(5)
            except tweepy.TweepError as e:
                print(e.reason)
            # Add the mention id into the list to prevent repeated replies
            responded_tweets.append(mention.id)
            mention_id = str(mention.id) + "\n"
            tweet_history_file.write(mention_id)

# Follow back
def follow_back():
    friends = api.friends_ids(api.me().id)
    for follower in tweepy.Cursor(api.followers).items():
        if follower.id != api.me().id:
            if follower.id not in friends:
                try:
                    follower.follow()
                    print('Followed: @' + follower.screen_name)
                except tweepy.TweepError:
                    print('Already tried to follow back @' + follower.screen_name)

# Create a scheduler to schedule the activities
scheduler = BlockingScheduler()
scheduler.add_job(tweet, 'interval', hours=6) # Tweet every 6 hours
scheduler.add_job(retweet, 'interval', hours=4) # Retweet every 4 hours
scheduler.add_job(favourite, 'interval', hours=2) # Favourite every 2 hours
scheduler.add_job(follow, 'interval', days=1) # Follow every day
scheduler.add_job(reply_all, 'interval', minutes=30) # Reply back every 30 minutes
scheduler.add_job(follow_back, 'interval', minutes=10) # Follow back every 10 minutes
# Start the scheduler
scheduler.start()