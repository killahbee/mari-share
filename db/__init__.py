import application

from flask import g

import os
import datetime
import psycopg2
import psycopg2.extras

from psycopg2.extensions import adapt, register_adapter, AsIs

# import other db libraries
import db.user as user
import db.admin as admin
import db.neighborhoods as neighborhoods

def connect_db():
	return psycopg2.connect(database=application.app.config["DB_NAME"],
		user=application.app.config["DB_ADMIN"],
		password=application.app.config["DB_PASSWORD"],
		host=application.app.config["DB_HOST"])

def get_db():
	db = getattr(g, 'db', None)

	if db is None:
		db = g.db = connect_db()

	return db