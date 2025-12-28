import numpy as np
import pytest

from topologyx.clustering import ClusterGenerator, ClusterStructure


@pytest.fixture
def simple_2d_data() -> np.ndarray:
    """Simple 2D dataset for basic tests."""
    return np.array([[0, 0], [1, 0], [0, 1], [1, 1], [5, 5], [6, 5], [5, 6], [6, 6]])


@pytest.fixture
def blobs_data() -> tuple[np.ndarray, np.ndarray]:
    """Generate blob dataset with known structure."""
    generator = ClusterGenerator(
        structure=ClusterStructure.BLOBS, n_samples=300, randomize=42
    )
    x, y = generator.generate()
    return x, y


@pytest.fixture
def moons_data() -> tuple[np.ndarray, np.ndarray]:
    """Generate moons dataset with known structure."""
    generator = ClusterGenerator(
        structure=ClusterStructure.MOONS, n_samples=300, randomize=42
    )
    x, y = generator.generate()
    return x, y


@pytest.fixture
def circles_data() -> tuple[np.ndarray, np.ndarray]:
    """Generate circles dataset with known structure."""
    generator = ClusterGenerator(
        structure=ClusterStructure.CIRCLES, n_samples=300, randomize=42
    )
    x, y = generator.generate()
    return x, y
