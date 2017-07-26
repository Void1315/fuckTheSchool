from PIL import Image, ImageFilter
from svmutil import *
from svm import *
import os
import shutil
# import thread
class SVMImage():
	"""docstring for SVMImage
		特征化图片+机器学习+机器识别
	"""
	file_model = "data_svm/model.txt"
	file_test = "data_svm/test.txt"
	def __init__(self,img):
		self.img = img
		self.list_date = self.set_feature()
		self.svmDate = self.getSvmDate()

	def set_feature(self):#特征化
		h,w = self.img.size
		pix_cnt_x = 0
		pix_cnt_y = 0
		pixel_cnt_list = []
		for x in range(w):
			for y in range(h):
				if self.img.getpixel((x, y)) == 0:  # 黑色点
					pix_cnt_x += 1
			pixel_cnt_list.append(pix_cnt_x)
		for y in range(h):
			for x in range(w):
				if self.img.getpixel((x, y)) == 0:
					pix_cnt_y += 1
			pixel_cnt_list.append(pix_cnt_y)
		return pixel_cnt_list

	def getStrDate(self,label=0):
		list_date = self.list_date
		list_date = {index+1:i for index,i in enumerate(list_date)}
		str_date = str(label)+" "+str(list_date)[1:-1].replace(" ",'').replace(","," ")+"\n"
		return str_date
	def getSvmDate(self):
		list_date = self.list_date
		svmDate = {index+1:i for index,i in enumerate(list_date)}
		return svmDate
		

	def svmDateSave(self,str_date):
		file_p = open(self.file_model,'a')
		file_p.writelines(str_date)
		print("写入成功")
		file_p.close()

	def getSvmCode(self):
		pass


	def testDate(self):
		test_date = [self.svmDate]
		label = [5]
		y,x = svm_read_problem(self.file_model)
		param = svm_parameter('-t 1 -b 1 -q')
		model = svm_problem(y, x)
		model = svm_train(model,param)
		p_label, p_acc, p_val = svm_predict(label,test_date,model)
		if p_label[0]>9.0:
			return chr(int(p_label[0]))
		else:
			return p_label[0]

if __name__ == '__main__':

	def move_put():#从分割素材到 模板临时文件夹
		the_path = "split_img/"
		move_path = "move_put/"
		for root,dirs,files in os.walk(the_path):
			for the_name in files:
				img = Image.open(the_path+the_name)
				the_obj = SVMImage(img)
				code = the_obj.testDate()
				code = str(code)[:1]
				shutil.move(the_path+the_name,"move_put/"+code+"/")
				print("移动成功"+code)
	# move_put()

	def put_in_sucai():#模板临时文件夹 存入 训练数据 到 素材文件夹
		for i in range(0,10):
			# file_ = chr(i)
			file_ = str(i)
			the_path = "move_put/"+file_+"/"
			# the_path = "sucai/"+file_+"/"
			for root,dirs,files in os.walk(the_path):
				for the_name in files:
					img = Image.open(the_path+the_name)
					the_obj = SVMImage(img)
					str_date = the_obj.getStrDate(label=i)
					the_obj.svmDateSave(str_date)
					shutil.move(the_path+the_name,"sucai/"+file_+"/")
	# put_in_sucai()