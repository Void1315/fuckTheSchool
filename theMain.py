from save_img_fuck import Login
from save_db import NewDB as MyDB
from linkService import LinkService
from clear_img import ReadImage
import _thread



class TheMain(object):
	"""docstring for TheMain"""
	def __init__(self):
		my_db = MyDB(dict_config)#数据库连接
		the_link = LinkService()
		while 1:
			print('等待数据')
			print('获取数据'+str(stu_data))
			stu_data = the_link.witeData()
			try:
				_thread.start_new_thread(self.getRelut(stu_data))
				print('线程已启动-------')
			except:
				print ("Error: 无法启动线程")
			
			
	def getRelut(stu_data):
		'''
		获取结果线程
		'''
		list_data = stu_data.split(',')
		the_obj = Login(list_data)
		the_obj.the_link = the_link
		the_obj.the_db = my_db
		the_obj.save_img()#保存回话 还保存图片 
		img_obj = ReadImage(Image.open(the_obj.img_name))#传给 读取类
		# code = img_obj.get_code()#返回验证码
		code = img_obj.get_code()#返回验证码
		the_obj.set_code(code)#设置验证码
		# Image.open(the_obj.img_name).show()
		# print(code+"-----------")
		while not the_obj.the_send():
			# print("验证码失败...正在重试")
			time.sleep(1)
			the_obj.save_img()#保存cookie 还保存图片 
			img_obj = ReadImage(Image.open(the_obj.img_name))#传给 读取类
			# code = img_obj.getSVMCode()#返回验证码
			code = img_obj.get_code()#返回验证码
			the_obj.set_code(code)#设置验证码
if __name__ == '__main__':
	TheMain()
	while 1:
		pass

