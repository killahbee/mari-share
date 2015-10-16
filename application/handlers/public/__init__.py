from flask import g
from flask import Flask
from flask import escape
from flask import request
from flask import session
from flask import jsonify
from flask import url_for
from flask import redirect
from flask import send_file
from flask import render_template

from flask.ext.bcrypt import Bcrypt

import psycopg2.extras

import application
import db
import application.tools as tools

@application.app.route("/", methods=["GET"])
def main():
	
	return render_template("public/front_page.html")

@application.app.route("/login/", methods=["GET", "POST"])
def login():

	if request.method == "GET":

		next_redirect = request.args.get("next", False)

		return render_template("public/login.html",
			next=next_redirect)

	else:

		errs = []

		password = request.form.get("password", "")
		email = request.form.get("email", "")
		next = request.form.get("next", "")

		try:
			bc = Bcrypt(None)
			conn = db.get_db()

			sql_query = "SELECT * FROM users WHERE email = %s;"
			sql_data = (escape(email), )

			cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
			cur.execute( sql_query, sql_data )
			user = cur.fetchone()
			cur.close()

			if user == None:
				errs.append("No User Found.")

			else:

				if bc.check_password_hash(user["password"], password):

					# add user to the session
					tools.setCookie( email, user["username"], user["userid"] )

					# return the errors and redirect path
					redirect_url = "/welcome/"

					if next:
						redirect_url = next

					return redirect("/welcome/")

				else:
					print "bad pass"
					errs.append("Incorrect Password.")

		except Exception, e:
			print e
			errs.append("Unable to sign in at this time.")

		return render_template("public/login.html",
			next=next,
			errors=errs,
			email=email)

@application.app.route("/signup/", methods=["POST"])
def signup():
	
	if request.method == "POST":

		email = request.form.get("email", "")
		username = request.form.get("username", "")
		password = request.form.get("password", "")

		try:
			bc = Bcrypt(None)
			hashed_pw = bc.generate_password_hash( password )

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

				tools.setCookie( email, username, userid )

		except db.psycopg2.DatabaseError, e:
			# if I have a connection
			print e
			if conn:
				conn.rollback()

		return redirect("/welcome/")

@application.app.route("/logout/")
def logout():
	
	session.clear()
	return redirect("/")