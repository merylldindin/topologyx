# Author:  DINDIN Meryll
# Date:    05/05/2019
# Project: TdaToolbox

try: from architecture.layers import *
except: from layers import *

# Keras channel for Betti curves

def betti_channel(input_layer, ini_args, dropout=0.3):

    mod = Reshape((input_layer._keras_shape[1], 1))(input_layer)
    mod = Conv1D(64, 10, **ini_args)(mod)
    mod = PReLU()(mod)
    mod = Dropout(dropout)(mod)
    mod = Conv1D(128, 6, **ini_args)(mod)
    mod = PReLU()(mod)
    mod = Conv1D(128, 6, **ini_args)(mod)
    mod = PReLU()(mod)
    mod = Conv1D(128, 4, **ini_args)(mod)
    mod = PReLU()(mod)
    mod = Dropout(dropout)(mod)
    mod = GlobalAveragePooling1D()(mod)

    return mod

# Keras channel for persistence Landscapes

def silhouette_channel(input_layer, ini_args, dropout=0.3):

    shp = int(input_layer._keras_shape[-1])
    sil = SilhouetteLayer(shp)(input_layer)
    mod = Conv1D(64, 10, **ini_args)(sil)
    mod = PReLU()(mod)
    mod = Dropout(dropout)(mod)
    mod = Conv1D(128, 6, **ini_args)(mod)
    mod = PReLU()(mod)
    mod = Conv1D(128, 6, **ini_args)(mod)
    mod = PReLU()(mod)
    mod = Conv1D(128, 4, **ini_args)(mod)
    mod = PReLU()(mod)
    mod = Dropout(dropout)(mod)
    mod = GlobalAveragePooling1D()(mod)

    return mod
