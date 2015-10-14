from flask import g
from flask import Flask
from flask import request
from flask import session
from flask import jsonify
from flask import url_for
from flask import redirect
from flask import send_file
from flask import render_template
from flask.ext.bcrypt import Bcrypt

import application
import application.db as db

@application.app.route("/", methods=["GET"])
def main():
	
	return render_template("public/front_page.html")

@application.app.route("/signup/", methods=["POST"])
def signup():
	
	if request.method == "POST":

		email = request.form.get("email", "")
		username = request.form.get("username", "")
		password = request.form.get("password", "")

		print email
		print username
		print password

		try:
			bc = Bcrypt(None)
			hashed_pw = bc.generate_password_hash( password )

			print hashed_pw

			# Open a cursor to perform database operations
			conn = db.get_db()
			cur = conn.cursor()

			sql_query = "SELECT * FROM users WHERE email = %s;"
			sql_data = ( email, )

			cur.execute( sql_query, sql_data )
			old_email = cur.fetchone()

			if old_email:
				errs.append("Email already exists.")

			else:
				sql_query = "INSERT INTO users (email, password, username) VALUES (%s, %s, %s) RETURNING userid;"
				sql_data = ( email, hashed_pw, username )

				cur.execute( sql_query, sql_data )
				userid = cur.fetchone()[0]

				# sql_query = "INSERT INTO email_confirmation (userid, token) VALUES (%s, %s);"
				# sql_data = (userid, token)

				# cur.execute( sql_query, sql_data )

				conn.commit()
				cur.close()

		except db.psycopg2.DatabaseError, e:
			# if I have a connection
			print e
			if conn:
				conn.rollback()

		return redirect("/welcome/")