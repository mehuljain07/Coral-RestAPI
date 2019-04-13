from flask import render_template, request, jsonify
from package import app,mysql

from datetime import datetime
import hashlib


#Registration API

@app.route('/register',methods = ['GET','POST'])
def register():
	if(request.method == 'POST'):
		try:
			#mySqlConnection
			conn = mysql.connect()
			c = conn.cursor()
			r = request.get_json()
			username = str(r['username'])
			pwd = r['password']
			password = str(hashlib.sha1(pwd.encode('utf-8')).hexdigest())
			phone = str(r['phone'])
			email = str(r['email'])
			now = datetime.now()
			f = '%Y-%m-%d %H:%M:%S'
			dt = now.strftime(f)
			searchStmt = 'SELECT * FROM userData WHERE emailId=%s'
			c.execute(searchStmt,(email,))
			#return str(c.fetchall()),200
			if(c.rowcount == 0):
				insert_stmt = 'insert into userData(userName,emailId,phoneNo,password,dateTime) values(%s,%s,%s,%s,%s)'
				data = (username,email,phone,password,dt)
				c.execute(insert_stmt,data)
				conn.commit()
				c.close()
				return str("User Added Successfully"),200
			else:
				updateStmt = 'UPDATE userData SET userName=%s, emailId=%s, phoneNo=%s, password=%s, datetime=%s WHERE emailId=%s'
				c.execute(updateStmt,(username,email,phone,password,dt,email))
				conn.commit()
				c.close()
				return ('Record Updated Successfully'),200
		except Exception as e:
			return str(e),400
		finally:
			conn.close()
		
	else:
		return render_template('form.html')

@app.route('/search',methods=['POST'])
def search():
	try:
		conn = mysql.connect()
		c = conn.cursor()
		email = request.get_json()['emailId']
		searchStmt = 'SELECT * FROM userData WHERE emailId=%s'
		c.execute(searchStmt,(email,))
		if(c.rowcount == 0):
			return str('No record found for '+email),400	
		else:
			record = c.fetchone()
			newDict = {"username":record[0],"email":record[1],"phone":record[2]}
			return jsonify(newDict),200

	except Exception as e:
		return str(e),400

'''
#Add a User
@app.route("/api/v1/users",methods = ['POST'])
def create_user():
	global reqCounter
	reqCounter = reqCounter + 1
	new_User = User.query.filter_by(username = request.get_json().keys()[0])
	if(new_User.first() is None):
		try:
			password = request.get_json()['password']
			if(len(password)<40):
				return str("Bad Request"),400
			password = hashlib.sha1(password).hexdigest()
			new_User = User(request.get_json()['username'],password)
			db.session.add(new_User)
			db.session.commit()
			return str('User Registered.</br>Please Go to <a href = login>Login page</a></br>'),201
		except Exception as e:
			return str(e),400
	else:
		return str("Username already taken"),400

#Signup
@app.route("/api/v1/signup",methods=['GET'])
def signup():
	return render_template("register.html"),200


#Login User
@app.route("/api/v1/login",methods = ['GET','POST'])
def loginUser():
	if(request.method == 'GET'):
		return render_template("login.html"),200
	else:
		result = request.form
		userName = result['username']
		password = result['password']
		user = User.query.filter_by(username = userName).first()
		if (user and (hashlib.sha1(password).hexdigest() == user.password)):
			login_user(user)
			return redirect("http://34.238.62.10:8000/api/v1/home"),201
		else:
			return str("Username/Password Incorrect."),400

#logout
@app.route("/api/v1/logout")
def logout():
	logout_user()
	return render_template('home.html'),400

#Remove a user
@app.route("/api/v1/users/<userName>",methods=['DELETE'])
def delete_user(userName):
	global reqCounter
	reqCounter = reqCounter + 1
	# if(current_user.is_authenticated):
	user = User.query.filter_by(username = userName)
	if(user.first() is None):
		return str("Users does not exist."),400
	else:
		stmt = "delete from User where username = '"+userName+"'"
		db.session.execute(stmt)
		db.session.commit()
		logout_user()
		return str("User "+userName+" deleted successfully"),200
	# else:
	#  	return render_template("login.html")

#List all users
@app.route("/api/v1/users",methods = ["GET"])
def get_all_users():
	global reqCounter
	reqCounter = reqCounter + 1
	try:
		users = User.query.all()
		if(len(users) == 0):
			return str("No Content"),204
		response = []
		for user in users:
			response.append(user.username)
		return jsonify(response),200
	except Exception as e:
		return str("Bad Request"),405
		
#number of requests
@app.route("/api/v1/_count",methods=['GET','DELETE'])
def _count():
	global reqCounter
	if(request.method == "DELETE"):
		reqCounter = 0
		return jsonify([reqCounter]),200
	else:
		return jsonify([reqCounter]),200
		
		
'''



