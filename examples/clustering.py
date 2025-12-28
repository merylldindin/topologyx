import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    # ToMaTo Clustering Algorithm

    Implementation of the ToMaTo clustering algorithm, presented by Steve Oudot
    in "Persistence Theory: From Quiver Representations to Data Analysis".

    ## Concept

    The algorithm exploits topological data analysis for clustering. Given a
    two-dimensional dataset, the sublevels filtration of the simplex tree built
    over the density estimate gives, by reconstruction of the connected components,
    the hierarchical relation between the data points.

    By sorting it, we can retrace the density extrema and thus the centroids.
    Visualized persistence gives a good indication of the number of centroids.
    Once determined, the construction of distinct sets through UnionFind becomes possible.

    ## Algorithm

    ![ToMaTo Algorithm](./figures/tomato.png)
    """)
    return


@app.cell
def _():
    import warnings

    warnings.simplefilter("ignore")
    return


@app.cell
def _():
    from topologyx.clustering import (
        ClusterGenerator,
        ClusterStructure,
        TomatoClustering,
    )

    return ClusterGenerator, ClusterStructure, TomatoClustering


@app.cell
def _(mo):
    mo.md(r"""
    ## Example 1: Anisotropic Distribution
    """)
    return


@app.cell
def _(ClusterGenerator, ClusterStructure, TomatoClustering):
    generator_aniso = ClusterGenerator(
        structure=ClusterStructure.ANISOTROPY, randomize=20
    )
    tomato_aniso = TomatoClustering(*generator_aniso.generate())
    _ = tomato_aniso.estimate_clusters(visualize=True)
    _ = tomato_aniso.fit_predict(n_clusters=3, visualize=True)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Example 2: Two Moons
    """)
    return


@app.cell
def _(ClusterGenerator, ClusterStructure, TomatoClustering):
    generator_moons = ClusterGenerator(structure=ClusterStructure.MOONS, randomize=18)
    tomato_moons = TomatoClustering(*generator_moons.generate())
    _ = tomato_moons.estimate_clusters(visualize=True)
    _ = tomato_moons.fit_predict(n_clusters=2, visualize=True)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Example 3: Blobs
    """)
    return


@app.cell
def _(ClusterGenerator, ClusterStructure, TomatoClustering):
    generator_blobs = ClusterGenerator(structure=ClusterStructure.BLOBS, randomize=28)
    tomato_blobs = TomatoClustering(*generator_blobs.generate())
    _ = tomato_blobs.estimate_clusters(visualize=True)
    _ = tomato_blobs.fit_predict(n_clusters=2, visualize=True)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Example 4: Random Distribution
    """)
    return


@app.cell
def _(ClusterGenerator, ClusterStructure, TomatoClustering):
    generator_random = ClusterGenerator(structure=ClusterStructure.RANDOM, randomize=30)
    tomato_random = TomatoClustering(*generator_random.generate())
    _ = tomato_random.estimate_clusters(n_neighbors=10, visualize=True)
    _ = tomato_random.fit_predict(n_clusters=6, tau=0.001, visualize=True)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Example 5: Concentric Circles
    """)
    return


@app.cell
def _(ClusterGenerator, ClusterStructure, TomatoClustering):
    generator_circles = ClusterGenerator(
        structure=ClusterStructure.CIRCLES, randomize=60
    )
    tomato_circles = TomatoClustering(*generator_circles.generate())
    _ = tomato_circles.estimate_clusters(n_neighbors=25, visualize=True)
    _ = tomato_circles.fit_predict(n_clusters=2, tau=1.0, visualize=True)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
