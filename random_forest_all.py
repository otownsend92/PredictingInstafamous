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
from sklearn import ensemble
from math import ceil
from math import floor


feature_array = []
label_array = []

f = open("combined_data_zenghui.txt")
combined_data = pickle.load(f)
f.close()

for key in combined_data:
	features = combined_data.get(key)

	# (hour, num_tags, len_caption, num_people, filter_i, num_fold, num_fols, num_media)
	f = (features[0], features[1], features[2], features[3], features[4], features[5], features[6], features[7])
	feature_array.append(f)
	label_array.append(key[2])

print 'Done loading combining data.\n'
# ------------------------------



# ------------------------------
print 'Running random forest algorithm'
score = 0
attempt = 0

while score < 0.8 and attempt < 5:
	print 'Attempt',attempt
	
	train = int(floor(0.8*len(combined_data)))
	print 'Training with',train,'samples'
	
	model = ensemble.RandomForestRegressor(n_estimators=100)
	model.fit(feature_array[:train], label_array[:train])
	print'Built random forest and trained it'

	predict_labels = model.predict(feature_array[train:])
	print 'Predicted popularity...'

	score = model.score(feature_array[train:],label_array[train:])



	print 'Training done --------- '
	print 'Total samples:          ',len(feature_array)
	print 'Score:                  ',score
	print 'Size of test data:      ',len(predict_labels)
	print '----------------------- \n'



	i = 0
	while i < 40:
		print'Predicted:',predict_labels[i],'. Actual:',label_array[train+i]
		i += 1


	if score >= 0.8 or attempt == 4:
		print 'Writing model to disk...'
		ff = open('model_'+str(score)[:6]+'.txt', 'w')
		pickle.dump(model, ff)
		ff.close()
		print 'Done.'
		break

	else:
		print 'Model not good enough.\nDone.'

	attempt += 1



