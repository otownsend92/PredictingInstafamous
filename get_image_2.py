try:
    import cPickle as pickle
except:
    import pickle
import os
import pprint
import urllib2

all_media = {}


f = open('all_media_single_file.txt', 'r')
all_media = pickle.load(f)
folder_count = 0
image_count = 0

for media in all_media.keys():
	url = str(all_media[media].images['standard_resolution'])[7:]
	imgPath = "./Images" + str(folder_count) + "/" + media[0] + "." + url[-3:]

	# Create new image folder if it doesnt exist
	if not os.path.exists("./Images"+str(folder_count)):
		os.mkdir("./Images" + str(folder_count))

	# Save image
	if url[-3:] == "jpg":# && not os.path.exists(imgPath):
		try:
			f = open(imgPath,'wb')
			f.write(urllib2.urlopen(url,timeout = 10).read())
			f.close()
			# urllib.urlretrieve(url, imgPath)
			image_count = image_count + 1
		except Exception as e:
			print("Could not retrieve: " + str(media) + " at: " + str(url))

	# If 20,000 images in current image directory, make a new one 
	if image_count == 20000:
		folder_count = folder_count + 1
		image_count = 0
