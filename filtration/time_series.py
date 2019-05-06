# Author:  DINDIN Meryll
# Date:    26/06/2018
# Project: filtration

from filtration.toolbox import *

# Defines a way to deal with 1-D signals

class Levels:

    # Initialization
    # vec refers to a 1D numpy array
    def __init__(self, vec):

        # Defines the filtration
        self.simplex_up = gudhi.SimplexTree()
        self.simplex_dw = gudhi.SimplexTree()
        # Fullfill the simplexes
        for i in np.arange(len(vec)): 
            self.simplex_up.insert([i], filtration=vec[i])
            self.simplex_dw.insert([i], filtration=-vec[i])
        for i in np.arange(len(vec)-1): 
            self.simplex_up.insert([i, i+1], filtration=vec[i])
            self.simplex_dw.insert([i, i+1], filtration=-vec[i])
        # Initialize the filtrations
        self.simplex_up.initialize_filtration()
        self.simplex_dw.initialize_filtration()

    # Get both persistences from the signal
    # graph refers whether to display a graph or not
    def get_persistence(self, graph=False):

        # Computes the persistences
        dig_up = self.simplex_up.persistence()
        dig_dw = self.simplex_dw.persistence()

        if graph:
            plt.figure(figsize=(18,8))
            fig = gds.GridSpec(2,2)
            plt.subplot(fig[0,0])
            gudhi.plot_persistence_diagram(dig_up)
            plt.subplot(fig[1,0])
            gudhi.plot_persistence_barcode(dig_up)
            plt.subplot(fig[0,1])
            gudhi.plot_persistence_diagram(dig_dw)
            plt.subplot(fig[1,1])
            gudhi.plot_persistence_barcode(dig_dw)
            plt.tight_layout()
            plt.show()

        # Filters infinite values
        dig_up = np.asarray([[ele[1][0], ele[1][1]] for ele in dig_up if ele[1][1] < np.inf])
        dig_dw = np.asarray([[ele[1][0], ele[1][1]] for ele in dig_dw if ele[1][1] < np.inf])

        return dig_up, dig_dw

    # Defines the Betti curves out of the barcode diagrams
    # mnu, mnd refer to the minimal value for discretization
    # mxu, mxd refers to the maximal value for discretization
    # num_points refers to the amount of points to get as output
    # graph refers whether to display a graph or not
    def betti_curves(self, mnu=None, mxu=None, mnd=None, mxd=None, num_points=100, graph=False):

        # Compute persistence
        v,w = np.zeros(num_points), np.zeros(num_points)
        u,d = self.get_persistence(graph=False)

        if mnu and mxu and mnd and mxd:
            val_up = np.linspace(mnu, mxu, num=num_points)
            val_dw = np.linspace(mnd, mxd, num=num_points)
        else:
            mnu, mxu = np.min(u), np.max(u)
            mnd, mxd = np.min(d), np.max(d)
            val_up = np.linspace(mnu, mxu, num=num_points)
            val_dw = np.linspace(mnd, mxd, num=num_points)

        for ele in u: v += functionize(val_up, ele)
        for ele in d: w += functionize(val_dw, ele)

        # Memory efficiency
        del val_up, val_dw, u, d

        if graph:
            plt.figure(figsize=(18,3))
            plt.subplot(1,2,1)
            plt.title('Upper Levels Betti Curve')
            plt.plot(v)
            plt.xticks([])
            plt.yticks([])
            plt.subplot(1,2,2)
            plt.title('Sub Levels Betti Curve')
            plt.plot(w)
            plt.xticks([])
            plt.yticks([])
            plt.tight_layout()
            plt.show()

        return v, w

    # Defines the persistent landscapes of the diagrams
    # mnu, mnd refer to the minimal value for discretization
    # mxu, mxd refers to the maximal value for discretization
    # nb_landscapes refers to the amount of landscapes to build
    # num_points refers to the amount of points to get as output
    # graph refers whether to display a graph or not
    def landscapes(self, mnu=None, mxu=None, mnd=None, mxd=None, nb_landscapes=5, num_points=100, graph=False):
        
        # Computes the persistent landscapes for both diagrams
        u,d = self.get_persistence(graph=False)
        l_u = build_landscapes(u, nb_landscapes, num_points, mnu, mxu)
        l_d = build_landscapes(d, nb_landscapes, num_points, mnd, mxd)

        # Display landscapes if necessary
        if graph:
            plt.figure(figsize=(18,3))
            plt.subplot(1,2,1)
            plt.title('Upper Levels Persistence Landscapes')
            for ele in l_u: plt.plot(ele)
            plt.xticks([])
            plt.yticks([])
            plt.subplot(1,2,2)
            plt.title('Sub Levels Persistence Landscapes')
            for ele in l_d: plt.plot(ele)
            plt.xticks([])
            plt.yticks([])
            plt.tight_layout()
            plt.show()

        return l_u, l_d
