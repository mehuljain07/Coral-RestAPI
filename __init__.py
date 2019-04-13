from flask import Flask
from flask_cors import CORS
from flaskext.mysql import MySQL
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

mysql = MySQL() 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'dummyUser'
app.config['MYSQL_DATABASE_PASSWORD'] = 'dummyUser01'
app.config['MYSQL_DATABASE_DB'] = 'db_intern'
app.config['MYSQL_DATABASE_HOST'] = 'db-intern.ciupl0p5utwk.us-east-1.rds.amazonaws.com'
mysql.init_app(app)


from package import routes
