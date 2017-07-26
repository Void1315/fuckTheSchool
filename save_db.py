import pymysql.cursors
dict_config = {
	'host':'127.0.0.1',
	'user':'root',
	'passwd':'wqld1315',
	'db':'db_students'
}

class NewDB():
	"""docstring for NewDB"""
	def __init__(self, config):
		if not isinstance(config,dict):
			print("the '"+config+"'not dict!")
			return 0
		self.connection = pymysql.connect(**config)
		
	def create_date(self,tuple_):
		print('创建------------')
		cur = self.connection.cursor()
		reCount = cur.execute("INSERT INTO fractions(num_id,semester,content) VALUES (%s,%s,%s) ",tuple_)
		self.connection.commit()

	def get_student(self):
		cur = self.connection.cursor()
		sql = 'SELECT stu_num,passwd FROM students'
		reCount = cur.execute(sql)
		results = cur.fetchall()
		return results


	def in_dbSet(self,the_primerVal):
		'''
		通过学号看看是否有此人
		'''
		cur = self.connection.cursor()
		# print(the_primerVal)
		reCount = cur.execute(" SELECT COUNT(*) from fractions  where num_id = %s ",str(the_primerVal))
		the_sum = cur.fetchone()
		if the_sum[0]>0:
			return True
		else:
			return False


	def is_dbSetVal(self,the_tulpe):
		'''
		如果数据库存在这条学生成绩
		则更新
		'''
		cur = self.connection.cursor()
		effect_row = cur.execute(" UPDATE fractions SET content = %s WHERE num_id = %s AND content  <> %s ",(the_tulpe[2],str(the_tulpe[0]),the_tulpe[2]))
		if effect_row>0:
			print('写入数据库')
		else:
			print('存在这条数据')
			
	def save_info(self,*the_list):
		# print(the_list)
		if not self.in_dbSet(the_list[0]):
			self.create_date(the_list)
		else:
			self.is_dbSetVal(the_list)

if __name__ == '__main__':
	my_db = NewDB(dict_config)
	my_db.is_dbSetVal(the_table='fractions',the_primerVal='1',the_word='num_id',the_wordVal=2016010301)