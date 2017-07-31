import pymysql.cursors
import time
dict_config = {
	'host':'127.0.0.1',
	'user':'root',
	'passwd':'wqld1315',
	'db':'db_fuckschool'
}

class NewDB():
	"""docstring for NewDB"""
	def __init__(self, config):
		if not isinstance(config,dict):
			print("the '"+config+"'not dict!")
			return 0
		self.connection = pymysql.connect(**config)
		
	def create_date(self,tuple_):
		'''
		创建成绩数据
		'''
		print('创建------------')
		cur = self.connection.cursor()
		the_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		reCount = cur.execute("INSERT INTO results(u_id,year,term,result,created_at,updated_at) VALUES (%s,%s,%s,%s,%s,%s) ",tuple_+(the_time,the_time))
		self.connection.commit()

	def get_student(self):
		'''
		获取学生
		'''
		cur = self.connection.cursor()
		sql = 'SELECT stu_num,stu_passwd FROM users'
		reCount = cur.execute(sql)
		results = cur.fetchall()
		return results

	def in_dbSet(self,the_primerVal):#
		'''
		通过学号看看是否有此人的这学期数据
		'''
		cur = self.connection.cursor()
		reCount = cur.execute(" SELECT COUNT(*) from results  where u_id = %s and year = %s and  term = %s ",tuple(the_primerVal))
		the_sum = cur.fetchone()
		if the_sum[0]>0:
			return True
		else:
			return False

	def is_dbSetVal(self,the_tulpe):#
		'''
		如果数据库存在这条学生成绩
		则更新
		'''
		cur = self.connection.cursor()
		'''
		学号学年学期结果
		'''
		sql = " UPDATE results SET result = %s,updated_at = %s WHERE u_id = %s and year = %s and term = %s AND result  <> %s "
		the_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		sql_tulpe = (the_tulpe[2],the_time)+tuple(the_tulpe)
		effect_row = cur.execute(sql,sql_tulpe)
		self.connection.commit()
		if effect_row>0:
			print('写入数据库')
		else:
			print('存在这条数据')
			
	def save_info(self,*the_list):
		if not self.in_dbSet(the_list[:-1]):
			self.create_date(the_list)
		else:
			self.is_dbSetVal(the_list)

if __name__ == '__main__':
	test_obj = NewDB(dict_config)
	# cur = test_obj.connection.cursor()
	# _time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	# reCount = cur.execute(" INSERT INTO results(u_id,time,result) VALUES (%s,%s,%s) ",('1',_time,'1'))
	# test_obj.connection.commit()
	# print(_time)