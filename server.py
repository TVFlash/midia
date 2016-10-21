from flask import Flask, jsonify, request, url_for, render_template 

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

connected_users = []

#====================================================================================
#MARK: API endpoints
#====================================================================================

@app.route('/')
def renderLanding():
	return render_template("fblanding.html") #Waiting for frontent stuff

def hasFeed(user, feed):
	if user.activeFeeds.contains(feed):
		return true
	return false

@app.route('/api/login/<int:userID>', methods=['POST'])
def login(userID):
	#Get user from database
	print("Got user: " , userID)
	#If exists load assets
	if has_user(userID): 
		print(userID)
	#Else create user account 
	else :
		print("Does not exist, creating account")
	return jsonify({'result': 'login'}) #TODO : Add error checking and return payload

@app.route('/api/refresh/<int:userID>', methods=['POST'])
def send_refresh(userID):
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
	return False #TODO: Check from database

def add_user(userID):
	return False #TODO: Add user to database

def send_feed(userID, feedType):
	return False #TODO: Check diff for specified feed 

#====================================================================================
#MARK: Main
#====================================================================================

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=2000,debug=True)

