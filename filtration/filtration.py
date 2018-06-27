# Author: DINDIN Meryll
# Date: 27/06/2018
# Project: TDAToolbox

from filtration.toolbox import *

# Computes associated persistent objects

class Filtration: 

    # Initialisation
    def __init__(self, vec):

        # Dimension for simplex construction
        self.vec = vec
        self.num = vec.shape[0]
        self.dim = vec.shape[1]
        # Creates the complex
        alpha = gudhi.AlphaComplex(points=self.vec)
        # Save as attribute
        self.alp = alpha.create_simplex_tree(max_alpha_square=250.0)
        # Memory efficiency
        del alpha

    # Create the KDTree out of points
    def KDT(self, leaf_size=30, metric='euclidean'):

        self.kdt = KDTree(self.vec, leaf_size=leaf_size, metric=metric)
    
    # Computes the distance to the first neighbors corresponding to the points
    def KNN(self, pts, neighbors):

        return self.kdt.query(pts, neighbors, return_distance=True)

    # Computes the DTM corresponding to the given points
    def DTM(self, pts, neighbors):

        tmp = np.square(self.KNN(pts, neighbors)[0])

        return np.sqrt(np.sum(tmp, axis=1) / neighbors)

    # Defines the maximum value of the DTM discretization of a segment
    def max_segment(self, p, q, divisions, neighbors):

        stp = (q - p) / float(divisions)
        dim = len(p)
        pts = np.zeros((divisions+1, dim))
        for i in range(divisions): pts[i,:] = p + i*stp
        pts[divisions,:] = q
        
        return max(self.DTM(pts, neighbors))

    # Defines the maximum value of the DTM discretization of a triangle
    def max_triangle(self, p, q, r, divisions, neighbors):

        pts = []
        for alpha in range(divisions):
            for beta in range(divisions - alpha):
                gamma = divisions - alpha - beta
                pts.append((alpha*p + beta*q + gamma*r) / float(divisions))
                pts.append(p)
                pts.append(q)
                pts.append(r)

        return max(self.DTM(np.asarray(pts), neighbors))

    # DTM filtration thanks to the Rips algorithm
    def DTM_filter(self, neighbors=2, divisions=5, verbose=False):

        # Create the Rips complex
        self.KDT()
        # Defines the filtration
        fil = gudhi.SimplexTree()
        vtx = self.DTM(self.vec, neighbors)
        # Log
        if verbose: print('Max DTM Values = {}'.format(np.max(vtx)))
        # Create the filtration
        r_f = self.alp.get_filtration()
        for spx in r_f:
            if len(spx[0]) == 1: 
                fil.insert(spx[0], filtration=vtx[spx[0][0]])
            elif len(spx[0]) == 2: 
                val = self.max_segment(self.vec[spx[0][0],:], 
                                       self.vec[spx[0][1],:], 
                                       divisions, neighbors)
                fil.insert(spx[0], filtration=val)
            elif len(spx[0]) == 3:
                val = self.max_triangle(self.vec[spx[0][0],:], 
                                        self.vec[spx[0][1],:], 
                                        self.vec[spx[0][2],:], 
                                        divisions, neighbors)
                fil.insert(spx[0], filtration=val)
        # Initialize the filtration
        fil.initialize_filtration()
        self.dtm = fil
        del fil, vtx

    # Sublevel filtration
    def SUB_filter(self, neighbors=5):

        # Create the Rips complex
        self.KDT()
        # Defines the filtration
        fil = gudhi.SimplexTree()
        vtx = self.DTM(self.vec, neighbors)
        # Defines the new filtration
        fil = gudhi.SimplexTree()
        r_f = self.alp.get_filtration()
        # Apply incremental filtration
        for ele in r_f:
            val = max(ele[1], max([vtx[i] for i in ele[0]]))
            fil.insert(ele[0], filtration=val)
        # Save as attribute
        fil.set_dimension(self.dim)
        fil.initialize_filtration()
        self.sub = fil
        # Memory efficiency
        del fil, vtx

    # Computes the persistence of a given filtration
    def persistence(self, neighbors=5, alp=True, sub=True, dtm=True):

        # Launch the filtration
        if sub: self.SUB_filter(neighbors=neighbors)
        if dtm: self.DTM_filter(neighbors=neighbors)
        # Compute the persistences
        if alp: self.alp.persistence()
        if sub: self.sub.persistence()
        if dtm: self.dtm.persistence()

    # Computes the landscapes given a persistence
    def relative_landscapes(self, n_landscapes=10, alp=True, sub=True, dtm=True):
        
        # Computes the persistences
        self.persistence(alp=alp, sub=sub, dtm=dtm)

        lcd = []
        if alp:
            tmp = np.asarray([[ele[0], ele[1][0], ele[1][1]] for ele in self.alp.persistence() if ele[1][1] < np.inf])
            a_1 = [val[1:] for val in tmp[np.where(tmp[:,0] == 1)[0]]]
            lcd.append(build_landscapes(a_1, n_landscapes, self.num, np.min(a_1), np.max(a_1)))
            a_2 = [val[1:] for val in tmp[np.where(tmp[:,0] == 2)[0]]]
            lcd.append(build_landscapes(a_2, n_landscapes, self.num, np.min(a_2), np.max(a_2)))
            del tmp, a_1, a_2
        if sub:
            tmp = np.asarray([[ele[0], ele[1][0], ele[1][1]] for ele in self.sub.persistence() if ele[1][1] < np.inf])
            s_0 = [val[1:] for val in tmp[np.where(tmp[:,0] == 0)[0]]]
            lcd.append(build_landscapes(s_0, n_landscapes, self.num, np.min(s_0), np.max(s_0)))
            s_1 = [val[1:] for val in tmp[np.where(tmp[:,0] == 1)[0]]]
            lcd.append(build_landscapes(s_1, n_landscapes, self.num, np.min(s_1), np.max(s_1)))
            del tmp, s_0, s_1
        if dtm:
            tmp = np.asarray([[ele[0], ele[1][0], ele[1][1]] for ele in self.dtm.persistence() if ele[1][1] < np.inf])
            d_0 = [val[1:] for val in tmp[np.where(tmp[:,0] == 0)[0]]]
            lcd.append(build_landscapes(d_0, n_landscapes, self.num, np.min(d_0), np.max(d_0)))
            d_1 = [val[1:] for val in tmp[np.where(tmp[:,0] == 1)[0]]]
            lcd.append(build_landscapes(d_1, n_landscapes, self.num, np.min(d_1), np.max(d_1)))
            del tmp, d_0, d_1

        return np.asarray(lcd)

    # Defines the associated persistent image, relative to specific filtration
    def relative_images(self, var, filtration='alp', resolution=(50, 50), graph=False):

        # Computes the persistence first
        if filtration == 'alp': 
            self.persistence(sub=False, dtm=False)
            diag_0 = self.alp.persistence_intervals_in_dimension(0)
            diag_1 = self.alp.persistence_intervals_in_dimension(1)
        if filtration == 'sub': 
            self.persistence(alp=False, dtm=False)
            diag_0 = self.sub.persistence_intervals_in_dimension(0)
            diag_1 = self.sub.persistence_intervals_in_dimension(1)
        if filtration == 'dtm': 
            self.persistence(alp=False, sub=False)
            diag_0 = self.dtm.persistence_intervals_in_dimension(0)
            diag_1 = self.dtm.persistence_intervals_in_dimension(1)

        # Filtrates the infinite values
        diag_0 = np.asarray([ele for ele in diag_0 if ele[1] < np.inf])
        diag_1 = np.asarray([ele for ele in diag_1 if ele[1] < np.inf])
        # Pivotes the diagonal
        diag_0[:,1] = diag_0[:,1] - np.sum(diag_0, axis=1)/2
        diag_1[:,1] = diag_1[:,1] - np.sum(diag_1, axis=1)/2
        # Defines the extrema along each axis
        mx0, my0 = max(diag_0[:,0]), max(diag_0[:,0])/2
        mx1, my1 = max(diag_1[:,0]), max(diag_1[:,0])/2

        # Defines the image
        img_0 = np.zeros(resolution)
        for point in diag_0: img_0 += surface(point, mx0, my0)
        img_1 = np.zeros(resolution)
        for point in diag_1: img_1 += surface(point, mx1, my1)

        # Display if asked
        if graph:
            plt.figure(figsize=(18,6))
            fig = gd.GridSpec(1, 3)
            plt.subplot(fig[0,0])
            if filtration == 'alp': gudhi.plot_persistence_diagram(self.alp.persistence())
            if filtration == 'sub': gudhi.plot_persistence_diagram(self.sub.persistence())
            if filtration == 'dtm': gudhi.plot_persistence_diagram(self.dtm.persistence())
            plt.subplot(fig[0,1])
            plt.imshow(img_0)
            plt.subplot(fig[0,2])
            plt.imshow(img_1)
            plt.tight_layout()
            plt.show()

        return [img_0, img_1]

    # Visualisation given specific points
    def visual(self):

        # Computes the landscapes
        lcd = self.relative_landscapes()
        # Visualisation
        plt.figure(figsize=(18,10))
        fig = gds.GridSpec(5, 3)
        plt.subplot(fig[0,:])
        for ele in self.vec.transpose(): plt.plot(ele)
        plt.subplot(fig[1:3,0])
        gudhi.plot_persistence_diagram(self.alp.persistence())
        plt.subplot(fig[1:3,1])
        gudhi.plot_persistence_diagram(self.sub.persistence())
        plt.subplot(fig[1:3,2])
        gudhi.plot_persistence_diagram(self.dtm.persistence())
        plt.subplot(fig[3,0])
        for ele in lcd[0]: plt.plot(ele)
        plt.subplot(fig[4,0])
        for ele in lcd[1]: plt.plot(ele)
        plt.subplot(fig[3,1])
        for ele in lcd[2]: plt.plot(ele)
        plt.subplot(fig[4,1])
        for ele in lcd[3]: plt.plot(ele)
        plt.subplot(fig[3,2])
        for ele in lcd[4]: plt.plot(ele)
        plt.subplot(fig[4,2])
        for ele in lcd[5]: plt.plot(ele)
        plt.tight_layout()
        plt.show()
