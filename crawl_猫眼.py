import json
import requests
from lxml import etree

def getOnepage(n):

	url = 'http://maoyan.com/board/4?offset={}'.format((n-1)*10)
	#格式化输出，第一页的offset是00，后面每加一页，offset加10
	
	header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'}
	#定义头部，不指定头部会被网站识别成非法访问，请求被抛弃。可以在浏览器按F12,在network里面找'user-agent',直接复制

	r = requests.get(url,headers = header)
	#提交Get请求，并传入到变量r

	return r.text

print(getOnepage(1))
	
def parse(text):
	
	html = etree.HTML(text)
	#标准化，初始化
	
	names = html.xpath('//div[@class="movie-item-info"]/p[@class="name"]/a/@title')
	#提取信息，需要写xpath语法
	#names是列表，xpath返回列表
	
	releasetimes = html.xpath('//p[@class="releasetime"]/text()')
	
	item = {}
	
	for name, releasetime in zip(names,releasetimes):
	#拉链函数,在这里是用于合并关联输出
		
		item['name'] = name
		item['releasetime'] = releasetime
		
		yield item
		#生成器 可循环迭代,将item里面的‘name’和‘releasetime’抛回给循环外的空字典
		
def save2File(data):
	with open('movie.json','a', encoding='utf-8') as f:
		data = json.dumps(data, ensure_ascii=False) + '，\n'
		#将字典，列表转换成字符串，否则后面运行会报错(文本文件只能识别字符串？)。保证中文能正常输出。换行输出
		
		f.write(data)

		#保存数据
def run():
		
	for n in range(1,11):		
		text = getOnepage(n)
		items = parse(text)	

		for item in items:
			print(item)
			save2File(item)

if __name__ == '__main__':
#这个语句在本个脚本没有太大意义，一般是其他脚本引用此脚本的函数时使用
	run()