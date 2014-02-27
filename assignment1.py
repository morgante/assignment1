from faker import Faker
from datetime import date

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

	flow.run(customers)

	return 'done'

# Makes a random customer, for testing
def make_customer():
	id = Emirates_ID(fake.first_name(), fake.last_name(), fake.country_code(), "male",
		fake.date_time_between(start_date="-30y", end_date="-18y"), fake.date_time_this_year(), fake.random_int(min=0, max=9999))

	license = None

	passport = None

	eye_test = None

	translation = None

	customer = Customer(id, license, passport, eye_test, translation)

	return customer;


# This is for testing
def main():
	customers = []

	for i in range(1):
		customers.append((fake.date_time_this_month(), make_customer()))

	run(customers);

main()