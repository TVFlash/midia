from flask import Flask, jsonify

app = Flask(__name__)

class userObject:
	def __init__(self):
		self.userID = ''
		self.twitchFeed = ''
		self.twitterFeed = ''
		self.redditFeed = ''
		self.xkcdFeed = ''
		self.githubFeed = ''
		self.hackerNewsFeed = ''
		self.activeFeeds = []

@app.route('/')
def renderLanding:
	return "Welcome" #Waiting for frontent stuff

def hasFeed(user, feed):
	if user.activeFeeds.contains(feed):
		return true
	return false

