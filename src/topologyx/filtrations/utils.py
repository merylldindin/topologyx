from typing import Any

import gudhi
import matplotlib.pyplot as plt
import numpy as np


def functionize(vector: np.ndarray, descriptor: tuple[float, float]) -> np.ndarray:
    return np.vectorize(
        lambda x: 1 if (x > descriptor[0]) and (x < descriptor[1]) else 0
    )(vector)


def build_betti_curve(
    persistence: Any,
    minimum: float | None = None,
    maximum: float | None = None,
    n_points: int = 100,
) -> np.ndarray:
    if minimum is None:
        minimum = np.min(persistence)

    if maximum is None:
        maximum = np.max(persistence)

    linspace = np.linspace(minimum, maximum, num=n_points)  # type: ignore

    return np.zeros(n_points) + sum(
        functionize(linspace, component) for component in persistence
    )


def build_persistence_landscape(
    persistence: Any,
    minimum: float | None = None,
    maximum: float | None = None,
    n_landscapes: int = 5,
    n_points: int = 100,
) -> np.ndarray:
    if minimum is None:
        minimum = np.min(persistence)

    if maximum is None:
        maximum = np.max(persistence)

    support = np.zeros((n_landscapes, n_points))
    linspace = np.linspace(minimum, maximum, num=n_points)  # type: ignore

    for i, value in enumerate(linspace):
        _vector = []

        for pair in persistence:
            birth_radius, death_radius = pair[0], pair[1]

            if (death_radius + birth_radius) / 2.0 <= value <= death_radius:
                _vector.append(death_radius - value)
            elif birth_radius <= value <= (death_radius + birth_radius) / 2.0:
                _vector.append(value - birth_radius)

        _vector.sort(reverse=True)
        vector = np.asarray(_vector)

        for j in range(n_landscapes):
            if j < len(vector):
                support[j, i] = vector[j]

    return support


def _compute_point_weight(point: tuple[float, float], extrema: float) -> float:
    return 0 if point[1] <= 0 else point[1] / extrema


def _compute_gaussian_kernel(
    point: tuple[float, float],
    x_extremas: tuple[float, float],
    y_extremas: tuple[float, float],
    image_size: tuple[int, int],
    variance: float,
) -> np.ndarray:
    image = np.zeros(image_size)

    x_linspace = np.linspace(x_extremas[0], x_extremas[1], image_size[0])
    y_linspace = np.linspace(y_extremas[0], y_extremas[1], image_size[1])

    for i, x in enumerate(x_linspace):
        for j, y in enumerate(y_linspace):
            image[len(y_linspace) - j - 1, i] = (
                _compute_point_weight(point, y_extremas[1])
                * (1.0 / (2 * np.pi * variance))
                * np.exp(
                    -(np.square(x - point[0]) + np.square(y - point[1]))
                    / (2 * variance)
                )
            )

    return image


def build_persistence_image(
    persistence: Any,
    x_extremas: tuple[float, float] | None,
    y_extremas: tuple[float, float] | None,
    image_size: tuple[int, int],
    variance: float,
) -> np.ndarray:
    image = np.zeros(image_size)

    normalized_persistence = persistence.copy()
    normalized_persistence[:, 1] = (
        normalized_persistence[:, 1] - np.sum(normalized_persistence, axis=1) / 2
    )

    if x_extremas is None:
        x_extremas = (
            np.min(normalized_persistence[:, 0]),
            np.max(normalized_persistence[:, 0]),
        )

    if y_extremas is None:
        y_extremas = (
            np.min(normalized_persistence[:, 1]),
            np.max(normalized_persistence[:, 1]),
        )

    for point in normalized_persistence:
        image += _compute_gaussian_kernel(
            point, x_extremas, y_extremas, image_size, variance
        )

    return image


def plot_persistences(upper_persistence: Any, lower_persistence: Any) -> None:
    _, axes = plt.subplots(nrows=2, ncols=2, figsize=(18, 8))

    gudhi.plot_persistence_diagram(upper_persistence, axes=axes[0, 0])  # type: ignore
    gudhi.plot_persistence_barcode(upper_persistence, axes=axes[1, 0])  # type: ignore
    gudhi.plot_persistence_diagram(lower_persistence, axes=axes[0, 1])  # type: ignore
    gudhi.plot_persistence_barcode(lower_persistence, axes=axes[1, 1])  # type: ignore

    plt.tight_layout()
    plt.show()


def plot_betti_curves(upper_levels: np.ndarray, lower_levels: np.ndarray) -> None:
    # sourcery skip: extract-duplicate-method
    plt.figure(figsize=(18, 3))
    plt.subplot(1, 2, 1)
    plt.title("Upper Levels Betti Curve")
    plt.plot(upper_levels)
    plt.xticks([])
    plt.yticks([])
    plt.subplot(1, 2, 2)
    plt.title("Lower Levels Betti Curve")
    plt.plot(lower_levels)
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()
    plt.show()


def plot_persistence_landscapes(
    upper_levels: np.ndarray,
    lower_levels: np.ndarray,
) -> None:
    # sourcery skip: extract-duplicate-method
    plt.figure(figsize=(18, 3))
    plt.subplot(1, 2, 1)
    plt.title("Upper Levels Persistence Landscapes")
    for component in upper_levels:
        plt.plot(component)
    plt.xticks([])
    plt.yticks([])
    plt.subplot(1, 2, 2)
    plt.title("Lower Levels Persistence Landscapes")
    for component in lower_levels:
        plt.plot(component)
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()
    plt.show()
