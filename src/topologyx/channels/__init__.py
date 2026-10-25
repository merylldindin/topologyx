from typing import Any

from topologyx.channels.backend import select_keras_backend

select_keras_backend()

from keras import layers

from topologyx.channels.silhouette import SilhouetteLayer


def _stack_convolutions(channel: Any, args: dict[str, Any], dropout: float) -> Any:
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
    return layers.GlobalAveragePooling1D()(channel)


def betti_channel(input: Any, args: dict[str, Any], dropout: float = 0.3) -> Any:
    channel = layers.Reshape((input.shape[1], 1))(input)
    return _stack_convolutions(channel, args, dropout)


def silhouette_channel(input: Any, args: dict[str, Any], dropout: float = 0.3) -> Any:
    channel = SilhouetteLayer(int(input.shape[-1]))(input)
    return _stack_convolutions(channel, args, dropout)
