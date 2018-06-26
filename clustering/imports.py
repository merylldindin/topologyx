# Author: DINDIN Meryll
# Date: 26/06/2018
# Project: TDAToolbox

import sys

import numpy as np

from scipy.stats import kde
from sklearn.neighbors import KDTree
from sklearn.datasets import make_blobs, make_circles, make_moons

try:
	import matplotlib.pyplot as plt
	import matplotlib.gridspec as gds
	from mpl_toolkits.mplot3d import Axes3D
except:
	print('[###] Visual packages could not be imported ...')

try: 
	gpath = '2018-01-31-09-25-53_GUDHI_2.1.0/build/cython'
	build = '/home/intern/Downloads/{}'.format(gpath)
	sys.path.append(build)
	import gudhi
except:
	print('[###] Gudhi could not be imported ...')