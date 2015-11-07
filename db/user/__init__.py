import psycopg2.extras
import db

def get( userid=None, cols="*" ):

	try:
		conn = db.get_db()
		cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

		if userid:
			sql_query = "SELECT * FROM users WHERE username = %s;"
			sql_data = (userid, )
			cur.execute( sql_query, sql_data )
			payload = cur.fetchone()

			if payload == None:
				sql_query = "SELECT * FROM users WHERE userid = %s;"
				cur.execute( sql_query, sql_data )
				payload = cur.fetchone()

		else:
			sql_query = "SELECT * FROM users ORDER BY username ASC;"
			cur.execute( sql_query )
			payload = cur.fetchall()

		cur.close()

	except Exception, e:
		print e
		payload = {}

	return payload

def picture ( userid=None, cols="*" ):

	try:
		conn = db.get_db()
		cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

		sql_query = "SELECT * FROM profile_images WHERE userid = %s;"
		sql_data = (userid, )
		cur.execute( sql_query, sql_data )
		payload = cur.fetchone()

		cur.close()

	except Exception, e:
		print e
		payload = None

	return payload

def delete_picture ( userid ):

	try:
		conn = db.get_db()
		cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

		sql_query = "DELETE FROM profile_images WHERE userid = %s;"
		sql_data = (userid, )

		cur.execute( sql_query, sql_data )
		conn.commit()
		cur.close()

	except Exception, e:
		print e
		return False

	return True

def cover ( userid=None, cols="*" ):

	try:
		conn = db.get_db()
		cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

		sql_query = "SELECT * FROM cover_image WHERE userid = %s;"
		sql_data = (userid, )
		cur.execute( sql_query, sql_data )
		payload = cur.fetchone()

		cur.close()

	except Exception, e:
		print e
		payload = None

	return payload

def delete_cover ( userid ):

	try:
		conn = db.get_db()
		cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

		sql_query = "DELETE FROM cover_image WHERE userid = %s;"
		sql_data = (userid, )

		cur.execute( sql_query, sql_data )
		conn.commit()
		cur.close()

	except Exception, e:
		print e
		return False

	return True