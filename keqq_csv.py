import requests
from lxml import etree
import json
import csv

def getOnepage(page):
	
	url = r'https://ke.qq.com/course/list?mt=1001&st=2002&task_filter=0000000&&page={}'.format(page)
	
	header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'}
	
	r = requests.get(url, headers = header, verify = False)
	r.encoding = 'utf-8'
	
	return r.text

def parse(text):
	
	html = etree.HTML(text)
	
	names = html.xpath('//section[1]/div/div[3]/ul/li/h4/a/@title')
	costs = html.xpath('//section[1]/div/div[3]/ul/li/div[3]/span/text()')
	providers = html.xpath('//section[1]/div/div[3]/ul/li/div[2]/span[2]/a/@title')
	
	items = {}
	
	for a,b,c in zip(names,costs,providers):
		items['Name'] = a
		items['Cost'] = b
		items['Provider'] = c
		yield items
'''
def save2file(item):
	with open('qqclass.json','a', encoding = 'utf-8') as f:
		item = json.dumps(item,ensure_ascii = False) + '\n'
		f.write(item)
'''		

def AddCSV_Header():
	with open('qqclass.csv','a',newline = '', encoding = 'utf_8_sig') as f:
		columnnames = ['Class_Name','Price','Provider']
		writer = csv.DictWriter(f,fieldnames = columnnames)
		writer.writeheader()

def AddCSV_Content(j):
	with open('qqclass.csv','a',newline = '', encoding = 'utf_8_sig') as f:
		columnnames = ['Class_Name','Price','Provider']
		writer = csv.DictWriter(f,fieldnames = columnnames)
		writer.writerow({'Class_Name':j['Name'],'Price':j['Cost'],'Provider':j['Provider']})
		
def run():
	AddCSV_Header()
	
	for page in range(1,35):
		text = getOnepage(page)
		items = parse(text)
		for j in items:
			print(j)
			AddCSV_Content(j)

run()

