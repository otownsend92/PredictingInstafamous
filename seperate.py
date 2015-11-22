try:
	import cPickle as pickle
except:
	import pickle

import os


file_name = 'all_media_single_file.txt'
media_data = {}
file_count = 0


def write_file():
	global 	file_count
	write_file = "media_data_" + str(file_count) + ".txt"
	fw = open(write_file, 'w')
	pickle.dump(media_data, fw)
	file_count = file_count+1
	fw.close()



f = open(file_name, 'r')
print("Reading file: " + file_name)
media = pickle.load(f)
f.close()
print("Reading finish! ")
print(len(media))


for key in media:
	media_data[key] = media[key]
	if(len(media_data) == 30000):
		write_file()
		media_data.clear()

if len(media_data) != 0:
	write_file()
	media_data.clear()

print('Done.')


