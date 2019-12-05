# Author:  DINDIN Meryll
# Date:    26/06/2018
# Project: TdaToolbox

import sys
import numpy as np

from sklearn.datasets import make_blobs
from sklearn.datasets import make_moons
from sklearn.datasets import make_circles
from sklearn.neighbors import KDTree
from scipy.stats import gaussian_kde as kde
from sklearn.decomposition import PCA

try:
	import matplotlib.pyplot as plt
	import matplotlib.gridspec as gds
	from mpl_toolkits.mplot3d import Axes3D
except:
	print('[###] Visual packages could not be imported ...')

try: 
	import gudhi
except:
	print('[###] Gudhi could not be imported ...')