from flask import g
from flask import Flask
from flask import request
from flask import session
from flask import jsonify
from flask import url_for
from flask import redirect
from flask import send_file
from flask import make_response
from flask import render_template
from werkzeug import secure_filename
from flask import send_from_directory

import io
import cStringIO
import psycopg2.extras
from PIL import Image

import db
import application
import application.tools as tools

def allowed_file(filename):

	ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png", "gif", "svg"]

	return '.' in filename and \
		(filename.rsplit('.', 1)[1]).lower() in ALLOWED_EXTENSIONS

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

@application.app.route("/pictures/<userid>/")
@tools.authenticated
def view_profile_picture( user, userid ):

	image = db.user.picture( userid )

	if image:
		return send_file( io.BytesIO( image["imagedata"] ),
			attachment_filename=userid + '.jpg',
			mimetype=image["mimetype"])

	return send_from_directory(application.app.config["BASE_DIR"] + "/application/static/img/", "logo.jpg")

@application.app.route("/pictures/<userid>/", methods=["POST"])
@tools.authenticated
def picture_uploader( user, userid ):

	profile_size = 200

	MAX_FILE_SIZE = 4 * 1024 * 1024 # Max size is 4MB
	errs = []
	redirect_url = False
	response_data = {}

	try:

		original_image = db.user.picture( userid )

		if original_image:
			db.user.delete_picture( userid )

		f = request.files["uploadfile"]

		if f and allowed_file(f.filename):

			# determine the file size ( http://stackoverflow.com/questions/15772975/flask-get-the-size-of-request-files-object )
			blob = f.read()
			file_size = len(blob)

			if file_size > MAX_FILE_SIZE:
				errs.append("Exceeded max file size ( 4MB )")
				return jsonify(errors = ["Exceeded max file size ( 4MB )"]), 413

			filename = secure_filename(f.filename)

			# write string ( blob ) to a buffer
			buff = cStringIO.StringIO()
			buff.write( blob )

			#seek back to the beginning so the whole thing will be read by PIL
			buff.seek(0)

			# read the image
			img = Image.open(buff)

			# Get image date=a
			(im_width, im_height) = img.size
			im_format = img.format

			# set scale factor
			scale = 200.0 / min(im_width, im_height)

			# resize the image
			img = img.resize((int(scale * im_width), int(scale * im_height)), Image.ANTIALIAS)

			# get new dimensions
			(im_width, im_height) = img.size

			# get center
			xshift = int(max((im_width - 200)/2, 0))
			yshift = int(max((im_height - 200)/2, 0))

			# crop the image
			img = img.crop((0 + xshift, 0 + yshift, 200 + xshift, 200 + yshift))

			# store image in memory
			new_iobody = io.BytesIO()
			img.save(new_iobody, 'JPEG')

			# get the filedata for writing
			filedata = psycopg2.Binary( new_iobody.getvalue() )

			if len(errs) == 0:
				conn = db.get_db()
				cur = conn.cursor()

				sql_query = "INSERT INTO profile_images (userid, imagedata, mimetype) VALUES (%s, %s, %s);"
				sql_data = ( userid, filedata, im_format )

				cur.execute( sql_query, sql_data )
				conn.commit()
				cur.close()

			else:
				return jsonify(errors = errs), 400

		else:
			errs.append("Invalid file type")
			return jsonify(errors="Invalid file type"), 400

	except db.psycopg2.DatabaseError, e:
		# if I have a connection
		if conn:
			conn.rollback()

		return jsonify(errors="Something went wrong in the database"), 400

		print 'Error %s' % e

	except Exception, e:
		print e
		errs.append("Trouble parsing image")

	return jsonify(data = response_data), 200

@application.app.route("/cover/<userid>/")
@tools.authenticated
def view_cover_picture( user, userid ):

	image = db.user.cover( userid )

	if image:
		return send_file( io.BytesIO( image["imagedata"] ),
			attachment_filename=userid + '.jpg',
			mimetype=image["mimetype"])

	return send_from_directory(application.app.config["BASE_DIR"] + "/application/static/img/placeholders/", "cover-a.jpg")

@application.app.route("/cover/<userid>/", methods=["POST"])
@tools.authenticated
def cover_uploader( user, userid ):

	cover_size = (900, 300)

	errs = []
	response_data = {}

	try:

		original_image = db.user.cover( userid )

		if original_image:
			db.user.delete_cover( userid )

		f = request.files["uploadfile"]

		if f and allowed_file(f.filename):

			# determine the file size ( http://stackoverflow.com/questions/15772975/flask-get-the-size-of-request-files-object )
			blob = f.read()
			file_size = len(blob)

			filename = secure_filename(f.filename)

			# write string ( blob ) to a buffer
			buff = cStringIO.StringIO()
			buff.write( blob )

			#seek back to the beginning so the whole thing will be read by PIL
			buff.seek(0)

			# read the image
			img = Image.open(buff)

			# Get image data
			(im_width, im_height) = img.size
			im_format = img.format

			# start scaling the width
			if im_width < cover_size[0]:
				scale = cover_size[0] / im_width
				img = img.resize(( cover_size[0], int(scale * im_height)), Image.ANTIALIAS)

			# get new dimensions
			(im_width, im_height) = img.size

			# start scaling the height
			if im_height < cover_size[1]:
				scale = cover_size[1] / im_height
				img = img.resize(( int(scale * im_width), cover_size[1]), Image.ANTIALIAS)

			# get new dimensions
			(im_width, im_height) = img.size

			# get center
			xshift = int(max((im_width - cover_size[0])/2, 0))
			yshift = int(max((im_height - cover_size[1])/2, 0))

			# crop the image
			img = img.crop((0 + xshift, 0 + yshift, cover_size[0] + xshift, cover_size[1] + yshift))

			# store image in memory
			new_iobody = io.BytesIO()
			img.save(new_iobody, 'JPEG')

			# get the filedata for writing
			filedata = psycopg2.Binary( new_iobody.getvalue() )

			if len(errs) == 0:
				conn = db.get_db()
				cur = conn.cursor()

				sql_query = "INSERT INTO cover_image (userid, imagedata, mimetype) VALUES (%s, %s, %s);"
				sql_data = ( userid, filedata, im_format )

				cur.execute( sql_query, sql_data )
				conn.commit()
				cur.close()

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

	if errs:
		return jsonify(errors=errs), 400

	return jsonify(errors = errs, data = response_data), 200