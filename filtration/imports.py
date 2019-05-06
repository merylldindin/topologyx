# Author:  DINDIN Meryll
# Date:    26/06/2018
# Project: TdaToolbox

# Common packages
import sys
import tqdm
import numpy as np

from sklearn.neighbors import KDTree

try:
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gds
    import plotly.offline as pyo
    import plotly.graph_objs as go

    from plotly import tools
except:
    print('[###] Visual packages could not be imported ...')

try: 
    import gudhi
except:
    print('[###] Gudhi could not be imported ...')