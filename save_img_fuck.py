from clear_img import ReadImage
import requests
from PIL import Image, ImageFilter
import pytesseract
import http.cookiejar
import urllib.request as urllib2
import http.cookies
import urllib.request
import  urllib.parse
from bs4 import BeautifulSoup as soup
import time
from save_db import NewDB as MyDB
from get_info_me import GetInfo


dict_config = {
    'host':'127.0.0.1',
    'user':'root',
    'passwd':'wqld1315',
    'db':'db_students'
}


class Login(object):

    img_url = "http://59.69.173.117/jwweb/sys/ValidateCode.aspx"
    send_url = "http://59.69.173.117/jwweb/_data/index_LOGIN.aspx"
    logout_url = "http://59.69.173.117/jwweb/sys/Logout.aspx"
    path_info = "D:\yanzheng"
    filename = 'cookie.txt'
    userid = '2016010326'
    passwd = '721026'
    img_name = 'a.png'
    the_db = None
    code = 'xxxx'
    header = {
        'Cookie' : 'ASP.NET_SessionId=mwmesqyvvkqvpbfaafglfeby',
        'Host':'59.69.173.117',
        'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)'
    }

    postdata = {
        'UserID' : userid,
        'PassWord':passwd,
        'cCode':code,
        '__VIEWSTATE':'''dDwtMjM1NDY4NDcxO3Q8O2w8aTwxPjtpPDM+O2k8NT47aTw3Pjs+O2w8dDxwPGw8VGV4dDs+O2w85rKz5Y2X56eR5oqA5a2m6Zmi5paw56eR5a2m6ZmiOz4+Ozs+O3Q8cDxsPFRleHQ7PjtsPFw8c2NyaXB0IHR5cGU9InRleHQvamF2YXNjcmlwdCJcPgpcPCEtLQpmdW5jdGlvbiBDaGtWYWx1ZSgpewogdmFyIHZVPWRvY3VtZW50LmFsbC5VSUQuaW5uZXJUZXh0XDsKIHZVPXZVLnN1YnN0cmluZygwLDEpK3ZVLnN1YnN0cmluZygyLDMpXDsKIHZhciB2Y0ZsYWcgPSAiWUVTIlw7dHJ5ewogaWYgKGRvY3VtZW50LmFsbC5Vc2VySUQudmFsdWU9PScnKXsKIGFsZXJ0KCfpobvlvZXlhaUnK3ZVKyfvvIEnKVw7ZG9jdW1lbnQuYWxsLlVzZXJJRC5mb2N1cygpXDtyZXR1cm4gZmFsc2VcOwp9CiBlbHNlIGlmIChkb2N1bWVudC5hbGwuUGFzc1dvcmQudmFsdWU9PScnKXsKIGFsZXJ0KCfpobvlvZXlhaXlr4bnoIHvvIEnKVw7ZG9jdW1lbnQuYWxsLlBhc3NXb3JkLmZvY3VzKClcO3JldHVybiBmYWxzZVw7Cn0KIGVsc2UgaWYgKGRvY3VtZW50LmFsbC5jQ29kZS52YWx1ZT09JycgJiYgdmNGbGFnID09ICJZRVMiKXsKIGFsZXJ0KCfpobvlvZXlhaXpqozor4HnoIHvvIEnKVw7ZG9jdW1lbnQuYWxsLmNDb2RlLmZvY3VzKClcO3JldHVybiBmYWxzZVw7Cn0KIGVsc2UgeyBkb2N1bWVudC5hbGwuZGl2TG9nTm90ZS5pbm5lckhUTUw9J+ato+WcqOmAmui/h+i6q+S7vemqjOivgS4uLuivt+eojeWAmSEnXDsKIHJldHVybiB0cnVlXDt9Cn1jYXRjaChlKXt9Cn0KZnVuY3Rpb24gU2VsVHlwZShvYmopewogdmFyIHM9b2JqLm9wdGlvbnNbb2JqLnNlbGVjdGVkSW5kZXhdLnVzcklEXDsKIHZhciB3PW9iai5vcHRpb25zW29iai5zZWxlY3RlZEluZGV4XS5Qd2RJRFw7CiBkb2N1bWVudC5hbGwuVUlELmlubmVySFRNTD1zXDsKIHNlbFR5ZU5hbWUoKVw7Cn0KZnVuY3Rpb24gb3BlbldpbkxvZyh0aGVVUkwsdyxoKXsKdmFyIFRmb3JtLHJldFN0clw7CmV2YWwoIlRmb3JtPSd3aWR0aD0iK3crIixoZWlnaHQ9IitoKyIsc2Nyb2xsYmFycz1ubyxyZXNpemFibGU9bm8nIilcOwpwb3A9d2luZG93Lm9wZW4odGhlVVJMLCd3aW5LUFQnLFRmb3JtKVw7IC8vcG9wLm1vdmVUbygwLDc1KVw7CmV2YWwoIlRmb3JtPSdkaWFsb2dXaWR0aDoiK3crInB4XDtkaWFsb2dIZWlnaHQ6IitoKyJweFw7c3RhdHVzOm5vXDtzY3JvbGxiYXJzPW5vXDtoZWxwOm5vJyIpXDsKaWYodHlwZW9mKHJldFN0cikhPSd1bmRlZmluZWQnKSBhbGVydChyZXRTdHIpXDsKfQpmdW5jdGlvbiBzaG93TGF5KGRpdklkKXsKdmFyIG9iakRpdiA9IGV2YWwoZGl2SWQpXDsKaWYgKG9iakRpdi5zdHlsZS5kaXNwbGF5PT0ibm9uZSIpCntvYmpEaXYuc3R5bGUuZGlzcGxheT0iIlw7fQplbHNle29iakRpdi5zdHlsZS5kaXNwbGF5PSJub25lIlw7fQp9CmZ1bmN0aW9uIHNlbFR5ZU5hbWUoKXsKICBkb2N1bWVudC5hbGwudHlwZU5hbWUudmFsdWU9ZG9jdW1lbnQuYWxsLlNlbF9UeXBlLm9wdGlvbnNbZG9jdW1lbnQuYWxsLlNlbF9UeXBlLnNlbGVjdGVkSW5kZXhdLnRleHRcOwp9CmZ1bmN0aW9uIHdpbmRvdy5vbmxvYWQoKXsKCXZhciBzUEM9d2luZG93Lm5hdmlnYXRvci51c2VyQWdlbnQrd2luZG93Lm5hdmlnYXRvci5jcHVDbGFzcyt3aW5kb3cubmF2aWdhdG9yLmFwcE1pbm9yVmVyc2lvbisnIFNOOk5VTEwnXDsKdHJ5e2RvY3VtZW50LmFsbC5wY0luZm8udmFsdWU9c1BDXDt9Y2F0Y2goZXJyKXt9CnRyeXtkb2N1bWVudC5hbGwuVXNlcklELmZvY3VzKClcO31jYXRjaChlcnIpe30KdHJ5e2RvY3VtZW50LmFsbC50eXBlTmFtZS52YWx1ZT1kb2N1bWVudC5hbGwuU2VsX1R5cGUub3B0aW9uc1tkb2N1bWVudC5hbGwuU2VsX1R5cGUuc2VsZWN0ZWRJbmRleF0udGV4dFw7fWNhdGNoKGVycil7fQp9CmZ1bmN0aW9uIG9wZW5XaW5EaWFsb2codXJsLHNjcix3LGgpCnsKdmFyIFRmb3JtXDsKZXZhbCgiVGZvcm09J2RpYWxvZ1dpZHRoOiIrdysicHhcO2RpYWxvZ0hlaWdodDoiK2grInB4XDtzdGF0dXM6IitzY3IrIlw7c2Nyb2xsYmFycz1ub1w7aGVscDpubyciKVw7CndpbmRvdy5zaG93TW9kYWxEaWFsb2codXJsLDEsVGZvcm0pXDsKfQpmdW5jdGlvbiBvcGVuV2luKHRoZVVSTCl7CnZhciBUZm9ybSx3LGhcOwp0cnl7Cgl3PXdpbmRvdy5zY3JlZW4ud2lkdGgtMTBcOwp9Y2F0Y2goZSl7fQp0cnl7Cmg9d2luZG93LnNjcmVlbi5oZWlnaHQtMzBcOwp9Y2F0Y2goZSl7fQp0cnl7ZXZhbCgiVGZvcm09J3dpZHRoPSIrdysiLGhlaWdodD0iK2grIixzY3JvbGxiYXJzPW5vLHN0YXR1cz1ubyxyZXNpemFibGU9eWVzJyIpXDsKcG9wPXBhcmVudC53aW5kb3cub3Blbih0aGVVUkwsJycsVGZvcm0pXDsKcG9wLm1vdmVUbygwLDApXDsKcGFyZW50Lm9wZW5lcj1udWxsXDsKcGFyZW50LmNsb3NlKClcO31jYXRjaChlKXt9Cn0KZnVuY3Rpb24gY2hhbmdlVmFsaWRhdGVDb2RlKE9iail7CnZhciBkdCA9IG5ldyBEYXRlKClcOwpPYmouc3JjPSIuLi9zeXMvVmFsaWRhdGVDb2RlLmFzcHg/dD0iK2R0LmdldE1pbGxpc2Vjb25kcygpXDsKfQpcXC0tXD4KXDwvc2NyaXB0XD47Pj47Oz47dDw7bDxpPDE+Oz47bDx0PDtsPGk8MD47PjtsPHQ8cDxsPFRleHQ7PjtsPFw8b3B0aW9uIHZhbHVlPSdTVFUnIHVzcklEPSflraYgIOWPtydcPuWtpueUn1w8L29wdGlvblw+Clw8b3B0aW9uIHZhbHVlPSdURUEnIHVzcklEPSflt6UgIOWPtydcPuaVmeW4iOaVmei+heS6uuWRmFw8L29wdGlvblw+Clw8b3B0aW9uIHZhbHVlPSdTWVMnIHVzcklEPSfluJAgIOWPtydcPueuoeeQhuS6uuWRmFw8L29wdGlvblw+Clw8b3B0aW9uIHZhbHVlPSdBRE0nIHVzcklEPSfluJAgIOWPtydcPumXqOaIt+e7tOaKpOWRmFw8L29wdGlvblw+Cjs+Pjs7Pjs+Pjs+Pjt0PHA8cDxsPFRleHQ7PjtsPOmqjOivgeeggemUmeivr++8gVw8YnJcPueZu+W9leWksei0pe+8gTs+Pjs+Ozs+Oz4+Oz6rUibqKcRWN8Z3yXCsXJF4LAAvYA==''',
        '__VIEWSTATEGENERATOR':'4B596BA9',
        'Sel_Type':'STU',
        'typeName':'%D1%A7%C9%FA',
        'pcInfo':'''Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)x860 SN:NULL'''
    }


    def __init__(self,the_list):
        self.setInfo(the_list)
        

    def getInfo(self):
        the_info = GetInfo()
        return (the_info.getInfo(self.header))

    def test_user(self,html):
        doc = soup(html)
        if doc.select('#divLogNote')[0].string == '正在加载权限数据...':
            print('登陆成功！！！！')
            try:
                the_date = self.getInfo()
                list_ = []
                list_.append(int(self.postdata['UserID']))
                list_.append('2016-2017第二学期')
                list_.append(str(the_date))
                self.the_db.create_date((list_))
            except Exception as e:
                print('未成功写入')
                self.logout()
                raise e
                

            return True
        if doc.select('#divLogNote')[0].string == '账号或密码不正确！请重新输入。':
            print('密码错误'+str(self.postdata['UserID']))
            return True
        else:
            print(doc.select('#divLogNote')[0].string)
            return False

    def save_cook(self):
        cookie = self.save_img()  # 保存图片
        self.header['Cookie'] = cookie

    def save_img(self):
        a = urllib.request.urlretrieve(self.img_url,self.img_name)
        cookie = a[1]['Set-Cookie'][0:-8]
        return cookie

    def the_send(self):
        self.postdata['cCode'] = self.code
        to_postdata = urllib.parse.urlencode(self.postdata).encode()
        req = urllib2.Request(self.send_url,data=to_postdata,headers=self.header)
        result = urllib2.urlopen(req)
        return (self.test_user(result.read().decode('gb2312')))

    def setInfo(self,the_list):
        self.postdata['UserID'] = the_list[0]
        self.postdata['PassWord'] = the_list[1]
    
    def set_code(self,code):
        self.code = code

    def logout(self):
        req = urllib2.Request(self.logout_url,headers=self.header)
        result = urllib2.urlopen(req)
        print("成功退出")



my_db = MyDB(dict_config)#数据库连接


the_list_info = my_db.get_student()

for i in the_list_info:
    the_obj = Login(list(i))
    the_obj.the_db = my_db
    the_obj.save_cook()#保存cookie 还保存图片 

    img_obj = ReadImage(Image.open(the_obj.img_name))#传给 读取类

    code = img_obj.get_code()#返回验证码

    the_obj.set_code(code)#设置验证码

    while not the_obj.the_send():
        print("验证码失败...正在重试")
        time.sleep(1)
        the_obj.save_cook()#保存cookie 还保存图片 
        img_obj = ReadImage(Image.open(the_obj.img_name))#传给 读取类
        code = img_obj.get_code()#返回验证码
        the_obj.set_code(code)#设置验证码



