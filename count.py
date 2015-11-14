try:
    import cPickle as pickle
except:
    import pickle

import os

locations = {'San Francisco':0,'New York City':0,'Los Angeles':0,'Tokyo':0,'London':0,'Paris':0,'Chicago':0,'Moscow':0,'Toronto':0,'Sydney':0}

all_media = {}
for fn in os.listdir('./Media/'):
    print("Reading file: " + str(fn))
    if os.path.exists('./Media/'+fn):
            f = open('./Media/'+fn, 'r')
            print(f)
            curr_media = pickle.load(f)
            for key in curr_media:
                all_media[key] = curr_media[key]

print("Getting counts...")
for key in all_media:
    if key[1] in locations:
        locations[key[1]] += 1

print(locations)

count = 0
for key in locations:
	count = count + locations[key]
print("Total: " + str(count))		      
                
