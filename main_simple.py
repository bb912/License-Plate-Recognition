
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

# THIS IS WHERE THE UPLOADED FILES GET SAVED
app.config['UPLOAD_FOLDER'] = '/tmp/cars'
engine = create_engine('mysql+pymysql://lp:plate@35.237.243.227/auto')
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.errorhandler(404)
def not_found():
		return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def hello():
    return 'Hello, World!'
"""

Customers API
@app.route('/CustomersApi', methods=['POST'])
		-add new customers for database input
@app.route('/CustomersApi/<int:id>', methods=['GET', 'POST'])
		-update or get customer based on id
@app.route('/CustomersApi/<int:id>/delete', methods=['POST'])
		-delete customer based on id


"""
from flask import jsonify


if __name__ == '__main__':
		pymysql.install_as_MySQLdb()
		app.debug = True
		#http_server = WSGIServer(('', 4996), app)
		print("serving...forever")
		#http_server.serve_forever()
		app.run(host='0.0.0.0', port=4996)
