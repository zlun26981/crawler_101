import requests
from lxml import etree
import json
import csv


def getOnepage(page):
	url = r'http://www.dianping.com/shanghai/ch10/p{}'.format(page)
	
	header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'}
	
	r = requests.get(url,headers = header)
	r.encoding = 'utf-8'
	
	return r.text

#print(getOnepage(1))

def parse(text):
	
	html = etree.HTML(text)
	
	resturant = html.xpath('/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/ul/li/div[2]/div[1]/a/@title')	

	recommended = html.xpath('/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/ul/li/div[2]/div[4]/a/text()')
	
	type = html.xpath('/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/ul/li/div[2]/div[3]/a[1]/span/text()')
	
	cost = html.xpath('/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/ul/li/div[2]/div[2]/a[2]/b/text()')
	
	addr = html.xpath('/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/ul/li/div[2]/div[3]/span/text()')
	
	items = {}
	
	for a,b,c,d,e in zip(resturant,recommended,type,cost,addr):
		items['Restaurant'] = a
		items['Recommended'] = b
		items['Type'] = c
		items['Cost'] = d
		items['addr'] = e
		
		yield items

#save2file()		

def save2csvheader():
	with open('dp.csv','a',newline = '',encoding = 'utf_8_sig') as f:
		columnnames = ['Restaurant','Recommended','Type','Cost','Address']
		writer = csv.DictWriter(f,fieldnames = columnnames)
		writer.writeheader()
		
def run():
	save2csvheader()
	
	for i in range(1,51):
		text = getOnepage(i)
		items = parse(text)
		for j in items:
			print(j)
			with open('dp.csv','a', newline = '', encoding = 'utf_8_sig') as f:
				#encoding = 'utf_8_sig'给csv文件加上utf-8 BOM头部，excel可自动识别其编码
				columnnames = ['Restaurant','Recommended','Type','Cost','Address']				
				writer = csv.DictWriter(f,fieldnames = columnnames)
				writer.writerow({'Restaurant':j['Restaurant'],'Recommended':j['Recommended'],'Type':j['Type'],'Cost':j['Cost'],'Address':j['addr']})

run()
