from flask import Flask, jsonify, request, url_for, render_template, g 
from collections import namedtuple
import psycopg2 as driver
import requests
import argparse
import praw
import json
import urllib2
import datetime
import twitter
import unicodedata

app = Flask(__name__)

#creating twitter api object
c_k = 'UiAYyZK2QftHv4QFN82aUwXtc'
c_s = 'w9ExzHJCVZwEqtgty69vXZvrD3dxdPJyDNeIdqXY8mYPCHTggb'
a_t = '1360754605-h7DdBbXf0ddSUSCBtJ6mk1xLSy8GHrc8ng5RF2h'
a_s = 'xqvHvB0bul03IKdUmRhTLvQqlsT32KiHrP3p9vSoBYLrv'
api = twitter.Api(consumer_key=c_k, consumer_secret=c_s, access_token_key=a_t, access_token_secret=a_s)

#Bot objects
user_agent = 'web:server:v.1 (by /u/TVFlash)'
client_id = 'Nqf6SeqZFteU1A'
reddit = praw.Reddit(user_agent=user_agent, client_id=client_id, client_secret=client_secret)

#Database information
password = '' 

class userObject:
	def __init__(self):
		self.userID = ''
		self.token = ''
		self.twitchFeed = ''
		self.twitterFeed = ''
		self.redditFeed = []
		self.xkcdFeed = []
		self.githubFeed = ''
		self.hackerNewsFeed = ''
		self.fbStories = [] #IDs of stories showed
		self.activeFeeds = {}
		self.feedSource = {}
		#twitter objects
		self.friends = api.GetFriends(screen_name='trox94') # NEED TO CHANGE THIS TO SET IT TO INPUT FROM FRONTEND
		self.screens = []
		self.mostrecent = {}
		for x in self.friends:
			self.screens.append(x.screen_name)
		#twitch field
		self.recentstream = ''


class postObject:
	def __init__(self):
		self.id = ''
		self.source = ''
		self.message = ''
		self.time = ''
		self.link = ''
		self.picture = ''

	def to_json(self):
		return {"id": self.id, "source": self.source, "message": self.message, "time": self.time, "link": self.link, "picture": self.picture}

connected_users = {}

#====================================================================================
#MARK: API endpoints 
#====================================================================================

@app.route('/')
def renderLanding():
	return render_template("index.html")

def hasFeed(user, feed):
	if user.activeFeeds.contains(feed):
		return true
	return false

@app.route('/api/login/<int:userID>', methods=['POST'])
def login(userID):

	if not request.json:
			return jsonify({'err': 'Not JSON type'}), 201
	
	token = request.json['token']
	#Get user from database
	#If exists load assets
	user = has_user(userID)
	if user != False: 
		user.token = token #Update facebook token
	#Else create user account 
	else :
		print("Does not exist, creating account")
		add_user(userID)
		user = userObject()
		user.userID = userID
		user.token = token

	connected_users[userID] = user

	# #Pull latest FB data 
	send_refresh(userID)

	return jsonify({'result': 'login'}) #TODO : Add error checking and return payload

@app.route('/api/refresh/<int:userID>', methods=['POST'])
def send_refresh(userID):
	user = connected_users[userID] #Fetch requesting user
	user_pref_feeds = []
	if user.activeFeeds: 
		user_pref_feeds = sorted(user.activeFeeds.items(), key=user.activeFeeds.get, reverse=True)
	print user_pref_feeds
	update = []
	update = update_facebook(user, update)
	for feed in user_pref_feeds:
		feed = feed[0]
		if feed == 'reddit':
			update = update_reddit(user, update)
		elif feed == 'twitch':
			update = update_twitch(user, update) #TODO: write method
		elif feed == 'twitter':
			update = update_twitter(user, update)#TODO: write method
		elif feed == 'xkcd':
			update = update_xkcd(user, update)
		elif feed == 'github':
			update = update_github(user, update) #TODO: write method
		elif feed == 'hackernews':
			update = update_hackernews(user, update)#TODO: write method

	return json.dumps(update, ensure_ascii=False)

@app.route('/api/update/<int:userID>/<string:feedType>/<string:feedSource>', methods=['POST'])
def update_feed(userID, feedType, feedSource):
	con = get_db()
	cur = con.cursor()
	#Get current number of results
	query = 'SELECT array_dims(feeds) AS count FROM users WHERE user_id={}'.format(userID)
	cur.execute(query)
	con.commit()
	dim = cur.fetchone()
	item_count = 1

	if dim[0] is not None:
		item_count = int(dim[0].split(':')[1].split(']')[0]) + 1

	#Update feeds array to include new row
	query = """UPDATE users SET feeds[{}] = ROW('{}','{}',0)::feed WHERE user_id={}""".format(item_count, feedType, feedSource, userID)
	cur.execute(query)
	con.commit()
	#Refresh?
	return jsonify({'result': 'success'}) #TODO: Add / Change attributes to a feed

@app.route('/api/interaction/<int:userID>/<string:feedType>/<string:feedSource>', methods=['POST'])
def add_interaction(userID, feedType, feedSource):
	idx = 1
	con = get_db()
	cur = con.cursor()
	query = 'SELECT feeds FROM users WHERE user_id={}'.format(userID)
	cur.execute(query)
	con.commit()
	feeds = cur.fetchone()[0]
	feeds = feeds[3:len(feeds) - 3].replace("\"","").split("),(") #Trim leading and trailing braces

	for feed in feeds:
		attributes = feed.split(",")
		if attributes[0] == feedType and attributes[1] == feedSource:
			query = """UPDATE users SET feeds[{}] = ROW('{}','{}',{})::feed WHERE user_id={}""".format(idx, feedType, feedSource, int(attributes[2]) + 1,userID)
			cur.execute(query)
			con.commit()
		else: 
			idx = idx + 1

	return jsonify({'result': 'success'}) #TODO: Update the user's interaction count with a feed

#====================================================================================
#MARK: Helper functions
#====================================================================================

def has_user(userID):
	con = get_db()
	cur = con.cursor()
	query = 'SELECT * FROM users WHERE user_id={}'.format(userID)
	cur.execute(query)
	con.commit()

	if cur.rowcount == 0:
		return False
	user = userObject()
	user.userID = userID
	feeds = cur.fetchone()[1]
	if feeds:
		feeds = feeds[3:len(feeds) - 3].replace("\"","").split("),(") #Trim leading and trailing braces
		for feed in feeds:
			attributes = feed.split(",")
			feed_type = attributes[0]
			feed_source = attributes[1]
			interact_count = attributes[2]
			#Add feed sources to a list
			if feed_type not in user.feedSource:
				user.feedSource[feed_type] = []
			
			user.feedSource[feed_type].append(feed_source)
			#keep track of interaction count per feed
			if feed_type in user.activeFeeds:
				user.activeFeeds[feed_type] = user.activeFeeds[feed_type] + int(interact_count)
			else:
				user.activeFeeds[feed_type] = int(interact_count)
	return user

def add_user(userID):
	con = get_db()
	cur = con.cursor()
	query = 'INSERT INTO users (user_id) VALUES ({})'.format(userID)
	cur.execute(query)
	con.commit()

def send_feed(userID, feedType):
	return False #TODO: Check diff for specified feed 

def update_facebook(user, update):
	fb_content = requests.get('https://graph.facebook.com/v2.3/me/feed?access_token=' + user.token).content
	raw_json = json.loads(fb_content)
	for obj in raw_json[u'data']:
		if obj['id'] not in user.fbStories:
			post = postObject()
			post.id = obj['id']
			post.source = 'facebook'
			if 'message' in obj:
				post.message = obj['message']
			else:
				post.message = obj['story']
			post.time = obj['created_time']
			post.link = 'https://www.facebook.com/{}/posts/{}?pnref=story'.format(post.id.split('_')[0], post.id.split('_')[1])
			if 'picture' in obj:
				post.picture = obj['picture']
			update.append(post.to_json())
			user.fbStories.append(post.id)
	return update

def update_reddit(user, update):
	for subreddit in user.feedSource['reddit']:
		for submission in reddit.subreddit(subreddit).hot(limit=5):
			if submission.id not in user.redditFeed:
				post = postObject()
				post.id = submission.id
				post.source = 'reddit'
				post.message = submission.title
				post.link = 'http://reddit.com{}'.format(submission.permalink)
				post.picture = submission.url
				post.time = submission.created_utc	
				update.append(post.to_json())
				user.redditFeed.append(post.id)
	return update

def update_github(user, update):
	print("github")
	return update

def update_twitch(user, update):
	ret = []  # list of twitch streams to return that went live since last update
	tempurl = 'https://api.twitch.tv/kraken/users/trox94/follows/channels?response_type=token&limit=140&client_id=1pmqc0kf9rr5p3ku7s6ps6qezpav5d6&sortby=last_broadcast'
	#NEED TO CHANGE THIS API CALL TO USE USERNAME FROM FRONTEND
	contents = urllib2.urlopen(tempurl)
	con = contents.read()
	obj = json.loads(con)
	#gets the list of following objects, sorted by last broadcast time

	for i in range (0, 140):
		st = obj['follows'][i]['channel']['display_name']
		if user.mostrecent == '': # only happens on first call to update
			user.mostrecent = st
			ret.append(st)
			break
		if user.mostrecent == st: # found the most recent stream object from last update
			break
		else:
			ret.append(st)  #stream that came online since last call to update
			pass
	print("twitch")
	#want to return ret here
	return update

def update_twitter(user, update):
	ret = {} #ret is a hashmap, key = twitter username, value = text of tweet
	for name in user.screens: #iterate over people you follow
		statuses = api.GetUserTimeline(screen_name=name) #list of status objects for 'name'
		message = unicodedata.normalize('NFKD', statuses[0].text).encode('ascii','ignore') #gets rid of weird characters
		if name in user.mostrecent:
			if message != user.mostrecent[name]:
				user.mostrecent[name] = message #saves the most recent tweet from user 'name'
				ret[name] = message # add the tweet to the response hash map
		else:
			user.mostrecent[name] = message #only happens on first update, just save most recent tweet

	post = postObject()
	#want to return ret here

	return update

def update_hackernews(user, update):
	print("hackernews")
	return update

def update_xkcd(user, update):
	page = urllib2.urlopen('http://xkcd.com/info.0.json')
	cont = page.read()
	obj = json.loads(cont)
	post = postObject()
	post.picture = obj['img']
	post.source = 'xkcd' 
	post.id = obj['num'] ### THIS NEEDS TO BE CHANGED
	post.link = "http://xkcd.com"
	post.time = str(datetime.datetime.now())
	update.append(post.to_json())
	user.xkcdFeed.append(post.id)
	return update

@app.before_first_request
def establish_db_connection():
	g.db = driver.connect(database='postgres', user='postgres', host='localhost', password=password)

def get_db():
	if not hasattr(g, 'db'):
		print("Connecting to DB...")
		establish_db_connection()
	return g.db

def print_post(post):
	print(post.id)
	print(post.source)
	print(post.message)
	print(post.time)
	print(post.link)
	print(post.picture)

#TODO: Stringify function for posts in JSON format

#====================================================================================
#MARK: Main
#====================================================================================

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-p', type=str, required=True, help="usage: -p [password]")
	args = parser.parse_args()
	password = args.p
	app.run(host='0.0.0.0',port=2000,debug=True)

