# -*- coding: utf-8 -*-
# @Author: d4r
# @Date:   2018-01-01 13:42:27
# @Last Modified by:   d4r
# @Last Modified time: 2018-01-05 00:31:58
import time
import pprint
import random
import json

def get_quality_feed (feed):
	print 'get_quality_feed'
	feed_node = feed['node']
	feed_like_count = 0
	if(feed_node.has_key('edge_media_preview_like')):
		feed_like_count = feed_node.get('edge_media_preview_like', {}).get('count')

	# if hasattr(feed_node, 'edge_media_preview_like'):
	# 	print 'found'
	# 	feed_like_count = feed_node['edge_media_preview_like']['count']
	# else:
	# 	print 'notfound'
	print 'feed_like_count'
	print feed_like_count
	return feed

def filter_quality_feed (feed):
	print 'filter_quality_feed'
	feed_node = feed['node']
	feed_like_count = 0
	if(feed_node.has_key('edge_media_preview_like')):
		feed_like_count = feed_node.get('edge_media_preview_like', {}).get('count')

	# if hasattr(feed_node, 'edge_media_preview_like'):
	# 	print 'found'
	# 	feed_like_count = feed_node['edge_media_preview_like']['count']
	# else:
	# 	print 'notfound'
	print 'feed_like_count'
	print feed_like_count
	return feed

def same_type (feed):
	feed_node = feed.get('node')
	if(feed_node.get('__typename') == 'GraphImage'):
		return True
	else:
		return False

def is_already_posted (keyword):
	with open('/var/tmp/instabot.log') as logfile:
		if keyword in logfile.read():
			return True
		return False

class Worker :
	def __init__(self, bot):
		print 'on init'
		self.bot = bot
	# procedure 'analyze'
	# check what post from on last_logout
	# select several post from last_logout
	# save media and metadata to local
	# set flag to ready to post something
	def analyze (self):
		print '-- onanalyze --'
		last_analyze = time.time()
		# get recent feed
		self.bot.get_media_id_recent_feed()
		# select a high quality feed
		# hq_feeds = filter(filter_quality_feed, self.bot.media_on_feed)
		filter_feeds=filter(same_type, self.bot.media_on_feed)
		data_sorted=sorted(filter_feeds, key=lambda item: 
			item
				.get('node', {})
				.get('edge_media_preview_like', {})
				.get('count'))
		# get high like count
		last_item = data_sorted.pop()
		if(last_item
			.get('node', {})
			.get('edge_media_preview_like', {})
			.get('count') > 30):
			self.bot.ready_to_post = True
			self.bot.feed_to_post = last_item
			# write log last_item that selected
			self.bot.record_info('id:'+last_item.get('node', {}).get('id'))

		time.sleep(1)
		pass

	# procedure 'ready or not'
	# check if flag is ready to post something
	# if yes then post procedure
	# if no then do 'walking around'
	def ready_or_not(self):
		print 'onreadyornot'
		if(self.bot.ready_to_post):
			print 'we are ready to post something'
			postid = self.bot.feed_to_post.get('node', {}).get('id')
			keyid = 'already_id:'+postid

			# check if not posted yet
			if not is_already_posted(keyid):
				# post to social media
				self.bot.submit()
				# write log submit picture feed
				# write log id feed had been posted
				self.bot.record_info(keyid)
			else:
				print 'already posted '+keyid
			# reset value
			self.bot.ready_to_post = False
			self.bot.feed_to_post = False
		else: 
			print 'skip we are not ready for post something'
		
		time.sleep(10 * 60)
		pass

	# procedure 'walking around and like or follow'
	# select several post to follow and like
	def walking_around(self):
		print 'walking_around'
		# ------------------- Get media_id -------------------
		if len(self.bot.media_by_tag) == 0:
		    self.bot.get_media_id_by_tag(random.choice(self.bot.tag_list))
		    self.bot.this_tag_like_count = 0
		    self.bot.max_tag_like_count = random.randint(
		        1, self.bot.max_like_for_one_tag)
		# ------------------- Like -------------------
		self.bot.new_auto_mod_like()
		# ------------------- Follow -------------------
		self.bot.new_auto_mod_follow()
		# ------------------- Unfollow -------------------
		self.bot.new_auto_mod_unfollow()
		# ------------------- Comment -------------------
		self.bot.new_auto_mod_comments()
		# Bot iteration in 1 sec
		time.sleep(3)
		# print("Tic!")
		time.sleep(10 * 60)
		pass
