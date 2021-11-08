# -*- coding:utf-8 -*-
import urllib
from os.path import basename
from urllib.parse import urlparse
import re
import os
import requests
from bs4 import BeautifulSoup


def spider(base_url='', slt=''):
	source_code = requests.get(base_url)
	source_code.encoding=None   # None 으로 설정
	plain_text = source_code.text
	soup = BeautifulSoup(plain_text, 'lxml')

	if base_url[-1] != '/':
		base_url += '/'

	print('base_url', base_url)
	directory = base_url.split('/')[-2].replace(' ', '-')

	try:
		os.stat(directory)
		return
	except:
		os.mkdir(directory)

	for a in soup.findAll('a', {'class':'item-subject'}):
		_url = a.get("href")
		_name = a.text.strip()

		url = base_url + _url.split('/')[-1].replace(' ', '-')

		print('url: ', url)
		_source_code = requests.get(url)
		_source_code.encoding=None   # None 으로 설정
		_plain_text = _source_code.text
		_soup = BeautifulSoup(_plain_text, 'lxml')

#		if _url.split('/')[-1] == '14062':
#			print(_soup)
#			print(_soup.find('img', {'class':'img-tag'}))


		for i, img in enumerate(_soup.findAll('img', {'class':'img-tag'})):
			imgUrl = img.get("src")
			#print('imgUrl', imgUrl)
			fileName = directory + '/' + set_fileName(_name) + str(i).zfill(2) + get_fileExt(imgUrl)

			r = requests.get(imgUrl, allow_redirects=True)
			f = open(fileName, 'wb')
			f.write(r.content)
			f.close()



def list_toon(url):
	source_code = requests.get(url)
	source_code.encoding=None   # None 으로 설정
	plain_text = source_code.text
	soup = BeautifulSoup(plain_text, 'lxml')
	toons = []

	for div in soup.findAll('div', {'class':'img-item'}):
		toon = div.find('h3').text.strip()
		toons.append(toon)

	#print(toons)
	return toons


def get_fileName(head='', src=''):
	return head + src.split('/')[-1]



def set_fileName(name=''):
	name = name.strip().replace(' ', '-')
	digit = re.findall("\d+", name)
	if len(digit) == 0:
		return name + '_'
	else:
		il = name.rfind(digit[-1])
		name = (name[:il] + '_').replace('-_', '_')
		return name + digit[-1].zfill(3) + '_'


def get_fileExt(src=''):
	return '.' + src.split('.')[-1]


#+++++++++++++++
# main
#+++++++++++++++

url = 'https://babtoon.com/연재웹툰'
toons = list_toon(url)

for toon in toons:
	base_url = 'https://babtoon.com/웹툰/' + toon.strip().replace(' ', '-') + '/'
	spider(base_url, '')


#names = [' 좋은 듯 더 좋은 듯 16화 ', '좋은듯16화', '더 좋은 듯2 16화']

#for name in names:
#	print(set_fileName(name))



