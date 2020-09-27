
from flask import Flask, render_template, request, redirect, url_for, make_response
import hashlib
import pymysql
from sqlalchemy import create_engine, or_, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Customer, Service
from gevent.pywsgi import WSGIServer
from werkzeug.utils import secure_filename
from datetime import datetime
from flask_sqlalchemy import SQLalchemy
app = Flask(__name__)

# THIS IS WHERE THE UPLOADED FILES GET SAVED
app.config['UPLOAD_FOLDER'] = '/tmp/cars'
#engine = create_engine('mysql+pymysql://lp:plate@35.237.243.227/auto')
#engine = create_engine('mysql+pymysql://lp:plate@35.237.243.227/auto?unix_socket=cloudsql/auto-nation')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
db.create_all()

DBSession = sessionmaker(bind=db)
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


# get a single Customer by its id number
def get_customer(lp_num):
		customer = session.query(Customer).filter_by(LicensePlate = lp_num).one()
		return jsonify(Customer=Customer.serialize)

# create a new Customer given all information
def create_customer(first_name, last_name, phone, email, lp_num):
		add_customer = Customer(FirstName=first_name, LastName=last_name,
														PhoneNumber=phone,
														Email=email,
														LicensePlate=lp_num,
														VehicleType=vehicle)
		session.add(added_Customer)
		session.commit()
		return "Added Customer with id %s" % added_Customer.ID

# delete Customer by Customer ID
def delete_customer(id):
		Customer_to_delete = session.query(Customer).filter_by(ID=id).one()
		session.delete(Customer_to_delete)
		session.commit()
		return "Removed Customer with id %s" % id


# update an existing Customer
def update_customer(customer_id, first_name, last_name, phone, email, lp_num, vehicle):
		updated_Customer = session.query(Customer).filter_by(ID=customer_id).one()

		if first_name:
				updated_Customer.FirstName = first_name
		if last_name:
				updated_Customer.LastName = last_name
		if phone:
				updated_Customer.PhoneNumber = phone
		if email:
				updated_Customer.Email = email
		if lp_num:
				updated_Customer.LicensePlate = lp_num
		if vehicle:
				updated_Customer.VehicleType = vehicle

		session.add(updated_Customer)
		session.commit()

		return "Updated Customer with id %s" % Customer_id

# list Customers or add a Customer (for a specific user)

# GET request requires user_id in json

#POST request requires first_name, last_name, phone, email, user_id,

#ADDING A Customer FOR A USER
@app.route('/')
@app.route('/CustomersApi', methods=['POST'])
def PostNewCustomer():

		#if request.method == "OPTIONS": # CORS preflight
		#		return _build_cors_prelight_response()

		body = request.get_json(force=True)

		first = body.get('FirstName', '')
		last = body.get('LastName', '')
		phone = body.get('PhoneNumber', '')
		email = body.get('Email', '')
		lp = body.get('LicensePlate', '')
		vt = body.get('VehicleType', '')
		return create_new_Customer(first, last, phone, email, lp, vt)


# get a specific Customer by Customer ID, or update Customer, or delete Customer
@app.route('/CustomersApi/<int:id>', methods=['GET', 'POST'])
#@cross_origin()
def CustomersFunctionID(id):
		if request.method == 'GET':
				return get_Customer(id)

		elif request.method == 'POST':

				body = request.get_json(force=True)

				first = body.get('FirstName', '')
				last = body.get('LastName', '')
				phone = body.get('PhoneNumber', '')
				email = body.get('Email', '')
				user = body.get('UserID', '')
				return update_Customer(id, first, last, phone, email, lp, vt)


# get a specific Customer by Customer ID, or update Customer, or delete Customer
@app.route('/CustomersApi/<int:id>/delete', methods=['POST'])
#@cross_origin()
def CustomersFunctionDelete(id):
		return delete_Customer(id)



"""

Service API



"""

# get a single Customer by its id number
def get_services(lp_num):
		service = session.query(Customer).filter_by(LicensePlate = lp_num)
		return jsonify(Customer=Customer.serialize)

# create a new service given all information
def create_service(customer_id, service, advisor_name, date):
		add_service = service(CustomerID=customer_id, Service=service,
														AdvisorName=advisor_name,
														Date=date)
		session.add(added_service)
		session.commit()
		return "Added service with id %s" % added_service.ID

# delete service by service ID
def delete_service(id):
		service_to_delete = session.query(service).filter_by(ID=id).one()
		session.delete(service_to_delete)
		session.commit()
		return "Removed service with id %s" % id


# update an existing service
def update_service(service_id, customer_id, service, advisor_name, date):

		if not service_id:
			return "Error, include sevice_id"

		updated_service = session.query(service).filter_by(ID=service_id).one()

		if customer_id:
				updated_service.CustomerID = customer_id
		if service:
				updated_service.Service = service
		if advisor_name:
				updated_service.AdvisorName = advisor_name
		if date:
				updated_service.Date = date


		session.add(updated_service)
		session.commit()

		return "Updated service with id %s" % service_id



# ADDING A service FOR A USER
@app.route('/')
@app.route('/servicesApi', methods=['POST'])
def PostNewservice():

		body = request.get_json(force=True)

		cid = body.get('CustomerID', '')
		service = body.get('Service', '')
		advisor = body.get('AdvisorName', '')
		date = body.get('Date', '')
		return create_new_service(cid, service, advisor, date)


# get a specific service by service ID, or update service, or delete service
@app.route('/servicesApi/<int:id>', methods=['POST'])
def servicesFunctionID(id):

		cid = body.get('CustomerID', '')
		service = body.get('Service', '')
		advisor = body.get('AdvisorName', '')
		date = body.get('Date', '')
		return update_service(sid, cid, service, advisor, date)


# get a specific service by service ID, or update service, or delete service
@app.route('/servicesApi/<int:id>/delete', methods=['POST'])
#@cross_origin()
def servicesFunctionDelete(id):
		return delete_service(id)




"""
Photo uploading endpoints and user searching

"""

# for updating User's personal information
@app.route('/whichCustomer', methods=['POST'])
#@cross_origin()
def whichCustomer():
		if request.method == 'POST':
				file1 = request.files.get('a', None);
				file2 = request.files.get('b', None);
				file3 = request.files.get('c', None);

				if file1 and file1.filename:
					file1.save(os.path.join(UPLOADS_PATH, secure_filename(file1.filename)))
					a = 1
				if file2 and file2.filename:
					file2.save(os.path.join(UPLOADS_PATH, secure_filename(file2.filename)))

					b = 1
				if file3 and file3.filename:
					file3.save(os.path.join(UPLOADS_PATH, secure_filename(file3.filename)))

				# TODO: CALL THE BASH SCRIPT HERE ... conda activate && etc

				# scrape csv file

				# "vote" on the result, call above functions to search for which customer it is

				return None


if __name__ == '__main__':
		pymysql.install_as_MySQLdb()
		app.debug = True
		#http_server = WSGIServer(('', 4996), app)
		print("serving...forever")
		#http_server.serve_forever()
		app.run(host='0.0.0.0', port=4996)
