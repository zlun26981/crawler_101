import requests
from lxml import etree
import json
import csv

def GetPageResp(page):
	page_url = r'https://m.kankanwu.com/dy/index_{}_______1.html'.format(page)
	
	header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'}
	
	response = requests.get(url = page_url, headers = header, verify = False)
	
	response.encoding = 'utf-8'
	
	return response.text

def Parse(text):
	
	html = etree.HTML(text)
	
	names = html.xpath('/html/body/div[5]/div/ul/li/a/@title') 
	actors = html.xpath('/html/body/div[5]/div/ul/li/p/text()')
	links = html.xpath('/html/body/div[5]/div/ul/li/a/@href')
	definitions = html.xpath('/html/body/div[5]/div/ul/li/a/div/label[2]/text()')
	
	for i in range(len(actors)):
		actors[i] = actors[i][3:]
	
	for i in range(len(links)):
		links[i] = r'https://m.kankanwu.com'+links[i]
	
	items = {}
	
	for name,actor,link,definition in zip(names,actors,links,definitions):
		items['Name'] = name
		items['Actors'] = actor
		items['Definition'] = definition
		items['Link'] = link
		
		yield items

def Save2json(item):
	with open('kkw.json','a', encoding = 'utf-8') as f:
		item = json.dumps(item, ensure_ascii = False) + ',\n'
		f.write(item)
		
def Run_to_json():
	for i in range(1,5):
		text = GetPageResp(i)
		items = Parse(text)
		for j in items:
			print(j)
			Save2json(j)
		
Run_to_json()

def Save2csvHeader():
	with open('kkw.csv','a',newline = '',encoding = 'utf_8_sig') as f:
		columnnames = ['Name','Definition','Actors','Link']
		writer = csv.DictWriter(f,fieldnames = columnnames)
		writer.writeheader()

def Save2csvRow(j):
	with open('kkw.csv', 'a', newline='', encoding = 'utf_8_sig') as f:
		columnnames = ['Name','Definition','Actors','Link']
		writer = csv.DictWriter(f, fieldnames=columnnames)
		writer.writerow(dict(Name=j['Name'],Actors=j['Actors'],Definition=j['Definition'],Link=j['Link']))

def Run_to_csv():
	Save2csvHeader()
	for i in range(1,5):
		text = GetPageResp(i)
		items = Parse(text)
		for j in items:
			print(j)
			Save2csvRow(j)
		
#Run_to_csv()