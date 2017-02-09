from classify import training
from sklearn.externals import joblib
import os
from transform import transform
import re

class PokerModel(object):
	def __init__(self):
		if not os.path.exists("model.pkl"):
			model = training()
			joblib.dump(model, "model.pkl")

		self.model = joblib.load("model.pkl")

	def predict(self, file):
		x = transform(file)

		return self.model.predict([x])[0]


def cut_clip(path, from_ts, duration, outpath):
    os.system('ffmpeg -i %s -ss %s -c copy -t %s %s' % (path, from_ts, duration, outpath))



def run():
	model = PokerModel()

	start_ts = 0
	buf = []

	for i in (k for k in os.listdir('images') if k.endswith('.jpg')):
		path = "images/%s" % i
		label = model.predict(path)
		buf.append((path, label))
		
	buf.sort(key=lambda i:i[0])

	re_pattern = re.compile(r'thumb([\d]+)\.jpg')

	def cut():
		start_ts = 0
		length = len(buf)

		for ind, (path, label) in enumerate(buf):
			sec = int(re_pattern.findall(path)[0])

			if ind + 1 == length:
				break

			if buf[ind][1] == "breaks" and buf[ind+1][1] == "images":
				yield start_ts, sec

				start_ts = sec

		yield start_ts, length

	for start_ts, end_ts in cut():
		cut_clip('poker.mp4', start_ts, end_ts - start_ts, 'poker%s.mp4' % start_ts)


run()