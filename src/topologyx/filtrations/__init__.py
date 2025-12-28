from enum import Enum
from typing import Protocol

import gudhi
import numpy as np
from sklearn.neighbors import KDTree


class SimplexTreeProtocol(Protocol):
    """Protocol defining the interface for gudhi SimplexTree objects."""

    def persistence(self) -> list[tuple[int, tuple[float, float]]]: ...
    def persistence_intervals_in_dimension(
        self, dimension: int
    ) -> list[tuple[float, float]]: ...
    def insert(self, simplex: list[int], filtration: float = 0.0) -> bool: ...
    def set_dimension(self, dimension: int) -> None: ...
    def initialize_filtration(self) -> None: ...


from topologyx.filtrations.utils import (
    build_betti_curve,
    build_persistence_image,
    build_persistence_landscape,
    plot_betti_curves,
    plot_persistence_landscapes,
    plot_persistences,
)


class FiltrationType(Enum):
    DTM = "dtm"
    SIMPLE = "simple"
    SUBLEVEL = "sublevel"


class Filtration:
    def __init__(
        self,
        vector: np.ndarray,
        use_alpha: bool = True,
        leaf_size: int = 30,
    ) -> None:
        self.vector = vector
        self.kd_tree = KDTree(self.vector, leaf_size=leaf_size, metric="euclidean")

        if use_alpha:
            self.simplex = gudhi.AlphaComplex(points=self.vector)  # type: ignore
            self.simplex = self.simplex.create_simplex_tree(max_alpha_square=250.0)

        else:
            self.simplex = gudhi.SimplexTree()  # type: ignore

            if vector.shape[1] == 1:
                for i in np.arange(len(vector)):
                    self.simplex.insert([i], filtration=vector[i])

                for i in np.arange(len(vector) - 1):
                    self.simplex.insert([i, i + 1], filtration=vector[i])

            elif vector.shape[1] == 2:
                for index in range(len(vector)):
                    self.simplex.insert([index], filtration=-vector[index, 1])

                    for neighbor in self.kd_tree.query(
                        [vector[index, :]], 5, return_distance=False
                    )[0][1:]:
                        self.simplex.insert(
                            [index, neighbor],
                            filtration=np.mean(
                                [-vector[index, 1], -vector[neighbor, 1]]
                            ),
                        )

            elif vector.shape[1] == 3:
                for index in range(len(vector)):
                    self.simplex.insert([index], filtration=-vector[index, 2])

                    for neighbor in self.kd_tree.query(
                        [vector[index, :]], 5, return_distance=False
                    )[0][1:]:
                        self.simplex.insert(
                            [index, neighbor],
                            filtration=np.mean(
                                [-vector[index, 2], -vector[neighbor, 2]]
                            ),
                        )

            else:
                raise ValueError("Dimension not supported")

            self.simplex.initialize_filtration()

    def get_density_estimate(self, points: np.ndarray, n_neighbors: int) -> np.ndarray:
        neighbors = self.kd_tree.query(points, n_neighbors, return_distance=True)

        return np.sqrt(np.sum(np.square(neighbors[0]), axis=1) / n_neighbors)

    def get_vertexes(self, n_neighbors: int) -> np.ndarray:
        return self.get_density_estimate(self.vector, n_neighbors)

    def apply_sublevel_filtration(self, n_neighbors: int = 5) -> SimplexTreeProtocol:
        simplex = gudhi.SimplexTree()  # type: ignore
        vertexes = self.get_vertexes(n_neighbors)

        for pair in self.simplex.get_filtration():  # type: ignore
            simplex.insert(
                pair[0],
                filtration=max(pair[1], max(vertexes[i] for i in pair[0])),  # type: ignore
            )

        simplex.set_dimension(self.vector.shape[1])
        simplex.initialize_filtration()
        simplex.persistence()

        return simplex

    def compute_segment_maximum_density(
        self,
        p: np.ndarray,
        q: np.ndarray,
        n_divisions: int,
        n_neighbors: int,
    ) -> float:
        step = (q - p) / float(n_divisions)
        points = np.zeros((n_divisions + 1, len(p)))

        for i in range(n_divisions):
            points[i, :] = p + i * step

        points[n_divisions, :] = q

        return max(self.get_density_estimate(points, n_neighbors))

    def compute_triangle_maximum_density(
        self,
        p: np.ndarray,
        q: np.ndarray,
        r: np.ndarray,
        n_divisions: int,
        n_neighbors: int,
    ) -> float:
        points = []
        for alpha in range(n_divisions):
            for beta in range(n_divisions - alpha):
                gamma = n_divisions - alpha - beta

                points.append(
                    [(alpha * p + beta * q + gamma * r) / float(n_divisions), p, q, r]
                )

        return max(self.get_density_estimate(np.asarray(points), n_neighbors))

    def apply_dtm_filtration(
        self, n_neighbors: int = 5, n_divisions: int = 5
    ) -> SimplexTreeProtocol:
        simplex = gudhi.SimplexTree()  # type: ignore
        vertexes = self.get_vertexes(n_neighbors)

        for pair in self.simplex.get_filtration():  # type: ignore
            if len(pair[0]) == 1:
                simplex.insert(pair[0], filtration=vertexes[pair[0][0]])

            elif len(pair[0]) == 2:
                simplex.insert(
                    pair[0],
                    filtration=self.compute_segment_maximum_density(
                        self.vector[pair[0][0], :],
                        self.vector[pair[0][1], :],
                        n_divisions,
                        n_neighbors,
                    ),
                )

            elif len(pair[0]) == 3:
                simplex.insert(
                    pair[0],
                    filtration=self.compute_triangle_maximum_density(
                        self.vector[pair[0][0], :],
                        self.vector[pair[0][1], :],
                        self.vector[pair[0][2], :],
                        n_divisions,
                        n_neighbors,
                    ),
                )

            else:
                raise ValueError("Dimension not supported")

        simplex.set_dimension(self.vector.shape[1])
        simplex.initialize_filtration()
        simplex.persistence()

        return simplex

    def build_persistence_diagram(
        self, filtration_type: FiltrationType | None = None, dimension: int = 0
    ) -> None:
        simplex_tree: SimplexTreeProtocol = self.simplex  # type: ignore[assignment]

        match filtration_type:
            case FiltrationType.DTM:
                simplex_tree = self.apply_dtm_filtration()
            case FiltrationType.SUBLEVEL:
                simplex_tree = self.apply_sublevel_filtration()
            case _:
                simplex_tree.persistence()

        self.simplex = np.asarray(
            [
                [interval[0], interval[1]]
                for interval in simplex_tree.persistence_intervals_in_dimension(
                    dimension
                )
                if interval[1] < np.inf
            ]
        )

    def betti_curve(
        self,
        minimum: float | None = None,
        maximum: float | None = None,
        n_points: int = 100,
    ) -> np.ndarray:
        return build_betti_curve(
            self.simplex,
            minimum=minimum,
            maximum=maximum,
            n_points=n_points,
        )

    def persistence_landscapes(
        self,
        minimum: float | None = None,
        maximum: float | None = None,
        n_landscapes: int = 10,
        n_points: int = 100,
    ) -> np.ndarray:
        return build_persistence_landscape(
            self.simplex,
            minimum=minimum,
            maximum=maximum,
            n_landscapes=n_landscapes,
            n_points=n_points,
        )

    def persistence_image(
        self,
        x_extremas: tuple[float, float] | None = None,
        y_extremas: tuple[float, float] | None = None,
        image_size: tuple[int, int] = (32, 32),
        variance: float = 1e-8,
    ) -> np.ndarray:
        return build_persistence_image(
            self.simplex,
            x_extremas,
            y_extremas,
            image_size,
            variance,
        )


class Levels:
    def __init__(self, serie: np.ndarray) -> None:
        self.upper_simplex = gudhi.SimplexTree()  # type: ignore
        self.lower_simplex = gudhi.SimplexTree()  # type: ignore

        for index in np.arange(len(serie)):
            self.upper_simplex.insert([index], filtration=serie[index])
            self.lower_simplex.insert([index], filtration=-serie[index])

        for index in np.arange(len(serie) - 1):
            self.upper_simplex.insert([index, index + 1], filtration=serie[index])
            self.lower_simplex.insert([index, index + 1], filtration=-serie[index])

        self.upper_simplex.initialize_filtration()
        self.lower_simplex.initialize_filtration()

    def build_persistence_diagram(
        self, visualize: bool = False
    ) -> tuple[
        np.ndarray,
        np.ndarray,
    ]:
        upper_persistence = self.upper_simplex.persistence()
        lower_persistence = self.lower_simplex.persistence()

        if visualize:
            plot_persistences(upper_persistence, lower_persistence)

        upper_persistence = np.asarray(
            [
                [component[1][0], component[1][1]]
                for component in upper_persistence
                if component[1][1] < np.inf
            ]
        )

        lower_persistence = np.asarray(
            [
                [component[1][0], component[1][1]]
                for component in lower_persistence
                if component[1][1] < np.inf
            ]
        )

        return upper_persistence, lower_persistence

    def betti_curves(
        self,
        upper_minimum: float | None = None,
        upper_maximum: float | None = None,
        lower_minimum: float | None = None,
        lower_maximum: float | None = None,
        n_points: int = 100,
        visualize: bool = False,
    ) -> tuple[
        np.ndarray,
        np.ndarray,
    ]:
        upper_persistence, lower_persistence = self.build_persistence_diagram(
            visualize=visualize
        )

        upper_curve = build_betti_curve(
            upper_persistence,
            minimum=upper_minimum,
            maximum=upper_maximum,
            n_points=n_points,
        )
        lower_curve = build_betti_curve(
            lower_persistence,
            minimum=lower_minimum,
            maximum=lower_maximum,
            n_points=n_points,
        )

        if visualize:
            plot_betti_curves(upper_curve, lower_curve)

        return upper_curve, lower_curve

    def persistence_landscapes(
        self,
        upper_minimum: float | None = None,
        upper_maximum: float | None = None,
        lower_minimum: float | None = None,
        lower_maximum: float | None = None,
        n_landscapes: int = 5,
        n_points: int = 100,
        visualize: bool = False,
    ) -> tuple[
        np.ndarray,
        np.ndarray,
    ]:
        upper_persistence, lower_persistence = self.build_persistence_diagram(
            visualize=visualize
        )

        upper_landscapes = build_persistence_landscape(
            upper_persistence,
            minimum=upper_minimum,
            maximum=upper_maximum,
            n_landscapes=n_landscapes,
            n_points=n_points,
        )
        lower_landscapes = build_persistence_landscape(
            lower_persistence,
            minimum=lower_minimum,
            maximum=lower_maximum,
            n_landscapes=n_landscapes,
            n_points=n_points,
        )

        if visualize:
            plot_persistence_landscapes(upper_landscapes, lower_landscapes)

        return upper_landscapes, lower_landscapes
