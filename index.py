# -*- coding: utf-8 -*-
# @Author: d4r
# @Date:   2017-12-30 18:57:32
# @Last Modified by:   d4r
# @Last Modified time: 2018-01-04 01:53:47
import os
import sys
import time
from collections import deque 

import ConfigParser
config = ConfigParser.ConfigParser()
config.read('config.ini')
# get config
username = config.get('default', 'username')
password = config.get('default', 'password')

from worker import Worker

sys.path.append(os.path.join(sys.path[0], 'module/instabot/src'))

from check_status import check_status
from feed_scanner import feed_scanner
from follow_protocol import follow_protocol
# from instabot import InstaBot
from instabotalpha import InstabotAlpha
from unfollow_protocol import unfollow_protocol

print 'try to login as ' + username

cycle = deque()
current_cycle_index = 0
current_cycle = ''
ready_to_post = 0
last_analyze = 0

bot = InstabotAlpha(
		username,
		password
	)

def sequence_cycle (self):
	a = [
		method_name for method_name in dir(self)
 		if callable(getattr(self, method_name)) 
 	]
 	b = [
 		name for name in a if "__" not in name
 	]
	c = reversed(b)
	cycle.extendleft(c)

worker = Worker(bot)

sequence_cycle(worker)

while True:
	current_cycle = cycle[0]
	check_status(bot)
	# try:
	func = getattr(worker, current_cycle)
	func()
	# except:
	# 	print sys.exc_info()[0]
	# time.sleep(10 * 60)
	cycle.rotate(-1)
	pass

