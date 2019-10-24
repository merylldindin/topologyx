# Author:  DINDIN Meryll
# Date:    26/06/2018
# Project: TdaToolbox

try: from filtration.utils import *
except: from utils import *

# Computes associated persistent objects

class Filtration: 

    # Initialisation
    # vec refers to the multidimensional input vector
    # use_alpha refers whether to use an AlphaComplex or not
    # leaf_size refers to the size of the KDTree to be used
    def __init__(self, vec, use_alpha=True, leaf_size=30):

        self.vec = vec
        # KDTree for easy access
        self.kdt = KDTree(self.vec, leaf_size=leaf_size, metric='euclidean')

        # Creates the complex
        if use_alpha:
            self.fil = gudhi.AlphaComplex(points=self.vec)
            self.fil = self.fil.create_simplex_tree(max_alpha_square=250.0)
        else:
            self.fil = gudhi.SimplexTree()
            # Insert elements
            if vec.shape[1] == 1:
                for i in np.arange(len(vec)): 
                    self.fil.insert([i], filtration=vec[i])
                for i in np.arange(len(vec)-1): 
                    self.fil.insert([i, i+1], filtration=vec[i])
            if vec.shape[1] == 2:
                for ind in range(len(vec)):
                    self.fil.insert([ind], filtration=-vec[ind,1])
                    nei = self.kdt.query([vec[ind,:]], 5, return_distance=False)[0][1:]
                    for idx in nei: self.fil.insert([ind, idx], filtration=np.mean([-vec[ind,1], -vec[idx,1]]))
            if vec.shape[1] == 3:
                for ind in range(len(vec)):
                    self.fil.insert([ind], filtration=-vec[ind,2])
                    nei = self.kdt.query([vec[ind,:]], 5, return_distance=False)[0][1:]
                    for idx in nei: self.fil.insert([ind, idx], filtration=np.mean([-vec[ind,2], -vec[idx,2]]))
            # Initialize the filtration
            self.fil.initialize_filtration()

    # Computes the corresponding vertexes
    # neighbors refers to the amount of corresponding neighbors in the graph
    def vertexes(self, neighbors):

        tmp = np.square(self.kdt.query(self.vec, neighbors, return_distance=True)[0])
        return np.sqrt(np.sum(tmp, axis=1) / neighbors)

    # Sublevel filtration
    # neighbors refers to the amount of corresponding neighbors in the graph
    def sub_filtration(self, neighbors=5):

        # Defines the filtration
        fil = gudhi.SimplexTree()
        vtx = self.vertexes(neighbors)
        r_f = self.fil.get_filtration()

        # Apply incremental filtration
        for spx in r_f:
            fil.insert(spx[0], filtration=max(spx[1], max([vtx[i] for i in spx[0]])))

        # Memory efficiency
        del vtx, r_f
        # Save as attribute
        fil.set_dimension(self.vec.shape[1])
        fil.initialize_filtration()
        fil.persistence()
        
        return fil

    # DTM filtration thanks to the Rips algorithm
    def dtm_filtration(self, neighbors=5, divisions=5) :

        # Defines the filtration
        fil = gudhi.SimplexTree()
        vtx = self.vertexes(neighbors)
        r_f = self.fil.get_filtration()

        # Computes the DTM corresponding to the given points
        def DTM(pts, neighbors):

            tmp = self.kdt.query(pts, neighbors, return_distance=True)
            tmp = np.square(tmp[0])

            return np.sqrt(np.sum(tmp, axis=1) / neighbors)

        # Defines the maximum value of the DTM discretization of a segment
        def max_segment(p, q, divisions, neighbors) :

            stp = (q - p) / float(divisions)
            dim = len(p)
            pts = np.zeros((divisions+1, dim))
            for i in range(divisions) : pts[i,:] = p + i*stp
            pts[divisions, :] = q
            
            return max(DTM(pts, neighbors))

        # Defines the maximum value of the DTM discretization of a triangle
        def max_triangle(p, q, r, divisions, neighbors) :

            pts = []
            for alpha in range(divisions):
                for beta in range(divisions - alpha):
                    gamma = divisions - alpha - beta
                    pts.append((alpha*p + beta*q + gamma*r) / float(divisions))
                    pts.append(p)
                    pts.append(q)
                    pts.append(r)

            return max(DTM(np.asarray(pts), neighbors))

        # Create the filtration
        for spx in r_f :

            if len(spx[0]) == 1 : 
                fil.insert(spx[0], filtration=vtx[spx[0][0]])
            elif len(spx[0]) == 2 : 
                val = max_segment(self.vec[spx[0][0], :], self.vec[spx[0][1], :], divisions, neighbors)
                fil.insert(spx[0], filtration=val)
            elif len(spx[0]) == 3 :
                val = max_triangle(self.vec[spx[0][0], :], self.vec[spx[0][1], :], self.vec[spx[0][2], :], divisions, neighbors)
                fil.insert(spx[0], filtration=val)

        # Memory efficiency
        del vtx, r_f
        # Initialize the filtration
        fil.set_dimension(self.vec.shape[1])
        fil.initialize_filtration()
        fil.persistence()

        return fil

    # Compute the graph persistence
    # type_filtration refers to the type of persistence to be computed
    # dimension refers to dimension focus and diagram extraction
    def persistence(self, type_filtration=None, dimension=0):

        if type_filtration is None: self.fil.persistence()
        if type_filtration == 'sublevel': self.fil = self.sub_filtration()
        if type_filtration == 'dtm': self.fil = self.dtm_filtration()

        self.fil = self.fil.persistence_intervals_in_dimension(dimension)
        self.fil = np.asarray([[ele[0], ele[1]] for ele in self.fil if ele[1] < np.inf])

    # Defines the Betti curves out of the barcode diagrams
    # m_n, m_x refer to the minimal value for discretization
    # num_points refers to the amount of points to get as output
    def betti_curve(self, m_n=None, m_x=None, num_points=100):

        # Aims at barcode discretization
        def functionize(val, descriptor):

            def dirichlet(x):
                return 1 if (x > descriptor[0]) and (x < descriptor[1]) else 0
    
            return np.vectorize(dirichlet)(val)

        # Compute persistence
        res = np.zeros(num_points)
        if m_n is None: m_n = np.min(self.fil)
        if m_x is None: m_x = np.max(self.fil)
        val = np.linspace(m_n, m_x, num=num_points)
        for ele in self.fil: res += functionize(val, ele)
        # Memory efficiency
        del val

        return res

    # Defines the persistent landscapes of the diagrams
    # m_n, m_x refer to the minimal value for discretization
    # nb_landscapes refers to the amount of landscapes to build
    # num_points refers to the amount of points to get as output
    def landscapes(self, m_n=None, m_x=None, nb_landscapes=10, num_points=100):

        # Prepares the discretization
        ldc = np.zeros((nb_landscapes, num_points))
        if m_n is None: m_n = np.min(self.fil)
        if m_x is None: m_x = np.max(self.fil)
        stp = np.linspace(m_n, m_x, num=num_points)

        # Use the triangular functions
        for idx, ele in enumerate(stp):
            val = []
            for pair in self.fil:
                b, d = pair[0], pair[1]
                if (d+b)/2.0 <= ele <= d: val.append(d - ele)
                elif  b <= ele <= (d+b)/2.0: val.append(ele - b)
            val.sort(reverse=True)
            val = np.asarray(val)
            for j in range(nb_landscapes):
                if (j < len(val)): ldc[j, idx] = val[j]
            del val

        # Memory efficiency
        del stp

        return ldc

    # Build a persistence image out of a dimension-specific diagram
    # m_n is a tuple refering to the extremas of the x-axis
    # m_x is a tuple refering to the extremas of the y-axis
    # image_size refers to the number of pixels to be consituting the image
    # variance refers to the gaussian dispersion
    def imagify(self, m_n=None, m_x=None, image_size=(32, 32), variance=1e-8):

        dig = self.fil.copy()
        img = np.zeros(image_size)
        dig[:,1] = dig[:,1] - np.sum(dig, axis=1)/2
        if m_n is None: mnx, mxx = np.min(dig[:,0]), np.max(dig[:,0])
        else: mnx, mxx = m_n
        if m_x is None: mny, mxy = np.min(dig[:,1]), np.max(dig[:,1])
        else: mny, mxy = m_x

        def weight(point, extrema):

            if point[1] <= 0: return 0
            else: return point[1] / extrema

        def gaussian_value(point, mean, var):

            coe = 1.0 / (2*np.pi*var)
            com = np.exp(-(np.square(point[0]-mean[0])+np.square(point[1]-mean[1]))/(2*var))

            return coe*com

        def gaussian_kernel(point, mnx, mxx, mny, mxy, image_size, var=1e-8):

            # Discretization
            x = np.linspace(mnx, mxx, image_size[0])
            y = np.linspace(mny, mxy, image_size[1])
            img = np.zeros(image_size)

            # Value filling
            for i in range(len(x)):
                for j in range(len(y)):
                    val = gaussian_value([x[i], y[j]] , point, var)
                    val = val * weight(point, mxy)
                    img[len(y)-1-j, i] = val

            return img

        for point in dig: img += gaussian_kernel(point, mnx, mxx, mny, mxy, image_size, var=variance)

        return img
