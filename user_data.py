try:
	import cPickle as pickle
except:
	import pickle

from instagram.client import InstagramAPI
import os
import urllib
import time


# Insert access_token and client secret here:
access_token = ""
client_secret = ""

# TODO: INSERT FILE NAME HERE!!!
file_name = 'all_media_single_file.txt'
user_data = {}
file_count = 0;

def user(user_id):
	num_followed_by = 0
	num_follows = 0
	num_media = 0
	try:
		api = InstagramAPI(access_token=access_token, client_secret=client_secret)
		user = api.user(user_id)
		num_media = user.counts['media']
		num_followed_by = user.counts['followed_by']
		num_follows = user.counts['follows']
	except Exception as e:
		print(e)
	return num_followed_by,num_follows,num_media

def write_file():
	write_file = "user_data_" + str(file_count) + ".txt"
	fw = open(write_file, 'w')
	pickle.dump(user_data, fw)
	file_count = file_count+1
	fw.close()



f = open(file_name, 'r')
print("Reading file: " + file_name)
print(f)
curr_media = pickle.load(f)
f.close()
for key in curr_media:
	user_id = curr_media[key].user.id
	num_followed_by,num_follows,num_media = user(user_id)
	user_data[user_id] = (num_followed_by,num_follows,num_media)
	time.sleep(0.73)
	if(len(user_data) == 30000):
		write_file()
		user_data.clear()




print 'Done.\n'


