import psycopg2.extras
import db

def get( userid=None ):

	payload = []

	try:
		conn = db.get_db()
		cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

		sql_query = """SELECT 
				* 
			FROM 
				message
			WHERE 
				subject = %s
			ORDER BY 
				created DESC;
		"""

		sql_data = (userid, )
		cur.execute( sql_query, sql_data )
		payload = cur.fetchall()

		cur.close()

	except Exception, e:
		print e
		payload = []

	return payload

def send( subject=None, author=None, message=None ):

	if subject == None or author == None or message == None:
		return False

	try:

		# Open a cursor to perform database operations
		conn = db.get_db()
		cur = conn.cursor()

		sql_query = "INSERT INTO message (subject, author, message) VALUES (%s, %s, %s);"
		sql_data = ( subject, author, message )

		cur.execute( sql_query, sql_data )

		conn.commit()
		cur.close()

	except db.psycopg2.DatabaseError, e:
		# if I have a connection
		print e

		if conn:
			conn.rollback()

		return False

	return True