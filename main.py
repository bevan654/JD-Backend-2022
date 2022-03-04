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





class Monitor:
	def __init__(self,endpoint):
		self.endpoint = endpoint

	def LOG(self,text,color):
		print(colored(f'[{datetime.now()}] {text}',color))

	def start_monitor(self):
		pass



	def headers(self):
		method = "GET"
		content = ''
		content_type = 'application/json'

		sender = Sender({'id': '60122c4543',
		'key': '066268d08e45b34290f553f9f4e56906',
		'algorithm': 'sha256'},
		self.url,
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



endpoints = []
for i in endpoints:
	#threading.Thread(target=Monitor,args=(i,)).start()
	Monitor(i)