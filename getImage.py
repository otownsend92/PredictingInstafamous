try:
    import cPickle as pickle
except:
    import pickle
import os
import pprint
import urllib

all_media = {}

for file in os.listdir('./Media'):
    f = open('./Media/' + file, 'r')
    all_media = pickle.load(f)

    for media in all_media.keys():
        url = str(all_media[media].images['standard_resolution'])[7:]
        imgPath =  "./Images/" + media[0] + "." + url[-3:]
        urllib.urlretrieve(url,imgPath)
