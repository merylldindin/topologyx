import numpy as np

from topologyx.clustering import TomatoClustering


def test_tomato_initialization(simple_2d_data: np.ndarray) -> None:
    tomato = TomatoClustering(simple_2d_data)

    assert tomato.x is not None
    assert tomato.x.shape == (8, 2)
    assert tomato.y is None
    assert hasattr(tomato, "simplex")
    assert hasattr(tomato, "kd_tree")


def test_tomato_initialization_with_labels(
    blobs_data: tuple[np.ndarray, np.ndarray],
) -> None:
    x, y = blobs_data

    tomato = TomatoClustering(x, y)

    assert tomato.y is not None
    assert len(tomato.y) == len(tomato.x)


def test_estimate_density(simple_2d_data: np.ndarray) -> None:
    tomato = TomatoClustering(simple_2d_data)

    density = tomato.estimate_density()

    assert density is not None
    assert len(density) == len(simple_2d_data)
    assert all(d > 0 for d in density)


def test_estimate_clusters_creates_simplex_tree(simple_2d_data: np.ndarray) -> None:
    tomato = TomatoClustering(simple_2d_data)

    tomato.estimate_clusters(n_neighbors=3)

    assert hasattr(tomato, "simplex")
    assert hasattr(tomato, "kd_tree")


def test_fit_predict_returns_cluster_assignments(simple_2d_data: np.ndarray) -> None:
    tomato = TomatoClustering(simple_2d_data)

    pointers = tomato.fit_predict(n_clusters=2)

    assert pointers is not None
    assert len(pointers) == len(simple_2d_data)


def test_fit_predict_with_n_clusters(simple_2d_data: np.ndarray) -> None:
    tomato = TomatoClustering(simple_2d_data)

    pointers = tomato.fit_predict(n_clusters=2)
    unique_clusters = np.unique(pointers)

    assert len(unique_clusters) <= 2


def test_fit_predict_creates_clusters_and_centroids(simple_2d_data: np.ndarray) -> None:
    tomato = TomatoClustering(simple_2d_data)

    tomato.fit_predict(n_clusters=2)

    assert hasattr(tomato, "clusters")
    assert hasattr(tomato, "centroids")
    assert len(tomato.clusters) == len(tomato.centroids)


def test_tomato_blobs_clustering(blobs_data: tuple[np.ndarray, np.ndarray]) -> None:
    x, y = blobs_data

    tomato = TomatoClustering(x, y)
    pointers = tomato.fit_predict(n_clusters=3)

    unique_clusters = np.unique(pointers)
    assert len(unique_clusters) <= 3
    assert len(tomato.clusters) <= 3


def test_tomato_moons_clustering(moons_data: tuple[np.ndarray, np.ndarray]) -> None:
    x, y = moons_data

    tomato = TomatoClustering(x, y)
    pointers = tomato.fit_predict(n_clusters=2)

    unique_clusters = np.unique(pointers)
    assert len(unique_clusters) <= 2


def test_tomato_circles_clustering(circles_data: tuple[np.ndarray, np.ndarray]) -> None:
    x, y = circles_data

    tomato = TomatoClustering(x, y)
    pointers = tomato.fit_predict(n_clusters=2, n_neighbors=15, tau=0.5)

    unique_clusters = np.unique(pointers)
    assert len(unique_clusters) <= 2


def test_fit_predict_with_custom_tau(simple_2d_data: np.ndarray) -> None:
    tomato = TomatoClustering(simple_2d_data)

    pointers = tomato.fit_predict(n_clusters=2, tau=0.1)

    assert pointers is not None
    assert len(pointers) == len(simple_2d_data)


def test_fit_predict_with_custom_n_neighbors(simple_2d_data: np.ndarray) -> None:
    tomato = TomatoClustering(simple_2d_data)

    pointers = tomato.fit_predict(n_clusters=2, n_neighbors=3)

    assert pointers is not None
    assert len(pointers) == len(simple_2d_data)


def test_define_clusters_returns_unionfind(simple_2d_data: np.ndarray) -> None:
    tomato = TomatoClustering(simple_2d_data)

    _vertexes, filtrations = [], []
    for simplex, filtration in tomato.simplex.get_filtration():
        if len(simplex) == 1:
            _vertexes.append(simplex[0])
            filtrations.append(-filtration)

    vertexes = np.asarray(_vertexes)
    n_simplexes = dict(zip(vertexes, np.asarray(filtrations)))

    union_find = tomato.define_clusters(vertexes, n_simplexes, n_neighbors=3)

    assert union_find is not None
    assert len(union_find.objects_to_indexes) > 0


def test_x_plan_is_2d_for_high_dimensional_data() -> None:
    high_dim_data = np.random.default_rng(42).random((100, 10))

    tomato = TomatoClustering(high_dim_data)

    assert tomato.x_plan.shape == (100, 2)


def test_x_plan_unchanged_for_2d_data(simple_2d_data: np.ndarray) -> None:
    tomato = TomatoClustering(simple_2d_data)

    np.testing.assert_array_equal(tomato.x_plan, simple_2d_data)
