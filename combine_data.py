try:
    import cPickle as pickle
except:
    import pickle
import os
import pprint
import urllib2
import time
import datetime
import numpy as np


all_data = {}
dead_users = 0
combined_file_num = 0

city_times = {
	'Bangkok':7,	# Bangkok is 7 hours ahead of UTC
	'Beijing':8,
	'Boston':-5,	# Boston is 5 hours behind UTC
	'Buenos Aires':-3,
	'Cairo':2,
	'Chicago':-6,
	'Columbus':-5,
	'Delhi':5.5,
	'Dhaka':6,
	'Houston':-6,
	'Las Vegas':-8,
	'London':0,
	'Los Angeles':-8,
	'Mexico City':-6,
	'Moscow':3,
	'Mumbai':5.5,
	'New York City':-5,
	'Oklahoma':-6,
	'Osaka':9,
	'Paris':1,
	'Philadelphia':-5,
	'San Antonio':-6,
	'San Diego':-8,
	'San Francisco':-8,
	'Sao Paulo':-2,
	'Seattle':-8,
	'Shanghai':8,
	'Singapore':8,
	'Sydney':11,
	'Tokyo':9,
	'Toronto':-5,
	'Washington':-5
}

filters = {
	'kelvin':0,
	'1977':1,
	'walden':2,
	'hudson':3,
	'inkwell':4,
	'sutro':5,
	'sierra':6,
	'hefe':7,
	'toaster':8,
	'nashville':9,
	'brannan':10,
	'willow':11,
	'lo-fi':12,
	'x-pro ii':13,
	'valencia':14,
	'rise':15,
	'amaro':16,
	'mayfair':17,
	'earlybird':19,
	'normal':20,
	'clarendon':21,
	'ludwig':22,
	'gingham':23,
	'moon':24,
	'lark':25,
	'reyes':26,
	'juno':27,
	'slumber':28,
	'crema':29,
	'aden':30,
	'perpetua':31,
	'ashby':32,
	'charmes':33,
	'skyline':34,
	'stinson':35,
	'vesper':36,
	'dogpatch':37,
	'unknown':38,
	'maven':39,
	'brooklyn':40,
	'helena':41,
	'ginza':42,
	'poprocket':43,
	'':44
}

# User info data
user_data = {}
user_data_temp = {}
user_data_file_list = []

# Media social data
media_data_temp = {}
media_file_list = []

# ------------------------------
# Load user data
for _file in os.listdir('./'):
	if "user_data_" in _file:
		user_data_file_list.append(_file)

for user_data_file in user_data_file_list:

	f = open(user_data_file)
	# print 'Loading ',user_data_file
	user_data_temp = pickle.load(f)
	f.close()
	user_data.update(user_data_temp)
	# print 'user_data length:',len(user_data)
	user_data_temp.clear()

print '\nDone loading user data.\n',len(user_data),'total users\nNow loading media text data...\n'
# ------------------------------


# ------------------------------
# Load media data
	# number of tags
	# caption length
	# number of likes
	# hour it was uploaded (0-23)
	# number of people tagged in photo
	# location ID

for _file in os.listdir('./'):
	if "media_data_" in _file:
		media_file_list.append(_file)

for media_data_file in media_file_list:

	f = open(media_data_file)
	print 'Loading ', media_data_file
	media_data_temp = pickle.load(f)

	for key in media_data_temp:
		m_id = key[0]
		loc = key[1]
		media = media_data_temp.get(key, None)
		if (media is None):
			continue # and forget about this one

		else :
			time_diff = city_times[loc]
			created_time = str(media.created_time)
			hour = int(created_time.split(" ")[1].split(":")[0])
			hour = (hour + time_diff)%24
			num_tags = len(media.tags)
			len_caption = len(str(media.caption))
			num_people 	= len(media.users_in_photo)
			filter_s = str(media.filter).lower()
			filter_i = filters[filter_s]
			user_id = media.user.id
			num_likes = media.like_count

			try:
				# (num_followed_by,num_follows,num_media)
				num_fold = user_data[user_id][0]
				num_fols = user_data[user_id][1]
				num_media = user_data[user_id][2]

				# Finally add all features to all_media
				features = np.array([hour, num_tags, len_caption, num_people, filter_i, num_fold, num_fols, num_media]) 
				all_data[(media,user_id,num_likes)] = features
				# print '\n\nADDED ',media,' :: ',user_id

			except Exception as e:
				print 'Could not get user data'
				# print(e)
				dead_users += 1
				print 'Total dead users:',dead_users,'\n'
				continue

	if (len(all_data) > 50000):
		ff = open('combined_data_'+str(combined_file_num)+'.txt', 'w')
		pickle.dump(all_data, ff)
		ff.close()
		combined_file_num += 1
		all_data.clear()
		print 'Wrote combined file number',combined_file_num





	# user_data.update(user_data_temp)
	f.close()



print 'Done combining data.\n'
# ------------------------------





