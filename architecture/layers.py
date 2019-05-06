# Author:  DINDIN Meryll
# Date:    05/05/2019
# Project: TdaToolbox

try: from architecture.imports import *
except: from imports import *

# Keras layer for Landscapes ponderation

class SilhouetteLayer(Layer):

    # Initialisation
    def __init__(self, output_dim, **kwargs) :
        
        # Defines the output dimension
        self.output_dim = output_dim
        
        super(SilhouetteLayer, self).__init__(**kwargs)

    # Build the layer
    def build(self, input_shape) :
        
        # Init all the weights to one
        ini = initializers.Constant(value=1.0)
        # Create a trainable weight variable for this layer
        self.kernel = self.add_weight(name='kernel', shape=(1, input_shape[-2]), 
                                      initializer=ini, trainable=True)
        
        super(SilhouetteLayer, self).build(input_shape)

    # Fit instance
    def call(self, x) :
        
        var = K.reshape(K.sum(K.dot(self.kernel, x), axis=0), (-1, x.get_shape()[-1], 1))
        
        return var

    # Output shape for inference
    def compute_output_shape(self, input_shape) :
        
        return (None, self.output_dim, 1)

