import psycopg2.extras
import db

def getNeighborhoods( id=None ):

	hoods = []

	try:

		# Open a cursor to perform database operations
		conn = db.get_db()
		cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

		sql_query = "SELECT * FROM neighborhood;"

		cur.execute( sql_query )
		hoods = cur.fetchall()

		cur.close()

	except db.psycopg2.DatabaseError, e:
		# if I have a connection
		print e

		if conn:
			conn.rollback()

	return hoods