#信息保存成json文本后，再读取，其格式不是字典而是字符串，本脚本用意在于将json文本内的字符串再转换回字典

import json

def Readjson():
	with open('kkw.json','r',encoding='utf-8') as f:
	#读取文件名为'kkw.json'的文本
		m_list = []
		#创建空列表
		for line in f:
			m_list.append(line[:-2])
			#去除换行符后将每行内容添加到空列表
		for i in m_list:
			i = json.loads(i)
			print(i['Name'])
			#打印'Name'对应的值
					
Readjson()			


