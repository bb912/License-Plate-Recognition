
from flask import Flask, render_template, request, redirect, url_for, make_response
import hashlib
import pymysql
from sqlalchemy import create_engine, or_, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Customer, Service
from gevent.pywsgi import WSGIServer
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)



@app.route('/')
def hello():
    return 'Hello, World!'


if __name__ == '__main__':
		pymysql.install_as_MySQLdb()
		app.debug = True
		#http_server = WSGIServer(('', 4996), app)
		print("serving...forever")
		#http_server.serve_forever()
		app.run(host='0.0.0.0', port=4996)
