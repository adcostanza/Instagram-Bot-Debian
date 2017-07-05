import psycopg2

class pg:
	def __init__(self, dbname, user, pw):
		try:
			self.conn = psycopg2.connect("dbname='"+dbname+"' user='"+user+"' host='localhost' password='"+pw+"'")
			
			print('Connected to database')
		except:
			print("Could not connect")
	
	def createTable(self):
		try:
			cur = self.conn.cursor()
			cur.execute("""CREATE TABLE Posts (\
							id serial PRIMARY KEY,\
							link varchar,\
							_like integer,\
							_time timestamp DEFAULT now())""")
			cur.execute("""CREATE TABLE tags (\
							id serial PRIMARY KEY,\
							tag varchar,\
							_time timestamp DEFAULT now())""")
			self.conn.commit()
			print("Table created")
		except:
			print("Table not created")
	def HourlyLikes(self):
		cur = self.conn.cursor()
		cur.execute("""SELECT  *\
		FROM Posts\
		WHERE _time >= NOW() - '1 hour'::INTERVAL""")
		likes = cur.rowcount
		#print()
		self.conn.commit()
		return likes
	def addPost(self,link,like):
		
		cur = self.conn.cursor()
		cur.execute("""INSERT INTO Posts (link, _like) VALUES (%s, %s)""",(link,like))
		self.conn.commit()
		print("Inserted into posts", link)
	def addTag(self,tag):
		cur = self.conn.cursor()
		cur.execute("""SELECT * FROM tags WHERE tag='%s'""" % tag)
		print("Tag in database? :", cur.rowcount)
		if(cur.rowcount == 0):
			cur.execute("""INSERT INTO tags (tag) VALUES ('%s')"""%tag)
		else: 
			print(cur.fetchall())
			cur.execute("""DELETE FROM tags WHERE tag='%s'"""%tag)
			cur.execute("""INSERT INTO tags (tag) VALUES ('%s')"""%tag)
		self.conn.commit()
		print("Inserted into tags", tag)
	def getAllLinks(self):
		cur = self.conn.cursor()
		cur.execute("""SELECT link FROM Posts""")
		posts = cur.fetchall()
		self.conn.commit()
		#print(posts)
		return(posts)
	def getAllTagsTimes(self):
		cur = self.conn.cursor()
		cur.execute("""SELECT tag, _time FROM tags""")
		tags = cur.fetchall()
		self.conn.commit()
		return(tags)
	def getTagTime(self, tag):
		cur = self.conn.cursor()
		cur.execute("""SELECT _time FROM tags WHERE tag='%s'""" % tag)
		if(cur.rowcount > 0):
			times = cur.fetchall()
			times = times[0][0]
			return(times)
		else:
			return False
			