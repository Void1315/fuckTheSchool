from PIL import Image, ImageFilter
import pytesseract
import time
import os
from hongshui import HongShui

class ReadImage(object):

	threshold = 195
	def __init__(self, img):
		self.img = img

	def get_bin_table(self,):
	    
	    table  =  []
	    for  i  in  range( 256 ):
	        if  i  <  self.threshold:
	            table.append(0)
	        else:
	            table.append(255)
	    return table#获得二值化 数组 用于初始化 黑白图

	def left_zone(self,img, x, y):
	    sum = img.getpixel((x + 1, y)) + \
	          img.getpixel((x + 1, y + 1)) + \
	          img.getpixel((x + 1, y - 1)) + \
	          img.getpixel((x, y + 1)) + \
	          img.getpixel((x, y - 1))
	    if sum >= 1020:
	        return 255
	    else:
	        return 0#左边界

	def right_zone(self,img, x, y):
	    sum = img.getpixel((x - 1, y)) + \
	          img.getpixel((x - 1, y + 1)) + \
	          img.getpixel((x - 1, y - 1)) + \
	          img.getpixel((x, y + 1)) + \
	          img.getpixel((x, y - 1))
	    if sum >= 1020:
	        return 255
	    else:
	        return 0#右边界

	def up_zone(self,img, x, y):
	    sum = img.getpixel((x - 1, y)) + \
	          img.getpixel((x + 1, y)) + \
	          img.getpixel((x - 1, y + 1)) + \
	          img.getpixel((x, y + 1)) + \
	          img.getpixel((x + 1, y + 1))
	    if sum >= 1020:
	        return 255
	    else:
	        return 0#上方边界

	def down_zone(self,img, x, y):#下方边界
	    sum = img.getpixel((x - 1, y)) + \
	          img.getpixel((x + 1, y)) + \
	          img.getpixel((x - 1, y - 1)) + \
	          img.getpixel((x, y - 1)) + \
	          img.getpixel((x + 1, y - 1))
	    if sum >= 1020:
	        return 255
	    else:
	        return 0

	def min_zone(self,img, x, y):
	    sum = img.getpixel((x - 1, y + 1)) + \
	          img.getpixel((x - 1, y)) + \
	          img.getpixel((x - 1, y - 1)) + \
	          img.getpixel((x, y + 1)) + \
	          img.getpixel((x, y - 1)) + \
	          img.getpixel((x + 1, y + 1)) + \
	          img.getpixel((x + 1, y)) + \
	          img.getpixel((x + 1, y - 1))
	    if sum >= (255 * 6):
	        return 255
	    else:
	        return 0#中间区域

	def remove_noise(self,img, x, y):
	    cur_pixel = img.getpixel((x, y))
	    width = img.width
	    height = img.height
	    if cur_pixel == 255:
	        return 255
	    else:
	        if x == 0:
	            if y == 0 or y == height:
	                return 255
	            else:
	                return self.left_zone(img, x, y)
	        if x == width:
	            if y == 0 or y == height:
	                return 255
	            else:
	                return self.right_zone(img, x, y)
	        if y == 0:
	            if x == 0 or x == width:
	                return 255
	            else:
	                return self.up_zone(img, x, y)
	        if y == height:
	            if x == 0 or x == width:
	                return 255
	            else:
	                return self.down_zone(img, x, y)

	        return self.min_zone(img, x, y)#移除噪点

	def list_set_img(self,list_img, img_):
	    w, h = img_.size
	    i = 0
	    for x in range(w):
	        for y in range(h):
	            if list_img[i] == None:
	                list_img[i] = 0
	            img_.putpixel((x, y), list_img[i])
	            i = i + 1
	    return img_


	def clear_img(self,img):
	    w,h = img.size
	    list_img = []
	    for x in range(w):
	        for y in range(h):
	            list_img.append(self.remove_noise(img, x, y))
	    return list_img

	def read_img(self,img_):
	    code = pytesseract.image_to_string(img_)
	    return code

	def to_black(self,img):
	    img = img.convert('L')
	    table = self.get_bin_table()
	    img_ = img.point(table, '1')
	    return img_

	def return_code(self):
	    list_img = []
	    img = self.img
	    img = self.to_black(img)
	    list_img = self.clear_img(img)
	    return self.read_img(self.list_set_img(list_img,img))

	def no_novce(self,img):
		'''
		移除噪点
		'''
		list_img =[]
		img = self.img
		img = self.to_black(img)
		list_img = self.clear_img(img)
		img = self.list_set_img(list_img,img)
		return img
		
	def getSVMCode(self):
		'''
			获得SVM验证码
		'''
		the_obj = HongShui()
		img = self.to_black(self.img)
		list_img = self.clear_img(img)
		img = self.list_set_img(list_img,img)
		return the_obj.splitImg(img)
	def get_code(self):
		'''
		外部获取验证码
		'''
		return self.return_code()