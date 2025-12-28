from typing import Any

from keras import layers

from topologyx.channels.silhouette import SilhouetteLayer


def betti_channel(input: Any, args: dict[str, Any], dropout: float = 0.3) -> Any:
    channel = layers.Reshape((input._keras_shape[1], 1))(input)
    channel = layers.Conv1D(64, 10, **args)(channel)
    channel = layers.PReLU()(channel)
    channel = layers.Dropout(dropout)(channel)
    channel = layers.Conv1D(128, 6, **args)(channel)
    channel = layers.PReLU()(channel)
    channel = layers.Conv1D(128, 6, **args)(channel)
    channel = layers.PReLU()(channel)
    channel = layers.Conv1D(128, 4, **args)(channel)
    channel = layers.PReLU()(channel)
    channel = layers.Dropout(dropout)(channel)
    channel = layers.GlobalAveragePooling1D()(channel)

    return channel


def silhouette_channel(input: Any, args: dict[str, Any], dropout: float = 0.3) -> Any:
    channel = SilhouetteLayer(int(input._keras_shape[-1]))(input)

    channel = layers.Conv1D(64, 10, **args)(channel)
    channel = layers.PReLU()(channel)
    channel = layers.Dropout(dropout)(channel)
    channel = layers.Conv1D(128, 6, **args)(channel)
    channel = layers.PReLU()(channel)
    channel = layers.Conv1D(128, 6, **args)(channel)
    channel = layers.PReLU()(channel)
    channel = layers.Conv1D(128, 4, **args)(channel)
    channel = layers.PReLU()(channel)
    channel = layers.Dropout(dropout)(channel)
    channel = layers.GlobalAveragePooling1D()(channel)

    return channel
