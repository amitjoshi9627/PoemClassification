# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import requests
import csv


class PoembotSpider(scrapy.Spider):
	name = 'poembot'
	allowed_domains = ['https://www.poets.org/poetsorg/poems?field_poem_themes_tid=1046']
	start_urls = ['https://www.poets.org/poetsorg/poems?field_poem_themes_tid=1166&page={num}'.format(num = num) for num in range(50,52)]#+["https://www.poets.org/poetsorg/poems?field_poem_themes_tid=896&page={num}".format(num = num) for num in range(0,55)] + ["https://www.poets.org/poetsorg/poems?field_poem_themes_tid=856&page={num}".format(num = num) for num in range(0,25)]+["https://www.poets.org/poetsorg/poems?field_poem_themes_tid=1226&page={num}".format(num = num) for num in range(0,56)]

	def parse(self, response):
		print('Processing>>>>>>>>>>>>>>>>>>>>>>',response.url)
		poem_links = response.xpath('//td[@class = "views-field views-field-title"]//a/@href').getall()
		poems = []
		urls =[]
		#886-->Animals(32)
		#901 -->Beauty(39)
		genres = {'971':'Death','896':'Audio','1226':'Nature','1166': 'Love'}
		for poem_link in poem_links:
			if len(urls) > 15:
				break
			try:
				poem_url = 'https://www.poets.org' + poem_link
				source = requests.get(poem_url).text
				soup = BeautifulSoup(source,'lxml')               
				text_wrapper = soup.find_all('div',id = "poem-content")[0].find_all('div')[4].pre
				poem = ''
				if text_wrapper != None:
					text = text_wrapper.text
					length = len(text.split(' '))
					poem = " ".join(text.split(' ')[:50]).replace('\n',' ')	 
					poem = poem.replace('  ','')               
				else:
					text_wrapper = soup.find_all('div',id = "poem-content")[0].find_all('div')[4].p
					text = text_wrapper.text
					length = len(text.split(' '))
					poem = " ".join(text.split(' ')[:50]).replace('\n',' ')
					poem = poem.replace('  ','')
				if length < 40:
					continue
				if poem not in poems:
					poems.append(poem)
					urls.append(poem_url)
			except:
				pass

		genre = genres[response.url.split('=')[1].split('&')[0]]
		for item,url in zip(poems,urls):
			scraped_data = {'Genre': genre,'Poem':item,'Poem Url': url}
			yield scraped_data
