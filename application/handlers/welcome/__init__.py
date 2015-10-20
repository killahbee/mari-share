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

@app.route("/pictures/<userid>/", methods=["POST"])
def picture_uploader( userid=None ):

	MAX_IMAGE_COUNT = 15

	MAX_FILE_SIZE = 8 * 1024 * 1024 # Max size is 4MB
	errs = []
	redirect_url = False
	response_data = {}

	if "email" not in session:
		errs.append("No user")

	if houseid == None:
		errs.append("No houseid specified")

	if db.get_house_image_count( houseid ) > MAX_IMAGE_COUNT:
		return jsonify(errors = ["A house can't have more than " + str(MAX_IMAGE_COUNT) + " images"]), 400

	house = db.get_house( houseid )

	if house == None:
		errs.append("House not found")

	try:

		f = request.files["uploadfile"]

		if f and tools.allowed_file(f.filename):

			# determine the file size ( http://stackoverflow.com/questions/15772975/flask-get-the-size-of-request-files-object )
			blob = f.read()
			file_size = len(blob)

			if file_size > MAX_FILE_SIZE:
				errs.append("Exceeded max file size ( 8MB )")
				return jsonify(errors = ["Exceeded max file size ( 8MB )"]), 413

			filename = secure_filename(f.filename)
			filedata = psycopg2.Binary( blob )

			# write string ( blob ) to a buffer
			buff = cStringIO.StringIO()
			buff.write( blob )

			#seek back to the beginning so the whole thing will be read by PIL
			buff.seek(0)

			# read the image
			img = Image.open(buff)

			# get the image dimensions and format
			(im_width, im_height) = img.size
			im_format = img.format

			if len(errs) == 0:
				conn = db.get_db()
				cur = conn.cursor()

				sql_query = "INSERT INTO images (houseid, imagedata, width, height, mimetype) VALUES (%s, %s, %s, %s, %s) RETURNING imageid;"
				sql_data = ( houseid, filedata, im_width, im_height, im_format )

				cur.execute( sql_query, sql_data )
				imageid = cur.fetchone()[0]
				conn.commit()
				cur.close()

				response_data["imageid"] = imageid

			else:
				return jsonify(errors = errs), 400

		else:
			errs.append("Invalid file type")

	except db.psycopg2.DatabaseError, e:
		# if I have a connection
		if conn:
			conn.rollback()

		errs.append("Something went wrong in the database")

		print 'Error %s' % e

	except Exception, e:
		print e
		errs.append("Trouble parsing image")

	return jsonify(errors = errs, data = response_data), 200