from mohawk import Sender
import requests
import json
from datetime import datetime
from termcolor import *
import colorama
import random
from discord_webhook import DiscordWebhook, DiscordEmbed
import threading
import time
colorama.init()

keywords = ['jordan 1','jordan 3','jordan 4','jordan 5','dunk','yeezy','1 per customer']



proxies = [{'http': 'http://xaqhyoax-rotate:8zr5nbw48xey@p.webshare.io:80', 'https': 'https://xaqhyoax-rotate:8zr5nbw48xey@p.webshare.io:80'}]


class Monitor:
	def __init__(self,endpoint):
		self.endpoint = endpoint
		self.products = []
		self.first_run = True

		self.start_monitor()

	def LOG(self,text,color):
		print(colored(f'[{datetime.now()}] {text}',color))


	def sendWebhook(self,name,sku,price,image,stock):

		if any(keyword in name.lower() for keyword in keywords):
			webhook_url = 'https://discord.com/api/webhooks/905605075114790952/Qwgth0OrJwKZ06OYX9AaJVLKJKADVXFk-SWB3B82XomKB_nH_Ft_aQseWo1YnQOsHqxo'
		else:
			webhook_url = 'https://discord.com/api/webhooks/948935640781824010/DWN8o8FO7aDndUGaUBH_TJYz9pRbZwE91cCQocO9hFyQIpWWhN0NBUdEEHQP3glNt9vi'

		
		
		webhook = DiscordWebhook(url=webhook_url)
		url = 'https://www.jd-sports.com.au/product/slot/'+sku.replace('_'+sku+'/','')+'?category=jdapp&endpoint=slot'

		embed = DiscordEmbed(title=name, color=15158332,url=url)
		
		embed.set_author(name='JD BACKEND')
		

		embed.set_thumbnail(url=image)
		
		# set footer
		embed.set_footer(text='Powered By Genesis | JDAU V0.9.9', icon_url='https://media.discordapp.net/attachments/904022469512396861/904022677109497907/Genesis_AIO_logo_black.png?width=810&height=810')
		
		embed.set_timestamp()
		
		# add fields to embed
		embed.add_embed_field(name='SKU', value=sku,inline=True)
		embed.add_embed_field(name='PRICE', value=str(price['amount']),inline=True)
		embed.add_embed_field(name='STOCK',value=stock,inline=False)
		embed.add_embed_field(name='LINKS',value=f'[Desktop Link]({url})')
		
		webhook.add_embed(embed)
		
		response = webhook.execute()

	def getStock(self,url):
		self.LOG('[STOCK] Fetching Stock','yellow')
		desc = ''
		while True:
			try:
				response = requests.get(url,proxies=random.choice(proxies),headers=self.headers(url))
			except:
				self.LOG("Request Error",'red')
				time.sleep(1)
				continue

			if response.status_code == 200:
				response = response.json()
				for i in response['options']:
					desc = desc + '``'+i+' :: ' + response['options'][i]['SKU'] + '``\n'

				break
				
			elif response.status_code == 403:
				self.LOG(" [STOCK UNAUTHORIZED] 403",'red')
				time.sleep(1)
				break
			elif response.status_code == 503:
				self.LOG("[STOCK SERVER ERROR] Backend Fetch Error 503",'red')
				time.sleep(1)
				continue
			else:
				self.LOG("[STOCK UNKOWN] Unkown Response Status "+str(response.status_code),'red')
				time.sleep(1)
				break

		if desc == '':
			desc = 'undefined'

		return desc
				
		
	def start_monitor(self):
		cycle = 0
		while True:
			cycle += 1

			if(cycle == 1 or cycle == 2 or cycle % 500 == 0):
				self.LOG(f'[CYCLE {str(cycle)}] Fetching Products','magenta')

			
			try:
				response = requests.get(self.endpoint,proxies=random.choice(proxies),headers=self.headers(self.endpoint))
			except Exception as e:
				print(e)
				self.LOG("Request Error",'red')
				time.sleep(1)
				continue

			if response.status_code == 200:
				response = response.json()

				for i in response['products']:
					if i['ID'] not in self.products:
						self.products.append(i['ID'])
						if not self.first_run:
							self.LOG("[NEW PRODUCT] :: "+i['name'],'green')
							self.sendWebhook(i['name'],i['ID'],i['price'],i['mainImage'],self.getStock(i['href']))


				if(self.first_run):
					self.LOG("[FIRST RUN] Products Fetched",'magenta')
							
						
					

			elif response.status_code == 403:
				self.LOG("[UNAUTHORIZED] 403",'red')
				time.sleep(1)
			elif response.status_code == 503:
				self.LOG("[SERVER ERROR] Backend Fetch Error 503",'red')
				time.sleep(1)
			else:
				self.LOG("[UNKOWN] Unkown Response Status "+str(response.status_code),'red')
				time.sleep(1)

				
			self.first_run = False
			time.sleep(5)



	def headers(self,url):
		method = "GET"
		content = ''
		content_type = 'application/json'

		sender = Sender({'id': '60122c4543',
		'key': '066268d08e45b34290f553f9f4e56906',
		'algorithm': 'sha256'},
		url,
		method,
		content=content,
		content_type=content_type)

		return {
			"x-api-key": "1753F69D6B4F48F9956DEE1002A83491",
			"MESH-Commerce-Channel": "android-app-phone",
			"User-Agent": "jdsportsjx/6.2.7.8361 (android-app-phone; Android 5.1.1; Build/SM-G955N-user 5.1.1 NRD90M.G955NKSU1AQDC 500201121 release-keys)",
			"Cache-Control": "no-cache",    
			"X-Request-Auth": sender.request_header,
			"Host": "prod.jdgroupmesh.cloud",
			"Connection": "Keep-Alive",
			"accept-encoding": "gzip"
		}



endpoints = ['https://prod.jdgroupmesh.cloud/stores/jdsportsau/products/category/women/womens-footwear?channel=iphone-app&max=2000','https://prod.jdgroupmesh.cloud/stores/jdsportsau/products/category/men/mens-footwear?channel=iphone-app&max=2000','https://prod.jdgroupmesh.cloud/stores/jdsportsauf/products/category/kids/junior-footwear-(sizes-3.5-7)/all-trainers?channel=iphone-app&max=2000']
for i in endpoints:
	threading.Thread(target=Monitor,args=(i,)).start()
