import urllib.request
import  urllib.parse
import requests
import urllib.request as urllib2
from bs4 import BeautifulSoup as soup
# from save_db import NewDB as MyDB
# import pymysql.cursors
import re
dict_config = {
	'host':'127.0.0.1',
	'user':'root',
	'passwd':'wqld1315',
	'db':'db_students'
}
class GetInfo(object):
	url = 'http://59.69.173.117/jwweb/xscj/Stu_MyScore_rpt.aspx'
	get_url = 'http://59.69.173.117/jwweb/xscj/Stu_MyScore.aspx'
	the_postdata = {
		'sel_xn':'2016',
		'sel_xq':'1',
		'SJ':'1',
		'btn_search':'%BC%EC%CB%F7',
		'SelXNXQ':'2',
		'txt_xm':'201600000906',
		'zfx_flag':'0'
	}
	info_content  = ''
	info_num = 0
	list_info = []

	# def __init__(self,config):
	# 	if isinstance(config,dict):
	# 		self.connection = pymysql.connect(**config)
	# 	else:
	# 		print('不是字典')
		
	def get_txt_xm(self,doc):#获得哪一个人
		tag = doc.find_all(name='input',value=re.compile(r'^201600\d{6}'))
		pattern = re.compile(r'201600\d{6}')
		self.the_postdata['txt_xm'] = str(pattern.search(str(tag)).group(0))

	def get_doc(self,head,url):
		postdata = urllib.parse.urlencode(self.the_postdata).encode()
		req = urllib2.Request(url,data=postdata,headers=head)
		result = urllib2.urlopen(req)
		doc = soup(result.read().decode('gb2312'))
		return doc

	def save_info(self):
		import saveImg as LinkUrl_
		the_db = db.NewDB(db.dict_config)
		for i in range(1,31):
			info_ = the_db.get_student(i)
			print(LinkUrl_.userid)
			LinkUrl_.userid = info_[0]
			LinkUrl_.passwd = info_[1]

	def get_table(self,doc):
		return doc.find('center')
		# print(doc.find('center'))

	def getInfo(self,head):
		doc = self.get_doc(head,self.get_url)
		self.get_txt_xm(doc)
		doc = self.get_doc(head,self.url)
		return (self.get_table(doc))




# my_db = MyDB(dict_config)
# the_stu = GetInfo()
# print(len(my_db.get_student()))






# url = 'http://59.69.173.117/jwweb/xscj/Stu_MyScore_rpt.aspx'
# the_postdata = {
# 	'sel_xn':'2016',
# 	'sel_xq':'1',
# 	'SJ':'1',
# 	'btn_search':'%BC%EC%CB%F7',
# 	'SelXNXQ':'2',
# 	'txt_xm':'201600000906',
# 	'zfx_flag':'0'
# }
# info_content  = ''
# info_num = 0
# list_info = []
# def get_stu_info(head,num):
# 	global info_content,info_num,list_info
# 	info_num = num
# 	postdata = urllib.parse.urlencode(the_postdata).encode()
# 	req = urllib2.Request(url,data=postdata,headers=head)
# 	result = urllib2.urlopen(req)
# 	doc = soup(result.read().decode('gb2312'))
# 	# print(doc.select('#ID_Table'))
# 	info_content = doc.select('#ID_Table')
# 	list_info.append(num)
# 	list_info.append('2016-2017学年第二学期')
# 	list_info.append(str(info_content[0]))
# 	# print(list_info)
# 	# save_info(tuple(list_info))

# def save_info():
# 	import saveImg as LinkUrl_
# 	the_db = db.NewDB(db.dict_config)
# 	for i in range(1,31):
# 		info_ = the_db.get_student(i)
# 		print(sys.path)
# 		print(LinkUrl_.userid)
# 		LinkUrl_.userid = info_[0]
# 		LinkUrl_.passwd = info_[1]
		# list_info = LinkUrl_.the_send()
		# the_db.create_date(list_info)
# save_info()