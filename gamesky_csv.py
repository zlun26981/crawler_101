import requests
from lxml import etree
import json
import csv

def getOnepage(page):
	url = r'https://down.gamersky.com/page/pc/0-0-0-0-0-0-0-00_{}.html'.format(page)
	
	header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'}
	
	response = requests.get(url, headers = header, verify = False)
	
	return response.text

def parse(text):
	
	html = etree.HTML(text)
	
	names = html.xpath('/html/body/div/ul/li/div[2]/a/@title')
	sizes = html.xpath('/html/body/div/ul/li/div[7]/text()')
	dates = html.xpath('/html/body/div/ul/li/div[3]/text()')
	languages = html.xpath('/html/body/div/ul/li/div[5]/text()')
	
	names = [i[:-2] for i in names]
	sizes = [i[5:] for i in sizes]
	dates = [i[5:] for i in dates]
	languages = [i[5:] for i in languages]
	
	items = {}
	
	for name,size,date,language in zip(names,sizes,dates,languages):
		items['Name'] = name
		items['Size'] = size
		items['Date'] =date
		items['Language'] = language
		yield items
		

def save2file(item):	
	with open('gamersky.json','a',encoding = 'utf-8') as f:
		item = json.dumps(item,ensure_ascii=False) + '\n'
		f.write(item)

def run_json_log():
	for i in range(0,347):
		text = getOnepage(i)
		items = parse(text)
		for j in items:
			print(j)
			save2file(j)

def addCSVheader():
	with open('gamersky.csv','a',encoding = 'utf_8_sig',newline = '') as f:
		columnnames = ['Name','Size','Date','Language']
		writer = csv.DictWriter(f,fieldnames = columnnames)
		writer.writeheader()

def addCSVrow(item):
	with open('gamersky.csv','a',encoding = 'utf_8_sig',newline = '') as f:
		columnnames = ['Name','Size','Date','Language']
		writer = csv.DictWriter(f, fieldnames = columnnames)
		writer.writerow({'Name':item['Name'],'Size':item['Size'],'Date':item['Date'],'Language':item['Language']})

def run_csv_log():
	addCSVheader()
	page = 0
	for i in range(347):
		text = getOnepage(i)
		items = parse(text)
		page = page + 1
		print('Page:',page)
		for j in items:
			print(j)
			addCSVrow(j)

run_csv_log()			