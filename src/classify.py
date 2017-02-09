from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier, GradientBoostingClassifier, ExtraTreesClassifier
import os
from os.path import isdir
from transform import transform
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import random

def to_list(func):
	def _list():
		return [i for i in func()]

	return _list

@to_list
def prepare_samples():
	for k in os.listdir('samples'):
		if isdir('samples/%s' % k):
			for i in os.listdir('samples/%s' % k):
				if i.endswith('.jpg'):
					yield k, 'samples/%s/%s' % (k, i)


def training():
	X = []
	Y = []

	for y, path in sorted(prepare_samples(), key=lambda i:random.random()):
		print y, path
		Y.append(y)
		X.append(transform(path))

	X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.5, random_state=0)

	rf = GradientBoostingClassifier()
	rf = rf.fit(X_train, y_train)
	y_pred = rf.predict(X_test)
	# print yp

	print classification_report(y_test, y_pred)
	
	return rf

