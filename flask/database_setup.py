# much of this code has been modified from
# https://www.kite.com/blog/python/flask-tutorial/

import sys

# for creating the mapper code
from sqlalchemy import Column, ForeignKey, Integer, String

# for configuration and class code
from sqlalchemy.ext.declarative import declarative_base

# for creating foreign key relationship between the tables
from sqlalchemy.orm import relationship

# for configuration
from sqlalchemy import create_engine
import hashlib
# create declarative_base instance
Base = declarative_base()

# the Auto Nation customer that whose car may be in video feed
class Customer(Base):
		__tablename__ = 'Contacts'

		ID = Column(Integer, primary_key=True)
		FirstName = Column(String(50), nullable=False)
		LastName = Column(String(50), nullable=False)
		Email = Column(String(80), nullable=True)
		PhoneNumber = Column(String(20), nullable=False)
		VehicleType = Column(String(20), nullable=True)
		# advisor name / license plate
		LicensePlate = Column(String(10), nullable=False)
		# if we had more time...
		# make History a separate model / object
		# holds objects that are dated service instances
		# We can still do this just need a separate table or nonrelational DB

		@property
		def serialize(self):
				return {
						'FirstName' : self.FirstName,
						'LastName' : self.LastName,
						'Email' : self.Email,
						'Phone' : self.PhoneNumber,
						'ID': self.ID,
						'LicensePlate' : self.LicensePlate,
						'VehicleType' : self.VehicleType,
				}


# generic service instance
class Service(Base):
	__tablename__ = 'ServiceInstance'

	ID = Column(Integer, primary_key=True)
	CustomerID = Column(Integer, nullable=False)
	Service = Column(String(80), nullable=False)
	AdvisorName = Columns(String(20), nullable=False)

	# TODO: Date time object?????
	Date = Column(String(50), nullable=False)

	@property
	def serialize(self):
			return {
					'CustomerID' : self.CustomerID,
					'ID': self.ID,
					'Service': self.Service,
					'Date' : self.Date,
					'AdvisorName': self.AdvisorName
			}




'''
		GET: The GET method is only used to retrieve information from the given server. Requests using this method should only recover data and should have no other effect on the data.
		POST: A POST request is used to send data back to the server using HTML forms.
		PUT: A PUT request replaces all the current representations of the target resource with the uploaded content.
		DELETE: A DELETE request removes all the current representations of the target resource given by URI.
'''
