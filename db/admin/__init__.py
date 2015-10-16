import psycopg2.extras
import db

def addNeighborhood( name ):

	try:

		# Open a cursor to perform database operations
		conn = db.get_db()
		cur = conn.cursor()

		sql_query = "INSERT INTO neighborhood (name) VALUES (%s) RETURNING hoodid;"
		sql_data = ( name, )

		cur.execute( sql_query, sql_data )
		hoodid = cur.fetchone()[0]

		conn.commit()
		cur.close()

	except db.psycopg2.DatabaseError, e:
		# if I have a connection
		print e
		if conn:
			conn.rollback()

	return {
		"name"		: name,
		"hoodid"	: hoodid
	}