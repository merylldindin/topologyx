# Author:  DINDIN Meryll
# Date:    26/06/2018
# Project: TdaToolbox

import sys
import numpy as np

from sklearn.neighbors import KDTree

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