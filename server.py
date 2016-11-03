from flask import Flask, jsonify, request, url_for, render_template, g 
from collections import namedtuple
import psycopg2 as driver
import requests
import argparse
import json

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
		self.xkcdFeed = ''
		self.githubFeed = ''
		self.hackerNewsFeed = ''
		self.fbStories = [] #IDs of stories showed 
		self.activeFeeds = []

class postObject:
	def __init__(self):
		self.id = ''
		self.source = ''
		self.message = ''
		self.time = ''
		self.link = ''
		self.picture = ''

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
	update_facebook(userID)

	return jsonify({'result': 'login'}) #TODO : Add error checking and return payload

@app.route('/api/refresh/<int:userID>', methods=['POST'])
def send_refresh(userID):
	user = connected_users[userID] #Fetch requesting user
	#make GET request to FB API
	#if any diff then return it
	#else return nothing
	return False #TODO: Return any diff in the user's feeds

@app.route('/api/update/<int:userID>/<string:feedType>', methods=['POST'])
def update_feed(userID, feedType):
	return False #TODO: Add / Change attributes to a feed

@app.route('/api/interaction/<int:userID>/<string:feedType>', methods=['POST'])
def add_interaction(userID, feedType):
	return False #TODO: Update the user's interaction count with a feed

#====================================================================================
#MARK: Helper functions
#====================================================================================

def has_user(userID):
	con = get_db()
	cur = con.cursor()
	query = 'SELECT * FROM users where user_id={}'.format(userID)

	cur.execute(query)

	con.commit()

	if cur.rowcount == 0:
		return False #TODO: Check from database
	user = userObject()
	user.userID = userID
	return user

def add_user(userID):
	con = get_db()
	cur = con.cursor()
	query = 'INSERT INTO users (user_id) VALUES ({})'.format(userID)
	cur.execute(query)
	con.commit()

def send_feed(userID, feedType):
	return False #TODO: Check diff for specified feed 

def update_facebook(userID):
	user = connected_users[userID]
	fb_content = requests.get('https://graph.facebook.com/v2.3/me/feed?access_token=' + user.token).content
	parsed_json = []
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
			print(post.link)
			parsed_json.append(post)
			user.fbStories.append(post.id)
	return parsed_json

def update_reddit(userID):
	user = connected_users[userID]

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

#====================================================================================
#MARK: Main
#====================================================================================

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-p', type=str, required=True, help="usage: -p [password]")
	args = parser.parse_args()
	password = args.p
	app.run(host='0.0.0.0',port=2000,debug=True)

