import requests
from lxml import etree
import json
#import csv

def getOnepage(n):
	url = r'https://vip.open.163.com/courses/?firstId=-1&source=pcphp_subView_more&page={}'.format(n)
	
	header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'}
	
	r = requests.get(url, headers = header, verify = False)
	r.encoding = 'utf-8'
	
	return r.text
	
def parse(text):	
	
	html = etree.HTML(text)
	
	names = html.xpath('/html/body/div[1]/div/div[3]/div[3]/div[2]/a/div[2]/div[1]/div[1]/text()')
	costs1 = html.xpath('/html/body/div[1]/div/div[3]/div[3]/div[2]/a/div[2]/div[2]/text()')
	
	costs = []
	for cost in costs1:
		cost = cost.strip('\n        ')
		costs.append(cost)
	
	items = {}
	
	for name,cost in zip(names,costs):
		items['Name'] = name
		items['Cost'] = cost
		yield items
				

def save2json(item):
	with open('163classes.json','a',encoding='utf-8') as f:
		item = json.dumps(item,ensure_ascii=False) + '\n'
		f.write(item)

def run():
	text = getOnepage(1)
	items = parse(text)
	for i in items:
		print(i)
		save2json(i)
		
run()

