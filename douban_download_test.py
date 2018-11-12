import requests

def GetPicnNamelist(page):
	url = r'https://movie.douban.com/j/search_subjects?type=movie&tag=热门&sort=recommend&page_limit=20&page_start={}'.format(page*20)
	#要爬取电影名和电影封面所在的页面
	
	header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'}
	
	response = requests.get(url,headers=header,verify=False)
	
	subjects = response.json()['subjects']
	#页面为json数据结构，电影名及封面信息都在subjects的各个项目下
	
	pic_list = []
	name_list = []	
	
	for i in subjects:
		pic_list.append(i['cover'])
		name_list.append(i['title'])
	
	return zip(pic_list,name_list)
	#返回结果将两个列表进行关联


def SavePic(item):
	url = item[0]
	pic_response = requests.get(url,verify=False)
	with open(r'C:\Users\zlun\Desktop\dou_pic\{}.jpg'.format(item[1]),'wb') as f:
		f.write(pic_response.content)
	

def run():
	for i in range(3):
		lists = GetPicnNamelist(i)
		for j in lists:
			print(j)
			SavePic(j)

run()


	
