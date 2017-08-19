import socket

class LinkService():
	"""docstring for LinkService
	本地连接远程 不断传输数据
	"""
	address = '101.201.71.119'
	prot = 8888
	socket = None
	connect = None
	socket = None
	myLinkData = 'wtmsb'

	def __init__(self):
		self.socket = socket.socket()
		self.connect = self.socket.connect((self.address,self.prot))
		self.sendIsMyLink()

	def sendIsMyLink(self):
		self.socket.sendall(self.myLinkData.encode('utf-8'))
	def witeData(self):
		'''
		等待服务端给我传输数据,并返回
		'''
		str_ = self.socket.recv(1024)
		while sum(str_) == 0:
			str_ = self.socket.recv(1024)
		return str_.decode()
	def sendReturn(self,str_):
		self.socket.sendall(str_.encode('utf-8'))
