import urllib.request
import  urllib.parse
import requests
import urllib.request as urllib2
from bs4 import BeautifulSoup as soup
from pyquery import PyQuery as pq
import re
import json
dict_config = {
	'host':'127.0.0.1',
	'user':'root',
	'passwd':'wqld1315',
	'db':'db_students'
}
class GetInfo(object):
	url = 'http://59.69.173.117/jwweb/xscj/Stu_MyScore_rpt.aspx'
	get_url = 'http://59.69.173.117/jwweb/xscj/Stu_MyScore.aspx'
	th_ = ['学年学期','课程环节','学分','类别','考核方式','修读性质','成绩','取得学分','绩点','学分绩点','备注']
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
		tag = doc.find_all(name='input',value=re.compile(r'^20\d{10}'))
		pattern = re.compile(r'20\d{10}')
		self.the_postdata['txt_xm'] = str(pattern.search(str(tag)).group(0))

	def get_doc(self,the_seed,url):
		result = the_seed.post(url,data=self.the_postdata)
		doc = soup(result.text)
		return doc


	def get_table(self,doc):
		return doc.find('center')

	def get_json(self,doc):
		list_ ={}
		json_list = {}
		doc = pq(doc.prettify())
		tb = doc('#ID_Table')
		tr_list = tb('tr')
		for i,tr in enumerate(tr_list.items()):
			for index,td in enumerate(tr('td').items()):
				list_[index] = td.text()
			json_list[i] = list_
		return json.dumps(json_list)
	def getInfo(self,the_seed):
		doc = self.get_doc(the_seed,self.get_url)
		self.get_txt_xm(doc)

		doc = self.get_doc(the_seed,self.url)
		self.get_json(doc)
		return (self.get_json(doc))
		# return (self.get_table(doc))
