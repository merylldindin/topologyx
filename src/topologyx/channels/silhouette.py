from typing import Any

from keras import initializers, layers, ops


class SilhouetteLayer(layers.Layer):  # type: ignore
    def __init__(self, dimension: int, **kwargs: Any) -> None:
        self.dimension = dimension

        super(SilhouetteLayer, self).__init__(**kwargs)

    def build(self, input_shape: tuple[int, ...]) -> None:
        self.kernel = self.add_weight(
            name="kernel",
            shape=(1, input_shape[-2]),
            initializer=initializers.Constant(value=1.0),
            trainable=True,
        )

        super(SilhouetteLayer, self).build(input_shape)

    def call(self, inputs: Any) -> Any:
        return ops.reshape(
            ops.sum(ops.dot(self.kernel, inputs), axis=0),
            (-1, inputs.get_shape()[-1], 1),
        )

    def compute_output_shape(self, _: Any) -> tuple[None, int, int]:
        return (None, self.dimension, 1)
