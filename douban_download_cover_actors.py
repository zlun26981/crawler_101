#爬取douban热门电影列表中的头n页电影，为每个电影创建以电影名为名称的文件夹，并在其中创建电影封面图片(以cover为文件名)以及创建actors文件夹，将演员图片(以演员名字作为文件名)放在actors文件夹内。
import requests
import os
from lxml import etree
import re


def mkdir(path):
#创建文件夹函数
	folder = os.path.exists(path)
	#检查文件夹是否已经存在
	if not folder:
		os.makedirs(path)
		print(path,'folder added!')
		#如果不存在则创建文件夹
	else:
		print(path,'folder already exisited!')


def GetPicnNamelist(page):
	url = r'https://movie.douban.com/j/search_subjects?type=movie&tag=热门&sort=recommend&page_limit=20&page_start={}'.format(page*20)
	#要爬取电影名和电影封面所在的页面
	
	header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'}
	
	response = requests.get(url,headers=header,verify=False)
	
	subjects = response.json()['subjects']
	#页面为json数据结构，电影名及封面信息都在subjects的各个项目下
	
	name_list = []	
	url_list = []
	
	for i in subjects:
		name_list.append(i['title'])
		url_list.append(i['url'])
		
	return zip(name_list,url_list)
	#返回结果将两个列表进行关联		
		
def GetPagePic(link):
	#从电影列表中获取具体电影的url
	url = link
	
	header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'}
	
	response = requests.get(url,headers=header,verify=False)
	return response.text

def Parse(text):
	html = etree.HTML(text)
	cover_pic = html.xpath('/html/body/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/a/img/@src')
	#电影封面所在位置
	actor_pics = html.xpath('/html/body/div[3]/div[1]/div[2]/div[1]/div[4]/ul/li/a/div/@style')
	#演员图片所在url(要修正后才能使用)
	actor_names = html.xpath('/html/body/div[3]/div[1]/div[2]/div[1]/div[4]/ul/li/div/span[1]/a/text()')
	#演员名字
	actor_pics = [i[22:-1] for i in actor_pics]
	#演员图片所在url修正
	movie_names = html.xpath('/html/body/div[3]/div[1]/h1/span[1]/text()')
	#电影名称
	
	items = {}
	for actor_pic,movie_name in zip(actor_pics,movie_names):
		items['AC_Names'] = actor_names
		items['Pic'] = actor_pics
		items['Cover'] = cover_pic[0]
		items['M_Name'] = movie_names[0]
		yield items
		#将上面收集的信息都生成字典

def SavePic(path,url):
	#创建保存图片函数，输入保存路径以及url
	pic_response = requests.get(url,verify=False)
	with open('{}{}'.format(path,'.jpg'),'wb') as f:
		f.write(pic_response.content)	

def validateTitle(title):
	#Windows对于文件名字符有要求，因此需要用此函数将非法字符转换成合法字符
	rstr = r"[\/\\\:\*\?\"\<\>\|]"  
	# '/ \ : * ? " < > |'
	new_title = re.sub(rstr, "_", title)
	# 替换为下划线
	return new_title
		
def run(page):
	ML = GetPicnNamelist(page)
	for M in ML:
	#列表中的信息进行迭代(具体电影资源的url)
		text = GetPagePic(M[1])
		#获取具体url
		items = Parse(text)
		#提取该url电影资源的内容(电影名，演员名（及图片url），封面)
		for item in items:
			validName = validateTitle(item['M_Name'])
			#电影名字符合法化
			mkdir(validName)
			#创建电影名文件夹
			path_movie = os.getcwd() + '\\' + validName
			#获取电影名文件夹位置
			mkdir(path_movie+'\\'+'actors')
			#在电影名文件夹下创建actors文件夹
			path_actors = path_movie+'\\'+'actors\\'
			#获取actors文件夹位置
			SavePic(path_movie+'\cover',item['Cover'])
			#将电影封面保存名为cover的图片，并存放在电影文件夹下
			print(path_movie+'\cover',item['Cover'])
			for name,actor_pic in zip(item['AC_Names'],item['Pic']):
				#print(path_actors+name,actor_pic)
				SavePic(path_actors+name,actor_pic)
				#将演员图片保存在actors文件夹下

run(2)