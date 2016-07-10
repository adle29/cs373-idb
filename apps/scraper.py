import requests
import psycopg2



def connect_db():
	try:
		conn = psycopg2.connect("dbname='scrub' user='postgres' host='198.199.84.221'	password='asdf'")
	except:
   		print "I am unable to connect to the database"

def scrape():
	pass

if __name__ == '__main__':
	connect_db()
	scrape()