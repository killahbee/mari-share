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

	neighborhoods = db.neighborhoods.getNeighborhoods()
	
	return render_template("welcome/welcome.html",
		user=user,
		neighborhoods=neighborhoods)

@application.app.route("/users/<userid>/", methods=["POST"])
@tools.authenticated
def update_user( user, userid ):

	role = request.form.get("role", "")
	description = request.form.get("description", "")
	neighborhood = request.form.get("neighborhood", "")

	if userid != user["userid"]:
		return "403", 403

	try:

		# Open a cursor to perform database operations
		conn = db.get_db()
		cur = conn.cursor()

		sql_query = "UPDATE users SET role = %s, bio = %s, neighborhood = %s WHERE userid = %s;"
		sql_data = ( role, description, neighborhood, userid )

		cur.execute( sql_query, sql_data )

		conn.commit()
		cur.close()

	except db.psycopg2.DatabaseError, e:
		# if I have a connection
		print e
		if conn:
			conn.rollback()

	return redirect(url_for("dashboard"))