try:
	import cPickle as pickle
except:
	import pickle

from instagram.client import InstagramAPI
import os
import urllib


# Insert access_token and client secret here:
access_token = ""
client_secret = ""

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


user_data = {}

# TODO: INSERT FILE NAME HERE!!!
file_name = ''

f = open(file_name, 'r')
print("Reading file: " + file_name)
print(f)
curr_media = pickle.load(f)
for key in curr_media:
	user_id = curr_media[key].user.id
	num_followed_by,num_follows,num_media = user(user_id)
	user_data[user_id] = (num_followed_by,num_follows,num_media)
f.close()


print len(user_data), ' unique users. Writing data to disk...'

f = open("user_data.txt", 'w')
pickle.dump(user_data, f)
f.close()

print 'Done.\n'


