import json
import requests
from lxml import etree

def getOnepage(n):
	if n == 1:
		url = 'http://www.metvb.com/list/2.html'
	else:
		url = 'http://www.metvb.com/list/2_{}.html'.format(n)
	
	header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'}
	
	r = requests.get(url, headers = header)
	r.encoding = 'utf-8'
	#将返回结果用utf-8编码，否则会出现乱码
	
	return r.text

#print(getOnepage(1))

def parse(text):
	
	html = etree.HTML(text)

	names = html.xpath('//div[@class="text"]/p[@class="name"]/text()')
	
#	print(names)
	
	actors = html.xpath('//div[@class="text"]/p[@class="zy"]/text()')

#	print(actors)

#parse(getOnepage(1))
#for testing	
	item = {}
	
	for i,j in zip(names,actors):
		item['name'] = i
		item['actor'] = j
		yield item

def save2file(data):
	with open('metvb.json','a', encoding = 'utf-8') as f:
		data = json.dumps(data, ensure_ascii=False) + ',\n'
		f.write(data)
		
def run():
	
	for n in range(1,98):
		text = getOnepage(n)
		items = parse(text)
		
		for item in items:
			print(item)
			save2file(item)

run()