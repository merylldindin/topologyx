import keras
import numpy as np

from topologyx.channels import betti_channel, silhouette_channel

CONV_ARGS = {"padding": "same"}
BATCH_SIZE = 4


def test_betti_channel_pools_to_final_filters() -> None:
    inputs = keras.Input(shape=(100,))
    model = keras.Model(inputs, betti_channel(inputs, CONV_ARGS))

    outputs = model.predict(np.random.rand(BATCH_SIZE, 100), verbose=0)

    assert outputs.shape == (BATCH_SIZE, 128)


def test_silhouette_channel_pools_to_final_filters() -> None:
    inputs = keras.Input(shape=(5, 100))
    model = keras.Model(inputs, silhouette_channel(inputs, CONV_ARGS))

    outputs = model.predict(np.random.rand(BATCH_SIZE, 5, 100), verbose=0)

    assert outputs.shape == (BATCH_SIZE, 128)
