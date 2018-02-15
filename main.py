#!/usr/bin/python
import time
import tweepy
import slacker
import json
import sqlite3
import requests

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

# twitter auth
consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# slack auth
slack_webhook_url = os.environ.get('SLACK_WEBHOOK_URL')jj

# db
conn = sqlite3.connect('twitter.db')
conn.text_factory = str
c = conn.cursor()

def get_all_tweets(screen_name):
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	try: 
		new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	except Exception as ex:
		new_tweets = ""
		print ex	

	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1

	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print "getting tweets after %s" % (oldest)
		
		#all subsiquent requests use the max_id param to prevent duplicates
		try:
			new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		except Exception as ex:
			new_tweets = ""
			print ex	

		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1

		#check if oldest is in db
		old_num = alltweets[-1].id
		query = 'SELECT * FROM tweets WHERE id = "%s" LIMIT 1' % old_num
		c.execute(query)
		result = c.fetchone()
		if result:
			# break out of looping more tweets
			print "+++++++++++found existing tweets++++++++++++"
			break
		
		print "...%s tweets processed so far" % (len(alltweets))

	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, screen_name, tweet.text.encode("utf-8")] for tweet in alltweets]

	insert_count = 0

	for tweet in outtweets:
		# print tweet[0]
		query = 'SELECT * FROM tweets WHERE id = "%s" LIMIT 1' % tweet[0]
		c.execute(query)
		result = c.fetchone()
		if result:
			pass
			# print "not inserting %s" % tweet[0]
		else:
			#print "inserting %s" % tweet[0]
			insert_count = insert_count + 1
			c.execute('INSERT INTO tweets VALUES (?,?,?,?)', tweet)
			result = c.fetchone()
			conn.commit()

	print "inserted %s records" % insert_count


	return
	

if __name__ == '__main__':
	# if just starting up, yank all the notifications and then mark them as read
	get_all_tweets('lucidworks')

	# periodically post new 
	while True:
		# post to slack
		headers = {'content-type': 'application/json'}
		r = requests.post(slack_webhook_url, data={'text': "posting to slack"}, headers=headers)
		time.sleep(300) # sleep 5 minutes