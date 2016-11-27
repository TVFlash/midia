from flask import Flask, jsonify, request, url_for, render_template, g 
from collections import namedtuple
import psycopg2 as driver
import requests
import argparse
import json
import urllib2
import datetime

app = Flask(__name__)

#Database information
password = '' 

class userObject:
	def __init__(self):
		self.userID = ''
		self.token = ''
		self.twitchFeed = ''
		self.twitterFeed = ''
		self.redditFeed = ''
		self.xkcdFeed = []
		self.githubFeed = ''
		self.hackerNewsFeed = ''
		self.fbStories = [] #IDs of stories showed
		self.activeFeeds = {}

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

	return json.dumps(update) #TODO: add the diffs in other feeds

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
			if attributes[0] in user.activeFeeds:
				user.activeFeeds[attributes[0]] = user.activeFeeds[attributes[0]] + int(attributes[2])
			else:
				user.activeFeeds[attributes[0]] = int(attributes[2])

		#TODO: load other fields from db
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
	print("reddit")
	return update

def update_github(user, update):
	print("github")
	return update

def update_twitch(user, update):
	print("twitch")
	return update

def update_twitter(user, update):
	print("twitter")
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

