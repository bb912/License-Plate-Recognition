
from flask import Flask, render_template, request, redirect, url_for, make_response
import hashlib
import pymysql
from sqlalchemy import create_engine, or_, asc, DateTime
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Customer, Service
from gevent.pywsgi import WSGIServer
from werkzeug.utils import secure_filename
from datetime import datetime


from twilio.rest import Client
from typing import Type
import json

account_sid = 'ACfa3ae5e3f45bc3117c8acdb2a746dda5'
auth_token = '7e15399f44e042b97717e65304363462'
client = Client(account_sid, auth_token)
msg = ""
link = "www.autonation.com"


def send_msg(msg, to):
    message = client.messages.create(
        from_='+14708237238',
        body=msg,
        to=to
    )
    return message


def appointment_found(service, user):
    msg = f"Greetings {service.AdvisorName}!\n{user.FirstName} {user.LastName} is "\
        f"here for their {service.Date.time()} appointment"
    return send_msg(msg, service.AdvisorPhone)


def appointment_not_found(user):
    msg = f"Greetings {user.FirstName}!\nThank you for visiting AutoNation "\
          f"We did not find any appointments for you today.\n\nIf you wish to"\
          f" schedule a drive-in appointment you can do it directly from {link}"
    return send_msg(msg, user.PhoneNumber)


def appointment_too_early(user, timediff):
    msg = f"Greetings {user.FirstName} {user.LastName}!\nThank you for visiting AutoNation "\
          f"It looks like you are {timediff} minutes early, please wait."

    return send_msg(msg, user['PhoneNumber'])

def appointment_late(user, timediff):
    msg = f"Greetings {user.FirstName} {user.LastName}!\nThank you for visiting AutoNation "\
          f"It looks like you are {timediff} minutes late. Would you like to reschedule at {link}?"
    return send_msg(msg, user['PhoneNumber'])


app = Flask(__name__)

# THIS IS WHERE THE UPLOADED FILES GET SAVED
app.config['UPLOAD_FOLDER'] = '/tmp/cars'
#engine = create_engine('mysql+pymysql://lp:plate@35.237.243.227/auto')
#engine = create_engine('mysql+pymysql://lp:plate@35.237.243.227/auto?unix_socket=cloudsql/auto-nation')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlalchemy_example.db'
!sudo chmod 664 sqlalchemy_example.db
engine = create_engine('sqlite:///sqlalchemy_example.db', pool_pre_ping=True)
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()



@app.errorhandler(404)
def not_found():
		return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def index():
    # rendering webpage
    return "Hello World"



"""

Customers API
app.route('/CustomersApi', methods=['POST'])
		-add new customers for database input
app.route('/CustomersApi/<int:id>', methods=['GET', 'POST'])
		-update or get customer based on id
app.route('/CustomersApi/<int:id>/delete', methods=['POST'])
		-delete customer based on id


"""
from flask import jsonify


# get a single Customer by its id number
def get_customer(lp_num):
		customer = session.query(Customer).filter_by(LicensePlate = lp_num).first()
		if customer is None:
			return None


		return customer

# create a new Customer given all information
def create_customer(first_name, last_name, phone, email, lp_num, vehicle):
		added_customer = Customer(FirstName=first_name, LastName=last_name,
														PhoneNumber=phone,
														Email=email,
														LicensePlate=lp_num,
														VehicleType=vehicle)
		session.add(added_customer)
		session.commit()
		return "Added Customer with id %s" % added_customer.ID

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

		return "Updated Customer with id %s" % customer_id

# list Customers or add a Customer (for a specific user)

# GET request requires user_id in json

#POST request requires first_name, last_name, phone, email, user_id,

#ADDING A Customer FOR A USER
@app.route('/CustomersApi', methods=['GET', 'POST'])
def PostNewCustomer():

		#if request.method == "OPTIONS": # CORS preflight
		#		return _build_cors_prelight_response()


		if request.method == 'GET':
				lp = body.get('LicensePlate', '')
				return get_customer(lp)

		body = request.get_json(force=True)

		first = body.get('FirstName', '')
		last = body.get('LastName', '')
		phone = body.get('PhoneNumber', '')
		email = body.get('Email', '')
		lp = body.get('LicensePlate', '')
		vt = body.get('VehicleType', '')
		return create_customer(first, last, phone, email, lp, vt)


# get a specific Customer by Customer ID, or update Customer, or delete Customer
@app.route('/CustomersApi/<int:id>', methods=['POST'])
#@cross_origin()
def CustomersFunctionID(id):
		body = request.get_json(force=True)


		first = body.get('FirstName', '')
		last = body.get('LastName', '')
		phone = body.get('PhoneNumber', '')
		email = body.get('Email', '')
		lp = body.get('LicensePlate', '')
		vt = body.get('VehicleType', '')
		return update_customer(id, first, last, phone, email, lp, vt)


# get a specific Customer by Customer ID, or update Customer, or delete Customer
@app.route('/CustomersApi/<int:id>/delete', methods=['POST'])
#@cross_origin()
def CustomersFunctionDelete(id):
		return delete_Customer(id)



"""

Service API



"""

# get a single Customer by its id number
def get_services(customer_id):
		service = session.query(Service).filter_by(CustomerID = customer_id)
		return list(serv for serv in service)

# create a new service given all information
def create_service(customer_id, service, advisor_name, phone):
		added_service = Service(CustomerID=customer_id, Service=service,
														AdvisorName=advisor_name,
														Date=datetime.now(),
														AdvisorPhone=phone)
		session.add(added_service)
		session.commit()
		return "Added service with id %s" % added_service.ID

# delete service by service ID
def delete_service(id):
		service_to_delete = session.query(Service).filter_by(ID=id).one()
		session.delete(service_to_delete)
		session.commit()
		return "Removed service with id %s" % id


# update an existing service
def update_service(service_id, customer_id, service, advisor_name, date, advisor_phone):

		if not service_id:
			return "Error, include sevice_id"

		updated_service = session.query(Service).filter_by(ID=service_id).one()

		if customer_id:
				updated_service.CustomerID = customer_id
		if service:
				updated_service.Service = service
		if advisor_name:
				updated_service.AdvisorName = advisor_name
		if date:
				updated_service.Date = date
		if advisor_phone:
				updated_service.AdvisorPhone = advisor_phone


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
		phone = body.get('AdvisorPhone', '')
		return create_service(cid, service, advisor, phone)


# get a specific service by service ID, or update service, or delete service
@app.route('/servicesApi/<int:sid>', methods=['POST'])
def servicesFunctionID(id):
		body = request.get_json(force=True)

		phone = body.get('AdvisorPhone', '')
		cid = body.get('CustomerID', '')
		service = body.get('Service', '')
		advisor = body.get('AdvisorName', '')
		date = body.get('Date', '')
		return update_service(sid, cid, service, advisor, date, phone)


# get a specific service by service ID, or update service, or delete service
@app.route('/servicesApi/<int:id>/delete', methods=['POST'])
#@cross_origin()
def servicesFunctionDelete(id):
		return delete_service(id)




"""
Photo uploading endpoints and user searching

"""
@app.route('/NumsBack', methods=['GET'])
def lp_back():
	body = request.get_json(force=True)

	# send back the licenses in a json with a, b ,c keys
	num1 = body.get('a', '')
	num2 = body.get('b', '')
	num3 = body.get('c', '')


	# for each of the three pics
	for num in [num1, num2, num3]:
		# get person associated with num
		person = get_customer(num)


		if person is not None:
			break
		# get id associated with lp_num

	if person is None:
		return "Plate does not exist in database"

	id = person.ID


	if id is not None:
		today = datetime.date
		servs = get_services(id)
		for service in servs:
			if service is None or service.Date.day != today:
				continue
			else:
				time_diff = datetime.time - service.get('Date').time

				# time diff greater than 30 min
				if time_diff > 30:
					sent_msg = appointment_late(person, service)
					return "message sent, appt late"
				elif time_diff < 30 and time_diff > 10:
					sent_msg = appointment_too_early(person, sevice)
					return "message sent, appt early"


		sent_msg = appointment_found(service, person)
	else:
		sent_msg = appointment_not_found(person)

		return "message has been sent"



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
		app.run(host='127.0.0.1', port=8080, debug=True)
