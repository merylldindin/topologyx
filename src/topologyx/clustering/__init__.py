from enum import Enum
from typing import Any

import gudhi
import numpy as np
from scipy.stats import gaussian_kde as kde
from sklearn.datasets import make_blobs, make_circles, make_moons
from sklearn.decomposition import PCA
from sklearn.neighbors import KDTree

from topologyx.clustering.unionfind import UnionFind
from topologyx.clustering.utils import plot_clusters, plot_density, plot_persistence


class ClusterStructure(Enum):
    ANISOTROPY = "anisotropy"
    BLOBS = "blobs"
    CIRCLES = "circles"
    MOONS = "moons"
    RANDOM = "random"
    VARIANCES = "variances"


class ClusterGenerator:
    def __init__(
        self,
        structure: ClusterStructure = ClusterStructure.BLOBS,
        n_samples: int = 1500,
        randomize: int = 42,
    ) -> None:
        self.structure = structure
        self.n_samples = n_samples
        self.randomize = randomize

    def generate(self) -> tuple[np.ndarray | None, ...]:
        match self.structure:
            case ClusterStructure.ANISOTROPY:
                x, y = make_blobs(n_samples=self.n_samples, random_state=self.randomize)  # type: ignore
                offset = [[0.60834549, -0.63667341], [-0.40887718, 0.85253229]]

                return (np.dot(x, offset), y)

            case ClusterStructure.VARIANCES:
                return make_blobs(
                    n_samples=self.n_samples,
                    cluster_std=[1.0, 2.5, 0.5],
                    random_state=self.randomize,
                )

            case ClusterStructure.CIRCLES:
                return make_circles(n_samples=self.n_samples, factor=0.5, noise=0.05)

            case ClusterStructure.MOONS:
                return make_moons(n_samples=self.n_samples, noise=0.05)

            case ClusterStructure.RANDOM:
                generator = np.random.default_rng(seed=self.randomize)

                return generator.random((self.n_samples, 2)), None

            case _:
                return make_blobs(n_samples=self.n_samples, random_state=self.randomize)


class TomatoClustering:
    def __init__(self, x: np.ndarray, y: np.ndarray | None = None) -> None:
        self.x = x
        self.y = y

        self.x_plan = PCA(n_components=2).fit_transform(x) if x.shape[1] > 2 else x

        self.estimate_clusters()

    def estimate_density(self, n_bins: int = 100, visualize: bool = False) -> Any:
        kernel_density = kde(self.x.T)
        vector_density = kernel_density(np.vstack(([*self.x.T])))

        if visualize:
            plot_density(self.x_plan, n_bins, vector_density)

        return vector_density

    def estimate_clusters(self, n_neighbors: int = 6, visualize: bool = False) -> None:
        vector_density = self.estimate_density(visualize=visualize)

        self.simplex = gudhi.SimplexTree()  # type: ignore
        self.kd_tree = KDTree(self.x, metric="euclidean")

        for index in range(self.x.shape[0]):
            self.simplex.insert([index], filtration=-vector_density[index])

            neighbors = self.kd_tree.query(
                [self.x[index]], n_neighbors, return_distance=False
            )[0][1:]

            for neighbor_index in neighbors:
                self.simplex.insert(
                    [index, neighbor_index],
                    filtration=np.mean(
                        [-vector_density[index], -vector_density[neighbor_index]]
                    ),
                )

        self.simplex.persistence()

        if visualize:
            plot_persistence(self.simplex.persistence())

    def define_clusters(
        self,
        vertexes: np.ndarray,
        n_simplexes: dict[int, np.ndarray],
        n_neighbors: int,
        tau: float = 1e-2,
    ) -> UnionFind:
        union_find = UnionFind()

        for vertex in vertexes:
            vertex_index = np.nonzero(vertexes == vertex)[0][0]

            if neighbors := [
                neighbor
                for neighbor in self.kd_tree.query(
                    [self.x[vertex]], n_neighbors, return_distance=False
                )[0][1:]
                if np.nonzero(vertexes == neighbor)[0][0] < vertex_index
            ]:
                parent = neighbors[
                    np.asarray(
                        [n_simplexes[neighbor] for neighbor in neighbors]
                    ).argmax()
                ]

                union_find.union(parent, vertex)

                for neighbor in neighbors:
                    root = union_find.find(neighbor)

                    if (
                        root != parent
                        and min(n_simplexes[parent], n_simplexes[root])  # type: ignore
                        < n_simplexes[vertex] + tau
                    ):
                        union_find.union(parent, root)
                        parent = union_find.find(root)

            else:
                union_find.insert_objects([vertex])

        return union_find

    def fit_predict(
        self,
        n_clusters: int | None = None,
        tau: float = 1e-2,
        n_neighbors: int = 6,
        visualize: bool = False,
    ) -> np.ndarray:
        if not hasattr(self, "simplex"):
            self.estimate_clusters(n_neighbors=n_neighbors, visualize=visualize)

        _vertexes, filtrations = [], []

        for simplex, filtration in self.simplex.get_filtration():
            if len(simplex) == 1:
                _vertexes.append(simplex[0])
                filtrations.append(-filtration)

        vertexes = np.asarray(_vertexes)
        n_simplexes = dict(zip(vertexes, np.asarray(filtrations)))

        neighbors_counter = n_neighbors
        union_find = self.define_clusters(vertexes, n_simplexes, n_neighbors)

        if n_clusters is not None:
            while len(np.unique(list(union_find.pointers.values()))) > n_clusters:
                neighbors_counter += 2
                union_find = self.define_clusters(
                    vertexes, n_simplexes, neighbors_counter, tau=tau
                )

        self.clusters, self.centroids = [], []

        indexes = np.asarray(list(union_find.indexes_to_objects.values()))
        pointers = np.asarray(list(union_find.pointers.values()))

        for pointer in np.unique(pointers):
            self.clusters.append(indexes[np.nonzero(pointers == pointer)[0]])
            self.centroids.append(union_find.indexes_to_objects[int(pointer)])

        if visualize:
            plot_clusters(self.x, self.clusters, self.centroids)

        return pointers
