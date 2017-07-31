import urllib.request
import  urllib.parse
import requests
import urllib.request as urllib2
from bs4 import BeautifulSoup as soup
from pyquery import PyQuery as pq
import re
import json
import sys
dict_config = {
	'host':'127.0.0.1',
	'user':'root',
	'passwd':'wqld1315',
	'db':'db_fuckschool'
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
	year_list = []
	index = 0

	def __init__(self,the_seed):
		self.the_seed = the_seed
		self.get_date()

	def get_date(self):
		doc = self.get_doc(self.get_url)#获得所需数据
		self.year_list = self.getAllYear(doc)#获得所有年份
		self.get_txt_xm(doc)#获得隐藏表单

	def get_txt_xm(self,doc):#获得哪一个人
		tag = doc.find_all(name='input',value=re.compile(r'^20\d{10}'))
		pattern = re.compile(r'20\d{10}')
		self.the_postdata['txt_xm'] = str(pattern.search(str(tag)).group(0))

	def get_doc(self,url):
		result = self.the_seed.post(url,data=self.the_postdata)
		doc = soup(result.text)
		return doc

	def getAllYear(self,doc):
		the_list = []
		doc = pq(doc.prettify())#转化为pq对象
		select = doc("select[name='sel_xn']")
		options = select('option')
		for option in options.items():
			the_list.append(option.attr("value"))
		return the_list

	def get_table(self,doc):
		return doc.find('center')

	def get_json(self,doc):
		json_list = {}
		doc = pq(doc.prettify())
		tb = doc('#ID_Table')
		if len(tb)==0:
			return False
		else:
			tr_list = tb('tr')
			for i,tr in enumerate(tr_list.items()):
				list_ ={}
				for index,td in enumerate(tr('td').items()):
					list_[index] = td.text()
				json_list[i] = list_
			return json.dumps(json_list)

	def getInfo(self):
		self.the_postdata['sel_xn'] = self.year_list[0]
		self.the_postdata['sel_xq'] = self.index
		year = self.year_list[0]
		doc = self.get_doc(self.url)#获得带有表格的doc
		i = self.index
		if self.index==1:
			self.index = 0#学期归位
			del self.year_list[0]#删除这个年份
		else:
			self.index +=1
		return (str(year),str(i),self.get_json(doc))