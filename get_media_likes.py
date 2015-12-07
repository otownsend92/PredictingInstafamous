try:
	import cPickle as pickle
except:
	import pickle

import os


file_name = 'all_media_single_file.txt'
media_data = {}
media_like = {}



def write_file():
	write_file = "media_likes.txt"
	fw = open(write_file, 'w')
	pickle.dump(media_like, fw)
	fw.close()





f = open(file_name, 'r')
print("Reading file: " + file_name)
media = pickle.load(f)
f.close()
print("Reading finish! ")
print(len(media))


for key in media:
	media_id = key[0]
	likes = len(media[key].like_count)
	media_like[media_id] = likes
	
	

	
write_file()

print('Done.')


