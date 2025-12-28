import gudhi
import matplotlib.gridspec as gds
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde as kde


def plot_persistence(persistence: list[tuple[int, list[tuple[float, float]]]]) -> None:
    reduced_persistence = [
        (dimension, radiuses) for (dimension, radiuses) in persistence if dimension == 0
    ]

    _, axes = plt.subplots(nrows=1, ncols=2, figsize=(18, 4))

    gudhi.plot_persistence_diagram(reduced_persistence, axes=axes[0])  # type: ignore

    gudhi.plot_persistence_barcode(reduced_persistence, axes=axes[1])  # type: ignore

    plt.tight_layout()
    plt.show()


def plot_density(tensor: np.ndarray, n_bins: int, vector_density: np.ndarray) -> None:
    x, y = tensor.T

    u, v = np.mgrid[
        int(x.min()) : int(x.max()) : n_bins * 1j,  # type: ignore
        int(y.min()) : int(y.max()) : n_bins * 1j,  # type: ignore
    ]

    kernel_density = kde(tensor.T)(np.vstack([u.flatten(), v.flatten()]))

    plt.figure(figsize=(18, 10))
    fig = gds.GridSpec(3, 6)

    plt.subplot(fig[0, 0:2])
    plt.title("Data Scatter Plot")
    plt.plot(x, y, "ko")
    plt.xticks([])
    plt.yticks([])

    plt.subplot(fig[0, 2:4])
    plt.title("Gaussian KDE")
    plt.pcolormesh(u, v, kernel_density.reshape(u.shape))
    plt.xticks([])
    plt.yticks([])

    plt.subplot(fig[0, 4:6])
    plt.title("Density Contours")
    plt.pcolormesh(u, v, kernel_density.reshape(u.shape))
    plt.contour(u, v, kernel_density.reshape(u.shape))
    plt.xticks([])
    plt.yticks([])

    axe_0 = plt.subplot(fig[1:3, 0:3], projection="3d")
    axe_0.set_title("Mapped Density over 2D Space")
    axe_0.set_xticks([])
    axe_0.set_yticks([])
    axe_0.set_zticks([])  # type: ignore
    axe_0.scatter(u, v, kernel_density.reshape(u.shape), s=2, c="lightblue")  # type: ignore
    axe_0.set_xlabel("x Coordinate")
    axe_0.set_ylabel("y Coordinate")
    axe_0.set_zlabel("Density Value")  # type: ignore

    axe_1 = plt.subplot(fig[1:3, 3:6], projection="3d")
    axe_1.set_title("Density Estimate over 2D Space")
    axe_1.set_xticks([])
    axe_1.set_yticks([])
    axe_1.set_zticks([])  # type: ignore
    axe_1.scatter(x, y, vector_density.reshape(x.shape), s=2, c="lightgrey")  # type: ignore
    axe_1.set_xlabel("x Coordinate")
    axe_1.set_ylabel("y Coordinate")
    axe_1.set_zlabel("Density Value")  # type: ignore

    plt.tight_layout()
    plt.show()


def plot_clusters(
    values: np.ndarray, clusters: list[list[int]], centroids: list[int]
) -> None:
    plt.figure(figsize=(18, 4))

    plt.subplot(1, 2, 1)
    plt.title("Initial Data")
    plt.scatter(values[:, 0], values[:, 1], c="lightgrey")
    plt.xticks([])
    plt.yticks([])

    plt.subplot(1, 2, 2)
    plt.title("Clustered Data")

    for index, label in enumerate(clusters):
        plt.scatter(values[label, 0], values[label, 1], label=f"Cluster {index}")

    plt.scatter(
        values[centroids, 0],
        values[centroids, 1],
        c="black",
        marker="x",
        label="Centroids",
    )

    plt.legend(loc="best")
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()
    plt.show()
