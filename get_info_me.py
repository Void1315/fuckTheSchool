import urllib.request
import  urllib.parse
import requests
import urllib.request as urllib2
from bs4 import BeautifulSoup as soup
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
		
	def get_txt_xm(self,doc):#获得哪一个人
		tag = doc.find_all(name='input',value=re.compile(r'^201600\d{6}'))
		pattern = re.compile(r'201600\d{6}')
		self.the_postdata['txt_xm'] = str(pattern.search(str(tag)).group(0))

	def get_doc(self,the_seed,url):
		result = the_seed.post(url,data=self.the_postdata)
		doc = soup(result.text)
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

	def getInfo(self,the_seed):
		doc = self.get_doc(the_seed,self.get_url)
		self.get_txt_xm(doc)
		doc = self.get_doc(the_seed,self.url)
		return (self.get_table(doc))
