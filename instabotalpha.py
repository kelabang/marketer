# -*- coding: utf-8 -*-
# @Author: d4r
# @Date:   2018-01-02 00:29:44
# @Last Modified by:   d4r
# @Last Modified time: 2018-01-05 00:35:46
import os
import sys
import time
import urllib2
import logging

sys.path.append(os.path.join(sys.path[0], 'module/pynstagram'))
sys.path.append(os.path.join(sys.path[0], 'module/instabot/src'))
print sys.path
from instabot import InstaBot
import pynstagram

logger = logging.getLogger('instabot')
hldr = logging.FileHandler('/var/tmp/instabot.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

hldr.setFormatter(formatter)
logger.addHandler(hldr)
logger.setLevel(logging.INFO)

class InstabotAlpha(InstaBot):
	ready_to_post = False
	feed_to_post = False
	def submit (self):
		url = self.feed_to_post.get('node', {}).get('display_url')
		captions = self.feed_to_post.get('node', {}).get('edge_media_to_caption',{}).get('edges',{})
		owner_username = self.feed_to_post.get('node', {}).get('owner', {}).get('username')
		caption = ''
		if len(captions) > 0:
			caption = captions[0].get('node',{}).get('text') +'. by: @'+owner_username
		self.reupload(url, caption)
		pass

	def reupload (self, url, caption):
		# download image 
		filedata = urllib2.urlopen(url)
		datatowrite = filedata.read()

		with open('./downloads/tmp.jpg', 'wb') as f:
			f.write(datatowrite)
		 
		with pynstagram.client(self.user_login, self.user_password) as client:
			client.upload('./downloads/tmp.jpg', caption)
		pass
	def record_error (self, msg):
		logger.error(msg)
		pass
	def record_info (self, msg):
		print msg
		logger.info(msg)
		pass