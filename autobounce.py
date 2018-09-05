#!/usr/bin/env python
# coding: utf-8

"""
		I run this script with crontab every 4 hours.
		alternatively, you could fetch the hour time in Yad2 and schedule the next update.
"""

import pickle
from requests_html import HTMLSession

# TODO: save session cookies and use it to login?
def save_cookies_to_file(r_cookie_jar, file_name):
	with open(file_name, 'wb') as f:
		pickle.dump(r_cookie_jar, f)

def load_cookies_from_file(file_name):
	with open(file_name, 'rb') as f:
		return pickle.load(f)

s = HTMLSession()

# log-in
s.post('https://my.yad2.co.il/login.php', data = {'Username' : 'ENTER_YOUR_USER_NAME_HERE', 'Password' : 'ENTER_YOUR_PASSWORD_HERE'})

# get html
r_products_html = s.get('https://my.yad2.co.il/newOrder/index.php?action=personalAreaFeed&CatID=3&SubCatID=0')

print(r_products_html)

#loop through products
for r_data_frame_object in r_products_html.html.find('tr[data-frame]'):

	r_data_frame_url = r_data_frame_object.attrs['data-frame']
	r_data_frame = s.get('https:' + r_data_frame_url)

	r_bounce_url = r_data_frame.html.find('#bounceRatingOrderBtn', first=True).attrs['data-ajax_path']

	if r_bounce_url == None:
		print("Err! couldn't get bounce url")

	print('https:' + r_bounce_url)

	#update
	s.post('https:' + r_bounce_url, headers = {'X-Requested-With' : 'XMLHttpRequest'})




