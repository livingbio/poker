import os
import numpy as np

from skimage import data
from skimage.feature import match_template
from skimage import io
from skimage import color
from skimage.transform import resize

def transform(file):
	return np.array(resize(color.rgb2gray(io.imread(file)), (128, 72))).flatten()

