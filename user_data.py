try:
	import cPickle as pickle
except:
	import pickle

from instagram.client import InstagramAPI
import os
import urllib

# locations = {'San Francisco':0,'New York City':0,'Los Angeles':0,'Tokyo':0,'London':0,'Paris':0,'Chicago':0,'Moscow':0,'Toronto':0,'Sydney':0}

access_token = "1503846364.461e393.349bc641eed2421aad507296ea092956"
client_secret = "384018d7be63463a87ca48a9da21f17c"

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
for fn in os.listdir('./Media/'):
	print("Reading file: " + str(fn))
	if os.path.exists('./Media/'+fn):
		f = open('./Media/'+fn, 'r')
		print(f)
		curr_media = pickle.load(f)
		for key in curr_media:
			# all_media[key] = curr_media[key]
			user_id = curr_media[key].user.id
			num_followed_by,num_follows,num_media = user(user_id)
			user_data[user_id] = (num_followed_by,num_follows,num_media)
		f.close()


print len(user_data), ' unique users. Writing data to disk...'

f = open("user_data.txt", 'w')
pickle.dump(user_data, f)
f.close()

print 'Done.\n'


