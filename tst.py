#!/usr/bin/python3
import os

os.environ['HBNB_MYSQL_USER'] = "hbnb_dev"
os.environ['HBNB_MYSQL_PWD'] = "hbnb_dev_pwd"
os.environ['HBNB_MYSQL_HOST'] = "localhost"
os.environ['HBNB_MYSQL_DB'] = "hbnb_dev_db"
os.environ['HBNB_TYPE_STORAGE'] = "db"
os.environ['HBNB_ENV'] = "dev"

mysql_user = os.environ.get('HBNB_MYSQL_USER')
mysql_password = os.environ.get('HBNB_MYSQL_PWD')
mysql_host = os.environ.get('HBNB_MYSQL_HOST')
mysql_db = os.environ.get('HBNB_MYSQL_DB')

print("mysql_user: {}, mysql_password: {}, mysql_host: {}, mysql_db: {}".\
        format(mysql_user, mysql_password, mysql_host, mysql_db))
