# WarmheartedSubstantialBrackets
from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
from random import randint
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

def is_int(s):
  try: 
      int(s)
      return True
  except ValueError:
      return False

def random_post_id():
	temprandom = randint(100000000000000, 999999999999999)
	conn = sqlite3.connect('db.sql')
	c = conn.cursor()
	posts = c.execute("SELECT id FROM posts").fetchall()
	# print(str(posts))
	conn.commit()
	conn.close()
	if len(posts) == 0:
		return str(temprandom)
	for post in posts:
		if temprandom == post[0]:
			random_post_id()
		else:
			# print(str(temprandom))
			return str(temprandom)

def random_pfp_id():
	temprandom = randint(1, 10)
	return str(temprandom)

def check_if_logged_in():
	if session.get('logged_in'):
		# print(session.get("username"))
		conn = sqlite3.connect('db.sql')
		c = conn.cursor()
		pwhash = c.execute("SELECT pwhash FROM accounts WHERE username=:username", {"username":session.get("username")}).fetchall()
		conn.commit()
		conn.close()
		if len(pwhash) == 0:
			return False
		if check_password_hash(pwhash[0][0], session.get("password")):
			return True
	
	return False

def is_developer(username):
	conn = sqlite3.connect('db.sql')
	c = conn.cursor()
	is_dev = c.execute("SELECT developer FROM accounts WHERE username=:username", {"username": username}).fetchall()[0][0]

	if is_dev:
		return True
	else: 
		return False
	
# def random_comment_id():
# 	temprandom = randint(100000000000000, 999999999999999)
# 	conn = sqlite3.connect('db.sql')
# 	c = conn.cursor()
# 	comments = c.execute("SELECT id FROM comments").fetchall()
# 	conn.commit()
# 	conn.close()
# 	for comment in comments:
# 		if temprandom == comment[0]:
# 			random_comment_id()
# 		else:
# 			return "c" + str(temprandom)

random_post_id()
@app.route("/")
def index(): 
	if check_if_logged_in() == False:
		return redirect("/login")

	conn = sqlite3.connect('db.sql')
	c = conn.cursor()
	posts = c.execute("SELECT * FROM posts").fetchall()
	# pfp = c.execute("SELECT pfp FROM accounts WHERE username=:username", {"username":session.get("username")}).fetchall()
	conn.commit()
	conn.close()
	# for i in reversed(posts):
	# 	print(str(i))
	return render_template("index.html", posts=reversed(posts), pfp=session.get("pfp"), username=session.get("username"))

@app.route("/register", methods=['POST', 'GET'])
def register():

	if request.method == "POST":
		if request.form.get("username") != None and request.form.get("password") != None:
			if request.form.get("password") != request.form.get("password-conf"):
				return render_template("registration-error.html", error="Your passwords don't match.")
			else: 
				conn = sqlite3.connect('db.sql')
				c = conn.cursor()
				account_usernames = c.execute("SELECT username FROM accounts").fetchall()

				for username in account_usernames:
					if "@" + request.form.get("username").lower() == username[0].lower():
						return render_template("registration-error.html", error="Username Taken.")

				if request.args.get("developer") == "true":
					c.execute("INSERT INTO accounts VALUES(?, ?, ?, ?, ?, ?)", ("@"+request.form.get("username"), generate_password_hash(request.form.get("password")), "", "", random_pfp_id(), 1))
				else:
					c.execute("INSERT INTO accounts VALUES(?, ?, ?, ?, ?, ?)", ("@"+request.form.get("username"), generate_password_hash(request.form.get("password")), "", "", random_pfp_id(), 0))

				conn.commit()
				conn.close()
				# return "Registtraction Success"
				return redirect("/login")
		else:
			return render_template("registration-error.html", error="Not all fields of the form were filled out.")
	else:
		pass

	if request.args.get("developer") != None and request.args.get("developer").lower() == "true":
		return render_template("register.html", developer="true")
	else:
		return render_template("register.html", developer="false")
	
@app.route("/login", methods=['POST', 'GET'])
def login():
	if request.method == "POST":
		conn = sqlite3.connect('db.sql')
		c = conn.cursor()
		
		stored_pwhash = c.execute("SELECT pwhash FROM accounts WHERE lower(username)=:username", {"username":"@"+request.form.get("username").lower()}).fetchall()
		stored_username = c.execute("SELECT username FROM accounts WHERE lower(username)=:username", {"username":"@"+request.form.get("username").lower()}).fetchall()
		stored_pfp = c.execute("SELECT pfp FROM accounts WHERE lower(username)=:username", {"username":"@"+request.form.get("username").lower()}).fetchall()
		conn.commit()
		conn.close()

		if len(stored_username) == 0:
			return render_template("login-error.html", error="That account doesn't exist.")

		if check_password_hash(stored_pwhash[0][0], request.form.get("password")):
			session.clear()
			session["username"] = stored_username[0][0]
			session["password"] = request.form.get("password")
			session["pfp"] = stored_pfp[0][0]
			# print("That password was correct!")
			session["logged_in"] = True
			return redirect("/")
		else:
			session.clear()
			return render_template("login-error.html", error="Incorrect password.")
	else: 
		pass
	if check_if_logged_in():
		return redirect("/")
	else:
		pass
	return render_template("login.html")

@app.route("/newpost")
def new_post():
	if check_if_logged_in() == False:
		return redirect("/login")

	return render_template("newpost.html", pfp=session.get("pfp"), username=session.get("username"))

@app.route("/publish", methods=['POST'])
def publish_post():
	title = request.form.get("title")
	content = request.form.get("body-content")
	# author = request.form.get("username")
	timestamp = datetime.datetime.now()
	timestamp = timestamp.strftime("%m/%d/%Y")
	conn = sqlite3.connect('db.sql')
	c = conn.cursor()
	if check_if_logged_in() == False:
		conn.commit()
		conn.close()
		return redirect("/login")
	random_generated = random_post_id()
	stored_pfp = c.execute("SELECT pfp FROM accounts WHERE username=:username", {"username":session.get("username")}).fetchall()
	c.execute("INSERT INTO posts VALUES(?, ?, ?, ?, ?, ?, ?)", (random_generated, session.get("username"), title, content, timestamp, 0, stored_pfp[0][0]))
	conn.commit()
	conn.close()
	#return render_template("posted.html", title=title, body=content, timestamp=timestamp)
	return redirect("/post/"+random_generated)

@app.route("/post/<post_id>")
def view_post(post_id):
	if check_if_logged_in() == False:
		return redirect("/login")
	if is_int(post_id) == False:
		return render_template("post-error.html", error="Invalid Post")
	
	argument = request.args.get("argument")

	conn = sqlite3.connect('db.sql')
	c = conn.cursor()
	data = c.execute("SELECT * FROM posts WHERE id=:post_id", {'post_id':post_id}).fetchall()
	comments = c.execute("SELECT * FROM comments WHERE post_id=:post_id", {"post_id": post_id}).fetchall()

	# Load developer information
	if is_developer(session.get("username")):
		developer = "true"
		debug_info = data[0]
		argument = request.args.get("argument")
	else:
		developer = "false"
		debug_info = ""
		argument = ""

	if argument == "iv":
		current_views = str(data[0][5])
		if data[0][1] == session.get("username"):
			delete_allowed = True
		else:
			delete_allowed = False

		# return commented page
		return render_template("viewpost.html", data=data, comments=reversed(comments), pfp=session.get("pfp"), username=session.get("username"), deleteAllowed=delete_allowed, current_views=current_views, developer=developer, debug_info=debug_info, argument=argument)

	else:
		current_views = str(data[0][5] + 1)

	c.execute("UPDATE posts SET views = views + 1 WHERE id=:post_id", {"post_id": post_id})
	if len(data) == 0:
		conn.commit()
		conn.close()
		return render_template("post-error.html", error="Invalid Post")

	# conn.commit()
	# conn.close()

	if data[0][1] == session.get("username"):
		delete_allowed = True
	else:
		delete_allowed = False
	
	#

	conn.commit()
	conn.close()
	
	return render_template("viewpost.html", data=data, comments=reversed(comments), pfp=session.get("pfp"), username=session.get("username"), deleteAllowed=delete_allowed, current_views=current_views, developer=developer, debug_info=debug_info, argument=argument)

@app.route("/comment", methods=['POST'])
def log_comment():
	# author = request.form.get("author")
	if check_if_logged_in() == False:
		return redirect("/login")
	body = request.form.get("comment")
	if body == None or  body == "" or body.isspace():
		return render_template("general-error.html", error="Comment cannot be empty")
	post_id = request.form.get("post_id")
	print(str(post_id))
	timestamp = datetime.datetime.now()
	timestamp = timestamp.strftime("%m/%d/%Y")
	conn = sqlite3.connect('db.sql')
	c = conn.cursor()
	# if check_if_logged_in() == False:
	# 	conn.commit()
	# 	conn.close()
	# 	return redirect("/login")
	profile_img_id = c.execute("SELECT pfp FROM accounts WHERE username=:username", {"username":session.get("username")}).fetchall()
	c.execute("INSERT INTO comments VALUES(?, ?, ?, ?, ?, ?, ?)", (post_id, session.get("username"), body, timestamp, 0, 0, profile_img_id[0][0]))
	conn.commit()
	conn.close()
	return redirect("/post/" + post_id + "?argument=iv")

@app.route("/profile")
def profile_custom():
	if check_if_logged_in() == False:
		return redirect("/login")
	else:
		pass

	# Send all the account information to profile page
	return redirect("/profile/" + session.get("username"))

@app.route("/profile/<username>")
def profile_general(username):
	if username == "[DELETED_ACCOUNT]":
		return render_template("general-error.html", error="This page is a temporary plceholder for deleted accounts.\nDeleted account do not have any information apart from saved comments and posts.\nThey will all be displayed under the name \"[DELETED_ACCOUNT]\"")
	
	if check_if_logged_in() == False:
		return redirect("/login")
	# Send all the account information to profile page
	conn = sqlite3.connect('db.sql')
	c = conn.cursor()
	account_information = c.execute("SELECT * FROM accounts WHERE lower(username)=:username", {"username":username.lower()}).fetchall()
	conn.commit()
	conn.close()
	if len(account_information) == 0:
		return render_template("general-error.html", error="That account doesn't exist.")

	if is_developer(session.get("username")):
		developer = "true"
		debug_info = account_information[0]
	else:
		developer = "false"
		debug_info = ""

	return render_template("profile.html", information=account_information[0], pfp=session.get("pfp"), username=session.get("username"), developer=developer, debug_info=debug_info)

#account

@app.route("/account")
def account_dashboard():
	if check_if_logged_in() == False:
		return redirect("/login")
	# return "Your are logged in as "+session.get("username")
	conn = sqlite3.connect('db.sql')
	c = conn.cursor()
	account_information = c.execute("SELECT * FROM accounts WHERE username=:username", {"username":session.get("username")}).fetchall()
	conn.commit()
	conn.close()
	return render_template("account.html", information=account_information[0], pfp=session.get("pfp"), username=session.get("username"))

@app.route("/edit-account", methods=['POST'])
def update_account():
	if check_if_logged_in() == False:
		return redirect("/login")
	input_username = "@"+request.form.get("username")
	bio = request.form.get("bio")
	status = request.form.get("status")
	conn = sqlite3.connect('db.sql')
	c = conn.cursor()

	c.execute("UPDATE accounts SET bio=:bio WHERE username=:username", {"bio":bio,"username":session.get("username")})

	c.execute("UPDATE accounts SET status=:status WHERE username=:username", {"status":status,"username":session.get("username")})
	
	# print(input_username.lower(), session.get("username").lower())
	
	if input_username.lower() != session.get("username").lower():

		stored_usernames = c.execute("SELECT username FROM accounts").fetchall()

		for username in stored_usernames:
			if input_username.lower() == username[0].lower():
				# return "Username taken"
				return render_template("account-error.html", error="Username Taken")

		c.execute("UPDATE posts SET author=:new_username WHERE author=:old_username", {"new_username":input_username,"old_username":session.get("username")})

		c.execute("UPDATE comments SET author=:new_username WHERE author=:old_username", {"new_username":input_username,"old_username":session.get("username")})
		
		c.execute("UPDATE accounts SET username=:input_username WHERE username=:old_username", {"input_username":input_username, "old_username":session.get("username")})

		session["username"] = input_username
	

	conn.commit()
	conn.close()
	return redirect("/account")

@app.route("/logout")
def logout():
	session.clear()
	return redirect("/login")

@app.route("/remove/<post_id>")
def remove_post(post_id):
	if check_if_logged_in() == False:
		return redirect("/login")
	
	conn = sqlite3.connect('db.sql')
	c = conn.cursor()
	post_author = c.execute("SELECT author FROM posts WHERE id=:id", {"id": post_id}).fetchall()
	if post_author[0][0] != session.get("username"):
		return render_template("general-error.html", error="You are not allowed to delete that post.")
	else: 
		pass

	c.execute("DELETE FROM posts WHERE id=:id", {"id": post_id})
	c.execute("DELETE FROM comments WHERE post_id=:id", {"id": post_id})
	conn.commit()
	conn.close()
	return redirect("/")

@app.route("/delete-everything")
def delete_everything():
	conn = sqlite3.connect('db.sql')
	c = conn.cursor()
	c.execute("DELETE FROM accounts WHERE username=:username", {"username": session.get("username")})
	# delete all comments
	c.execute("DELETE FROM comments WHERE author=:username", {"username":session.get("username")})

	# delete all posts including linked comments
	saved_posts = c.execute("SELECT id FROM posts WHERE author=:username", {"username": session.get("username")}).fetchall()
	for post in saved_posts:
		c.execute("DELETE FROM comments WHERE post_id=:post_id", {"post_id": post[0]})

	c.execute("DELETE FROM posts WHERE author=:username", {"username": session.get("username")})

	conn.commit()
	conn.close()

	return redirect("/")

@app.route("/delete-account", methods=['GET'])
def delete_account():
	conn = sqlite3.connect('db.sql')
	c = conn.cursor()
	c.execute("DELETE FROM accounts WHERE username=:username", {"username": session.get("username")})
	# rename all comments
	c.execute("UPDATE comments SET author='[DELETED_ACCOUNT]', pfp='0' WHERE author=:username", {"username":session.get("username")})
	# rename all posts excluding linked comments
	c.execute("UPDATE posts SET author='[DELETED_ACCOUNT]', pfp='0' WHERE author=:username", {"username": session.get("username")})

	conn.commit()
	conn.close()
	return redirect("/")

@app.route("/delete-posts")
def delete_posts():
	conn = sqlite3.connect('db.sql')
	c = conn.cursor()
	saved_posts = c.execute("SELECT id FROM posts WHERE author=:username", {"username": session.get("username")}).fetchall()
	for post in saved_posts:
		c.execute("DELETE FROM comments WHERE post_id=:post_id", {"post_id": post[0]})

	c.execute("DELETE FROM posts WHERE author=:username", {"username": session.get("username")})
	conn.commit()
	conn.close()
	return redirect("/account")

@app.route("/delete-comments")
def delete_comments():
	conn = sqlite3.connect('db.sql')
	c = conn.cursor()
	c.execute("DELETE FROM comments WHERE author=:username", {"username":session.get("username")})
	conn.commit()
	conn.close()
	return redirect("/account")

@app.route("/api/about")
def api_about():
	return redirect("https://github.com/JonathanW2018/SharePost#api")

@app.route("/api", methods=['GET'])
def access_api():
	profile_username = request.args.get("profile")
	if profile_username == None or profile_username.isspace() or profile_username == "":
		return "Missing parameters."
	conn = sqlite3.connect('db.sql')
	c = conn.cursor()
	profile_information = c.execute("SELECT * FROM accounts WHERE lower(username)=:profile_username", {"profile_username":profile_username.lower()}).fetchall()
	account_posts = c.execute("SELECT * FROM posts WHERE lower(author)=:profile_username", {"profile_username":profile_username.lower()}).fetchall()
	account_comments = c.execute("SELECT * FROM comments WHERE lower(author)=:profile_username", {"profile_username":profile_username.lower()}).fetchall()
	conn.commit()
	conn.close()
	if len(profile_information) == 0:
		return "Profile doesn't exist"
	return jsonify({'username': profile_information[0][0], 'bio': profile_information[0][2], 'status': profile_information[0][3], 'profile_picture': f"https://SharePost.jonathan2018.repl.co/static/images/profile/pfp-{profile_information[0][4]}.png", 'comments': len(account_comments), 'posts': len(account_posts)})

# Google #
@app.route("/googleb228004b8b05137a.html")
def google_site_verification():
	return render_template("Google/googleb228004b8b05137a.html")

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)