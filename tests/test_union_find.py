from topologyx.clustering.unionfind import UnionFind


def test_empty_initialization() -> None:
    uf = UnionFind()

    assert uf.weights == {}
    assert uf.pointers == {}
    assert uf.indexes_to_objects == {}
    assert uf.objects_to_indexes == {}


def test_find_creates_new_element() -> None:
    uf = UnionFind()

    result = uf.find("a")

    assert result == "a"
    assert "a" in uf.objects_to_indexes
    assert uf.weights[0] == 1
    assert uf.pointers[0] == 0


def test_find_returns_same_element_for_singleton() -> None:
    uf = UnionFind()
    uf.find("a")

    result = uf.find("a")

    assert result == "a"


def test_find_with_integer_objects() -> None:
    uf = UnionFind()

    result = uf.find(42)

    assert result == 42
    assert 42 in uf.objects_to_indexes


def test_find_with_tuple_objects() -> None:
    uf = UnionFind()

    result = uf.find((1, 2))

    assert result == (1, 2)
    assert (1, 2) in uf.objects_to_indexes


def test_union_two_elements() -> None:
    uf = UnionFind()
    uf.find("a")
    uf.find("b")

    uf.union("a", "b")

    assert uf.find("a") == uf.find("b")


def test_union_preserves_larger_set_as_root() -> None:
    uf = UnionFind()
    uf.find("a")
    uf.find("b")
    uf.find("c")
    uf.union("a", "b")

    uf.union("a", "c")

    root = uf.find("a")
    assert uf.find("b") == root
    assert uf.find("c") == root


def test_union_idempotent() -> None:
    uf = UnionFind()
    uf.find("a")
    uf.find("b")
    uf.union("a", "b")

    uf.union("a", "b")

    assert uf.find("a") == uf.find("b")


def test_union_three_sets() -> None:
    uf = UnionFind()
    for i in range(6):
        uf.find(i)

    uf.union(0, 1)
    uf.union(2, 3)
    uf.union(4, 5)

    assert uf.find(0) == uf.find(1)
    assert uf.find(2) == uf.find(3)
    assert uf.find(4) == uf.find(5)
    assert uf.find(0) != uf.find(2)
    assert uf.find(0) != uf.find(4)
    assert uf.find(2) != uf.find(4)


def test_union_merges_sets() -> None:
    uf = UnionFind()
    for i in range(4):
        uf.find(i)

    uf.union(0, 1)
    uf.union(2, 3)
    uf.union(1, 2)

    root = uf.find(0)
    assert uf.find(1) == root
    assert uf.find(2) == root
    assert uf.find(3) == root


def test_insert_multiple_objects() -> None:
    uf = UnionFind()

    uf.insert_objects(["a", "b", "c"])

    assert "a" in uf.objects_to_indexes
    assert "b" in uf.objects_to_indexes
    assert "c" in uf.objects_to_indexes
    assert len(uf.objects_to_indexes) == 3


def test_insert_objects_creates_singletons() -> None:
    uf = UnionFind()

    uf.insert_objects([1, 2, 3])

    assert uf.find(1) == 1
    assert uf.find(2) == 2
    assert uf.find(3) == 3


def test_path_compression_on_find() -> None:
    uf = UnionFind()
    for i in range(5):
        uf.find(i)

    uf.union(0, 1)
    uf.union(1, 2)
    uf.union(2, 3)
    uf.union(3, 4)

    root = uf.find(4)

    idx_4 = uf.objects_to_indexes[4]
    assert uf.pointers[idx_4] == uf.objects_to_indexes[root]


def test_weighted_union_attaches_smaller_to_larger() -> None:
    uf = UnionFind()
    for i in range(10):
        uf.find(i)

    for i in range(1, 5):
        uf.union(0, i)

    uf.find(9)
    uf.union(0, 9)

    root = uf.find(0)
    assert uf.find(9) == root


def test_union_same_element() -> None:
    uf = UnionFind()
    uf.find("a")

    uf.union("a", "a")

    assert uf.find("a") == "a"


def test_many_elements() -> None:
    uf = UnionFind()
    n = 1000

    for i in range(n):
        uf.find(i)

    for i in range(0, n - 1, 2):
        uf.union(i, i + 1)

    for i in range(0, n - 1, 2):
        assert uf.find(i) == uf.find(i + 1)


def test_chain_unions() -> None:
    uf = UnionFind()
    n = 100

    for i in range(n):
        uf.find(i)

    for i in range(n - 1):
        uf.union(i, i + 1)

    root = uf.find(0)
    for i in range(n):
        assert uf.find(i) == root
