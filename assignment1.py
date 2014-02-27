from faker import Faker
from datetime import date, timedelta
import random

from models import *
import flow

# Make Faker data
fake = Faker()

def run(customer_list):

	# Sort the customers by arrival time
	customer_list.sort(key=lambda tup: tup[0]);

	customers = []

	for (time, customer) in customer_list:
		customers.append(customer)

	successful_customers = flow.run(customers)

	licenses = []

	for customer in successful_customers:
		licenses.append(customer.uae_license)

	return licenses

# Makes a random customer, for testing
def make_customer():
	id = Emirates_ID(fake.first_name(), fake.last_name(), fake.country_code(), "male",
		fake.date_time_between(start_date="-30y", end_date="-18y"), fake.date_time_between(start_date="-1yr", end_date="+3yrs"), fake.random_int(min=0, max=9999))

	license = Drivers_License(id.first_name, id.last_name, id.nationality, id.gender, id.date_of_birth, fake.date_time_between(start_date="-1yr", end_date="+3yrs"))

	passport = Passport(id.first_name, id.last_name, id.nationality, id.gender, id.date_of_birth, fake.date_time_between(start_date="-1yr", end_date="+3yrs"))

	eye_test = None

	translation = None

	# if (random.randint(0,1) < 1):
		# id = None7

	customer = Customer(id, license, passport, eye_test, translation)

	return customer;


# This is for testing
def main():
	customers = []

	for i in range(10):
		customers.append((fake.date_time_this_month(), make_customer()))

	successful = run(customers)

	for license in successful:
		print "%s was successful" % license.driver.emirates_id.first_name

if __name__ == "__main__":
    main()