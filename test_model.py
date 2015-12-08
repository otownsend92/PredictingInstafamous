import numpy as np
import time  

try:
	import cPickle as pickle
except:
	import pickle

from scipy.stats import spearmanr

from sklearn.svm import SVR
from sklearn.svm import LinearSVR
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV


def loadData(filename = "data.txt"):
	media_features = {}
	media_likes = {}

	f = open(filename, 'r')
	for line in f:
		line = line.strip().split('\t')
		media_id = line[0]
		user_id = line[1]
		hour = float(line[2])
		num_tags = float(line[3])
		len_caption = float(line[4])
		num_people = float(line[5])
		filter_i = float(line[6])
		num_followed = float(line[7])
		num_follows = float(line[8])
		num_media = float(line[9])
		num_likes = float(line[10])
		
		features = np.array([hour, num_tags, len_caption, num_people, filter_i, num_followed, num_follows, num_media]) 

		media_features[media_id] = features
		media_likes[media_id] = num_likes
	f.close()

	return media_features,media_likes


def getX(media_features):
	m = len(media_features)
	n = len(media_features.items()[0][1])
	
	X = np.zeros((m,n))
	media_list = []

	count = 0

	for media_id in media_features:
		media_list.append(media_id)
		features = media_features[media_id]
		X[count] = features
		count += 1

	return X, media_list


def getY(media_likes):
	m = len(media_likes)
	Y = np.zeros(m)
	count = 0

	for media_id in media_likes:
		like = media_likes[media_id]
		Y[count] = like
		count += 1

	return Y



def tuning_params(train_x,train_y):

	#Parameter tuning using grid search
	parameters = {'C': [0.0001, 0.001, 0.01, 0.1, 1, 10, 100,1000],
				  'tol': [1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 10],
				  }

	gs_clf = GridSearchCV(LinearSVR(), parameters, n_jobs=-1)
	gs_clf = gs_clf.fit(train_x, train_y)

	best_parameters, score, _ = max(gs_clf.grid_scores_, key=lambda x: x[1])
	for param_name in sorted(parameters.keys()):
		print("%s: %r" % (param_name, best_parameters[param_name]))

	print score
	

if __name__ == '__main__':

	media_features,media_likes = loadData("train_data.txt")
	X_train, train_media_list = getX(media_features)
	Y_train = getY(media_likes)


	test_media_features,test_media_likes = loadData("test_data.txt")
	X_test, test_media_list = getX(test_media_features)
	Y_test = getY(test_media_likes)
	

	print "start tuning_params"

	tuning_params(X_train,Y_train,X_test,Y_test)

	print "Done"

	