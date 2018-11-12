#http://www.btbtt.net/forum-index-fid-951-page-1.htm

#http://www.btbtt.net/forum-index-fid-951-page-2727.htm

import json
import requests
from lxml import etree

def getOnepage(n):
	url = 'http://www.btbtt.net/forum-index-fid-951-page-{}.htm'.format(n)
	
	header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'}
	
	r = requests.get(url, headers=header)
	
	return r.text

#print(getOnepage(1))	

def parse(text):
	
	html = etree.HTML(text)
	
	names = html.xpath('//td[@class="subject"]/a/@title')
	
	views = html.xpath('//td[@class="views"]/span/text()')
	
	#print(names)
	#print(views)

#parse(getOnepage(1))
	item = {}
	
	for name,view in zip(names,views):
		item['name'] = name
		item['view'] = view
		yield item

def save2file(data):
		with open('BT_station.json','a',encoding = 'utf-8') as f:
			data = json.dumps(data, ensure_ascii=False)+ '\n'
			f.write(data)
			
def run():
	count = 0
	for i in range(1,2728):
		text = getOnepage(i)
		items = parse(text)
				
		for item in items:
			print(item)
			save2file(item)
		
		count = count + 1
		print('page',count)
run()