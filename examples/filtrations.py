import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # TDA on 3D Shapes

        This notebook demonstrates the use of Topological Data Analysis (TDA)
        on three-dimensional point clouds. We use height as the filtration function
        to analyze the topological features of a 3D hand shape.
        """
    )
    return


@app.cell
def _():
    import warnings

    warnings.simplefilter("ignore")
    return (warnings,)


@app.cell
def _(mo):
    mo.md(r"""## Load the 3D Point Cloud""")
    return


@app.cell
def _():
    import numpy as np

    def load_shape_file(filepath: str) -> np.ndarray:
        cloud = []
        with open(filepath, "r") as stream:
            while len(coordinates := stream.readline().split(" ")) == 3:
                cloud.append(np.asarray(coordinates).astype("float"))

        return np.vstack(cloud)

    cloud = load_shape_file("./samples/hand.off")
    return cloud, load_shape_file, np


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Build Persistence Diagram

        Extract the connected components (dimension 0) from the persistence diagram.
        """
    )
    return


@app.cell
def _():
    from topologyx.filtrations import Filtration, FiltrationType

    return Filtration, FiltrationType


@app.cell
def _(Filtration, FiltrationType, cloud):
    filtration = Filtration(cloud, use_alpha=False)
    filtration.build_persistence_diagram(
        filtration_type=FiltrationType.SIMPLE, dimension=0
    )
    return (filtration,)


@app.cell
def _(mo):
    mo.md(r"""## Compute Betti Curve""")
    return


@app.cell
def _(filtration):
    betti_curves = filtration.betti_curve()
    return (betti_curves,)


@app.cell
def _(mo):
    mo.md(r"""## Compute Persistence Landscapes""")
    return


@app.cell
def _(filtration):
    persistence_landscapes = filtration.persistence_landscapes()
    return (persistence_landscapes,)


@app.cell
def _(mo):
    mo.md(r"""## Visualization""")
    return


@app.cell
def _(betti_curves, cloud, filtration, persistence_landscapes):
    import gudhi
    import matplotlib.pyplot as plt

    diagram = [(0, tuple(e)) for e in filtration.simplex]

    fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(18, 14))
    grid = axes[0, 0].get_gridspec()

    for axe in axes[0:, 0]:
        axe.remove()

    axe_0 = fig.add_subplot(grid[0:, 0], projection="3d")
    axe_0.set_box_aspect(aspect=(1.5, 1.5, 2.75))  # type: ignore
    axe_0.set_title("Mapped 3 Dimensional Data Cloud")
    axe_0.set_xticks([])
    axe_0.set_yticks([])
    axe_0.set_zticks([])  # type: ignore
    axe_0.scatter(cloud[:, 0], cloud[:, 1], cloud[:, 2], s=2, c="coral")  # type: ignore
    axe_0.set_xlabel("x Coordinate")
    axe_0.set_ylabel("y Coordinate")
    axe_0.set_zlabel("z Coordinate")  # type: ignore

    gudhi.plot_persistence_diagram(diagram, axes=axes[0, 1])  # type: ignore

    gudhi.plot_persistence_barcode(diagram, axes=axes[1, 1])  # type: ignore

    axes[2, 1].set_title("Betti Curve")
    axes[2, 1].plot(betti_curves)

    axes[3, 1].set_title("Persistence Landscapes")
    for landscape in persistence_landscapes:
        axes[3, 1].plot(landscape)

    fig.tight_layout()
    plt.gca()
    return axes, axe_0, diagram, fig, grid, gudhi, landscape, plt


if __name__ == "__main__":
    app.run()
