import pymysql.cursors
dict_config = {
	'host':'127.0.0.1',
	'user':'root',
	'passwd':'wqld1315',
	'db':'db_students'
}

class NewDB(object):
	"""docstring for NewDB"""
	def __init__(self, config):
		if not isinstance(config,dict):
			print("the '"+config+"'not dict!")
			return 0
		self.connection = pymysql.connect(**config)
		
	def create_date(self,the_list):
		cur = self.connection.cursor()
		reCount = cur.execute("INSERT INTO fractions(num_id,semester,content) VALUES (%s,%s,%s) ",the_list)
		self.connection.commit()

	def get_student(self):
		cur = self.connection.cursor()
		sql = 'SELECT stu_num,passwd FROM students'
		reCount = cur.execute(sql)
		results = cur.fetchall()
		# print(result)
		return results
# the_db = NewDB(dict_config)
# list_ = (1,1,1)
# the_db.create_date(list_)