import psycopg2.extras
import db

def get( userid ):

	try:
		conn = db.get_db()

		sql_query = "SELECT * FROM users WHERE userid = %s;"
		sql_data = (userid, )

		cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		cur.execute( sql_query, sql_data )
		user = cur.fetchone()
		cur.close()

	except Exception, e:
		print e
		user = {}

	return user