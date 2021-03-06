from flask import Flask, jsonify, request, url_for, render_template, g 
from collections import namedtuple
from random import shuffle
import psycopg2 as driver
import requests
import argparse
import operator
import praw
import json
import urllib2
import datetime
import twitter
import unicodedata
from hackernews import HackerNews


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
client_secret = ''
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
		self.githubFeed = []
		self.hackerNewsFeed = []
		self.fbStories = [] #IDs of stories showed
		self.activeFeeds = {}
		self.feedSource = {}
		#twitter objects
		self.friends = ''
		self.screens = []
		self.mostrecent = {}
		#twitch field
		self.twitchuser = ''


class postObject:
	def __init__(self):
		self.id = ''
		self.type = ''
		self.source = ''
		self.message = ''
		self.time = ''
		self.link = ''
		self.picture = ''
		self.mainlabel = ''
		self.sublabel = ''

	def to_json(self):
		return {"id": self.id, "type": self.type, "source": self.source, "message": self.message, "time": self.time, "link": self.link, "picture": self.picture, "mainlabel": self.mainlabel, "sublabel": self.sublabel}

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
	if user.userID == 1379847898693831:
		return jsonify({'picture': 'https://scontent.xx.fbcdn.net/v/t1.0-1/p50x50/602182_1206447199367236_4235417433582915679_n.jpg?oh=4c8f464417f0373efa0221dc9da4e5c9&oe=58BE0C7A'})
	if user.userID == 1517929204900960:
		return jsonify({'picture': 'https://scontent.xx.fbcdn.net/v/t1.0-1/p50x50/14022262_1443956868964861_2652181416555563517_n.jpg?oh=1d6bc3e443654a2f0e5efb78b32cc2af&oe=58EC3A00'}) 
	if user.userID == 1423056431053053:
			return jsonify({'picture': 'https://scontent.xx.fbcdn.net/v/t1.0-1/p50x50/942280_1214650845226947_7957939453920290600_n.jpg?oh=0652f2bec4acace0b5570787d77313f1&oe=58EF1C0A'})
	return jsonify({'picture': 'None'}) 

@app.route('/api/refresh/<int:userID>', methods=['POST'])
def send_refresh(userID):
	user = connected_users[userID] #Fetch requesting user
	user_pref_feeds = []
	if user.activeFeeds: 
		user_pref_feeds = sorted(user.activeFeeds.items(), key=operator.itemgetter(1), reverse=True)
	strata_line = len(user_pref_feeds)/ 2  if user.activeFeeds is not None else 0
	strata_idx = 0
	print strata_line
	upper_strata = []
	lower_strata = []
	update = []
	update = update_facebook(user, update)
	for feed in user_pref_feeds:
		strata_idx = strata_idx + 1
		feed = feed[0] #Drop count from tuple
		if feed == 'reddit':
			update = update_reddit(user, update)
		elif feed == 'twitch':
			update = update_twitch(user, update)
		elif feed == 'twitter':
			update = update_twitter(user, update)
		elif feed == 'xkcd':
			update = update_xkcd(user, update)
		elif feed == 'github':
			update = update_github(user, update)
		elif feed == 'hackernews':
			update = update_hackernews(user, update)
		if strata_idx == strata_line:
			shuffle(update)
			upper_strata = update
			update = []
	
	if strata_line > 0:
		shuffle(update)
		lower_strata = update
		upper_strata.extend(lower_strata)

	else:
		upper_strata = update	

	return json.dumps(upper_strata, ensure_ascii=False)

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
	#Refresh
	user = connected_users[userID]
	if feedType not in user.feedSource:
		user.feedSource[feedType] = []

	user.feedSource[feedType].append(feedSource)
	user.activeFeeds[feedType] = 0
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

	user = connected_users[userID]
	user.activeFeeds[feedType] = user.activeFeeds[feedType] + 1
	return jsonify({'result': 'success'}) #TODO: Update the user's interaction count with a feed

@app.route('/api/feeds/<int:userID>', methods=['POST'])
def get_feeds(userID):
	user = connected_users[userID]
	return json.dumps(user.feedSource) 

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

			if feed_type == 'twitter':
				user.friends = api.GetFriends(screen_name=feed_source)
				for x in user.friends:
					user.screens.append(x.screen_name)
			if feed_type == 'twitch':
				user.twitchuser = feed_source
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
			post.type = 'facebook'
			post.mainlabel = 'Facebook'
			post.sublabel = 'You posted:'
			if 'message' in obj:
				post.message = obj['message']
			else:
				post.message = obj['story']
			post.time = obj['created_time']
			post.time = post.time[:len(post.time) - 5]
			post.link = 'https://www.facebook.com/{}/posts/{}?pnref=story'.format(post.id.split('_')[0], post.id.split('_')[1])
			if 'picture' in obj:
				post.picture = obj['picture']
			update.append(post.to_json())
			user.fbStories.append(post.id)
	return update

def update_reddit(user, update):
	for subreddit in user.feedSource['reddit']:
		for submission in reddit.subreddit(subreddit).hot(limit=15):
			if submission.id not in user.redditFeed:
				post = postObject()
				post.id = submission.id
				post.type = 'reddit'
				post.source =  subreddit
				post.mainlabel = submission.title
				post.sublabel = 'Points ' + str(submission.score )
				post.message = submission.selftext if submission.selftext != '' else "Read more"
				post.link = 'http://reddit.com{}'.format(submission.permalink)
				post.picture = submission.thumbnail
				post.time = submission.created_utc	
				update.append(post.to_json())
				user.redditFeed.append(post.id)
	return update

def update_github(user, update):
	cid = 'd82b3dc16fd177dc3f7d'
	sec = '71e8e9247baf1a485e4cf3bcd3d5ff7088ecce4e'

	for username in user.feedSource['github']:
		url = 'https://api.github.com/users/{}/received_events/public?client_id={}&client_secret={}'.format(username, cid, sec)
		gh_content = requests.get(url).content
		raw_json = json.loads(gh_content)
		for obj in raw_json:
			if obj['id'] not in user.githubFeed:
				post = postObject()
				post.id = obj['id']
				post.type = 'github'
				post.source = username

				action = ''
				action_type = obj['type']
				if action_type == 'WatchEvent':
					action = ' watched'
				elif action_type == 'ForkEvent':
					action = ' forked'
				elif action_type == 'PushEvent':
					action = ' pushed to'
				else:
					print obj
				post.mainlabel = 'GitHub'
				post.sublabel = obj['actor']['display_login'] + action + ' ' + obj['repo']['name']
				post.message = 'Read me'
				post.time = obj['created_at']
				post.picture = obj['actor']['avatar_url']
				update.append(post.to_json())
				user.githubFeed.append(post.id)
		return update

def update_twitch(user, update):
	if user.twitchuser == '':
		return update #twitch user uninitialized in user, back out
	tempurl = 'https://api.twitch.tv/kraken/users/' + user.twitchuser +  '/follows/channels?response_type=token&limit=140&client_id=1pmqc0kf9rr5p3ku7s6ps6qezpav5d6&sortby=last_broadcast'
	#NEED TO CHANGE THIS API CALL TO USE USERNAME FROM FRONTEND
	contents = urllib2.urlopen(tempurl)
	con = contents.read()
	obj = json.loads(con)
	followed = []
	#followed is a list of potential online streams, starts with all following initially, then only checks up till most recently checked

	for i in range (0, 140):
		st = obj['follows'][i]['channel']['display_name']
		if user.mostrecent == st: # found the most recent stream object from last update
			break
		else:
			followed.append(st)
			pass
	
	user.mostrecent = obj['follows'][0]['channel']['display_name'] # stores most recent stream to go online
	if len(followed) == 0: #no new streams since last check
		return update

	offlinecount = 0
	for stream in followed:
		try:
			url = 'https://api.twitch.tv/kraken/streams/' + stream + '?response_type=token&client_id=1pmqc0kf9rr5p3ku7s6ps6qezpav5d6'
			contents = urllib2.urlopen(url)
			con = contents.read()
			obj = json.loads(con)
			if obj['stream'] is not None:
				post = postObject()	
				post.type = 'twitch'
				post.source = stream
				post.message = '<a href=\"http://www.twitch.tv/' + st + '\"> just went live!'
				update.append(post.to_json())
				offlinecount = 0 #reset the counter
			else:
				offlinecount += 1	
				if offlinecount >= 7: #encountered 7 consecutive offline streams before finding an online one
					break
		except:
			pass
		
#	print("twitch")
	return update

def update_twitter(user, update):
	ret = '' #ret is a hashmap, key = twitter username, value = text of tweet
	for name in user.screens: #iterate over people you follow
		try:
			statuses = api.GetUserTimeline(screen_name=name) #list of status objects for 'name'
			message = unicodedata.normalize('NFKD', statuses[0].text).encode('ascii','ignore') #gets rid of weird characters
			if name in user.mostrecent:
				if message != user.mostrecent[name]:
					user.mostrecent[name] = message #saves the most recent tweet from user 'name'
					finalmess = name + ' tweeted ' + message + '\n'
					post = postObject()
					post.mainlabel = 'Twitter'
					post.sublabel = '@{}'.format(name)
					post.type = 'twitter'
					post.source = user.feedSource[post.type]
					post.message = finalmess
					update.append(post.to_json())
			else:
				user.mostrecent[name] = message #only happens on first update, just save most recent tweet
		except:
			pass
	return update

def update_hackernews(user, update):
	hn = HackerNews()

	for story_id in hn.top_stories(limit=15):
		post = postObject()
		hn_story = hn.get_item(story_id)
		message = hn_story.text

		post.mainlabel = hn_story.title.encode('ascii', 'ignore')
		post.time = str(hn_story.submission_time)
		post.sublabel = str(hn_story.score) + " points by " + hn_story.by
		post.message = message if message is not None else  "Read more"
		post.type = 'hackernews'
		post.link = "https://news.ycombinator.com/"
		if post.mainlabel not in user.hackerNewsFeed:
			update.append(post.to_json())
			user.hackerNewsFeed.append(post.mainlabel)
	return update

def update_xkcd(user, update):
	page = urllib2.urlopen('http://xkcd.com/info.0.json')
	cont = page.read()
	obj = json.loads(cont)
	post = postObject()
	post.mainlabel = 'XKCD'
	post.picture = obj['img']
	post.type = 'xkcd' 
	post.id = obj['num'] ### THIS NEEDS TO BE CHANGED
	post.link = "http://xkcd.com"
	post.time = str(datetime.datetime.now())
	if post.id not in user.xkcdFeed:
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

