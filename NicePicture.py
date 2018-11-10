# -*- coding:utf-8 -*-
import requests
import os
import time
import threading
from bs4 import BeautifulSoup
def download_page(url):
	'''
	This function is used to download the url pages
	'''
	headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"}
	r = requests.get(url,headers = headers)
	r.encoding = 'gb2312'
	return r.text

def get_pic_list(html):
	'''
	This function is used to obtain the pics list in 
	each page,and then loop to call function get_pic to get the pics
	'''
	soup = BeautifulSoup(html, 'html.parser')
	pic_list = soup.find_all('li', class_ = 'wp-item')
	for i in pic_list:
		a_tag = i.find('h3', class_ = 'tit').find('a')
		link = a_tag.get('href')  #套图链接
		text = a_tag.get_text()  #套图名字
		get_pic(link, text)
		
def get_pic(link, text):
	'''
	get the pics in current page and store
	'''
	html = download_page(link) #下载页面
	soup = BeautifulSoup(html, 'html.parser')
	pic_list = soup.find('div', id = 'picture').find_all('img') #找到页面所有的图片
	headers = {"User_Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"}
	create_dir('pic/{}'.format(text))
	for i in pic_list:
		pic_link = i.get('src') #拿到图片的具体 url
		r = requests.get(pic_link, headers = headers) #下载图片之后，保存到文件
		with open('pic/{}/{}'.format(text,pic_link.split('/')[-1]),'wb') as f:  #将link改成了pic_link
			f.write(r.content)
			time.sleep(1) #设置延时，减少网站压力，避免被封
			
def create_dir(name):
	if not os.path.exists(name):
		os.makedirs(name)

def execute(url):
	page_html = download_page(url)
	get_pic_list(page_html)
	
def main():
	create_dir('pic')
	queue = [i for i in range(1,8)] #构造 url 链接页码
	threads = []
	while len(queue) > 0:
		for thread in threads:
			if not thread.is_alive():
				threads.remove(thread)
		while len(threads) < 5 and len(queue) > 0: #最大线程数设置为5(改了此循环的缩进)
			cur_page = queue.pop(0)
			url = 'http://meizitu.com/a/more_{}.html'.format(cur_page)
			thread = threading.Thread(target = execute,args = (url,))
			thread.setDaemon(True)
				
			thread.start()
			print('{} is downloading the {}th page'.format(threading.current_thread().name,cur_page))
			threads.append(thread)
				
if __name__ == '__main__':
	main()