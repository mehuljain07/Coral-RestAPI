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

