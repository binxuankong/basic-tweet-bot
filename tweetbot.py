import time
import tweepy
from credentials import *
from apscheduler.schedulers.blocking import BlockingScheduler

# Access and authorize Twitter credentials
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# The tweet text
tweet_text = "Replace this text with something you want to tweet"

# Hashtag to retweet or favourite
hashtag_retweet = "tweetbot"
hashtag_favourite = "tweetbot"
# Number of tweets to retweet or favourite
limit_retweet = 10
limit_favourite = 10

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

# Create a scheduler to schedule the activities
scheduler = BlockingScheduler()
scheduler.add_job(tweet, 'interval', hours=6) # Tweets every 6 hours
scheduler.add_job(retweet, 'interval', hours=2) # Retweet every 2 hours
scheduler.add_job(favourite, 'interval', minutes=45) # Favourite every 45 minutes
# Start the scheduler
scheduler.start()