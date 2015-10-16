from flask import g
from flask import Flask
from flask import request
from flask import session
from flask import jsonify
from flask import url_for
from flask import redirect
from flask import send_file
from flask import render_template

import db
import application
import application.tools as tools

@application.app.route("/welcome/", methods=["GET"])
@tools.dbauthenticated
def welcome( user ):
	
	return render_template("welcome/welcome.html",
		user=user)

@application.app.route("/users/<userid>/", methods=["POST"])
@tools.authenticated
def update_user( user, userid ):

	role = request.form.get("role", "")
	description = request.form.get("description", "")
	neighborhood = request.form.get("neighborhood", "")

	if userid != user["id"]:
		return "403", 403

	try:

		# Open a cursor to perform database operations
		conn = db.get_db()
		cur = conn.cursor()

		sql_query = "INSERT INTO users (role, bio, neighborhood) VALUES (%s, %s, %s);"
		sql_data = ( role, description, neighborhood )

		cur.execute( sql_query, sql_data )

		conn.commit()
		cur.close()

	except db.psycopg2.DatabaseError, e:
		# if I have a connection
		print e
		if conn:
			conn.rollback()

	return redirect(url_for("dashboard"))