# Author:  DINDIN Meryll
# Date:    26/06/2018
# Project: clustering

from clustering.union_find import *

# Defines a class aimed at generating samples for clustering

class ClusterGenerator:

    # Initialization
    # structure refers to the type of data to generate
    # n_samples refers to the amount of data to deal with
    # randomize is the random state for reproducibility
    def __init__(self, structure='blobs', n_samples=1500, randomize=42):

        self.structure = structure
        self.n_samples = n_samples
        self.randomize = randomize

    # Function aiming at generating samples
    def generate(self):

        if self.structure == 'anisotropy':

            x,y = make_blobs(n_samples=self.n_samples, random_state=self.randomize)
            vec = [[0.60834549, -0.63667341], [-0.40887718, 0.85253229]]
            return np.dot(x, vec), y

        elif self.structure == 'variances':

            std = [1.0, 2.5, 0.5]
            return make_blobs(n_samples=self.n_samples, cluster_std=std, random_state=self.randomize)

        elif self.structure == 'circles':

            return make_circles(n_samples=self.n_samples, factor=0.5, noise=0.05)

        elif self.structure == 'moons':

            return make_moons(n_samples=self.n_samples, noise=0.05)

        elif self.structure == 'random':

            return np.random.rand(self.n_samples, 2), None

        else:

            return make_blobs(n_samples=self.n_samples, random_state=self.randomize)

# Implements the ToMaTo clustering algorithm

class ToMaTo:

    # Initialization
    # x refers to the data
    # y are the labels and won't be used
    def __init__(self, x, y = None):

        self.x = x
        self.y = y

        # Vizualization requires 2D data points
        if (x.shape[1]>2):
            self.reduced = PCA(n_components=2).fit_transform(x)
            print("PCA representation created")
        self.estimate_clusters()

    # Estimate gaussian densities around the data distribution
    # nbins refers to the visualization and space mapping
    # graph is a boolean for data visualization
    def estimate_density(self, nbins=100, graph=False):

        den = kde(self.x.T)
        vec = den(np.vstack(([*self.x.T])))

        if graph:
            reduced = self.reduced if hasattr(self,'reduced') else self.x
            plot_density(self.x, reduced, nbins, den, vec)

        del den

        return vec

    # Build the simplex tree and the corresponding filtration
    # neighbors refers to the neighboring graph of each element
    # graph is a boolean for data visualization
    def estimate_clusters(self, neighbors=6, graph=False):

        vec = self.estimate_density(graph=False)

        self.kdt = KDTree(self.x, metric='euclidean')
        self.sxt = gudhi.SimplexTree()

        for ind in range(self.x.shape[0]):
            self.sxt.insert([ind], filtration=-vec[ind])
            nei = self.kdt.query([self.x[ind]], neighbors, return_distance=False)[0][1:]
            for idx in nei:
                self.sxt.insert([ind, idx], filtration=np.mean([-vec[ind], -vec[idx]]))

        self.sxt.initialize_filtration()
        self.sxt.persistence()

        if graph:

            dig, res = self.sxt.persistence(), []
            for ele in dig:
                if ele[0] == 0: res.append(ele)

            plt.figure(figsize=(18, 4))
            fig = gds.GridSpec(1, 2)
            plt.subplot(fig[0,0])
            gudhi.plot_persistence_diagram(res)
            plt.subplot(fig[0,1])
            gudhi.plot_persistence_barcode(res)
            plt.tight_layout()
            plt.show()

    # Find the clusters and their centroids
    # num_clusters refers to the guessed number of clusters
    # tau is the limitation for one cluster to be merged into another
    # neighbors refers to the neighboring graph of each element
    # graph is a boolean for data visualization
    def fit_predict(self, num_clusters=None, tau=1e-2, neighbors=6, graph=False):

        if not hasattr(self, 'sxt'): self.estimate_clusters(neighbors=neighbors, graph=graph)

        lst = np.asarray([ele[0][0] for ele in self.sxt.get_filtration() if len(ele[0]) == 1])
        fil = np.asarray([-ele[1] for ele in self.sxt.get_filtration() if len(ele[0]) == 1])
        fil = {k: v for k,v in zip(lst, fil)}

        def define_clusters(lst, fil, neighbors):

            unf = UnionFind()

            for idx in lst:
    
                grp, srt = [], np.where(lst == idx)[0][0]
                for ele in self.kdt.query([self.x[idx]], neighbors, return_distance=False)[0][1:]:
                    if np.where(lst == ele)[0][0] < srt: grp.append(ele)
                
                if len(grp) == 0:
                    unf.insert_objects([idx])
                    
                else:
                    parent = grp[np.asarray([fil[j] for j in grp]).argmax()]
                    unf.union(parent, idx)
                    for ele in grp:
                        root = unf.find(ele)
                        if root != parent and min(fil[parent], fil[root]) < fil[idx] + tau:
                            unf.union(parent, root)
                            parent = unf.find(root)

            return unf

        unf, ini = define_clusters(lst, fil, neighbors), neighbors

        while len(np.unique(list(unf.parent_pointers.values()))) > num_clusters:

            ini += 2
            unf = define_clusters(lst, fil, ini)

        self.cen, self.sts = [], []
        ind = np.asarray(list(unf.num_to_objects.values()))
        rts = np.asarray(list(unf.parent_pointers.values()))

        for ele in np.unique(rts):

            self.cen.append(unf.num_to_objects[ele])
            self.sts.append(ind[np.where(rts == ele)[0]])

        self.cen = np.asarray(self.cen)

        if graph:

            plt.figure(figsize=(18, 4))
            plt.subplot(1,2,1)
            plt.title('Initial Data')
            plt.scatter(self.x[:,0], self.x[:,1], c='lightgrey')
            plt.xticks([])
            plt.yticks([])
            plt.subplot(1,2,2)
            plt.title('Clustered Data')
            for idx, grp in enumerate(self.sts): plt.scatter(self.x[grp,0], self.x[grp,1], label='Cluster {}'.format(idx))
            plt.scatter(self.x[self.cen,0], self.x[self.cen,1], c='black', marker='x', label='Centroids')
            plt.legend(loc='best')
            plt.xticks([])
            plt.yticks([])
            plt.tight_layout()
            plt.show()

        del lst, fil, unf, ini, ind

        return rts


def plot_density(X, reduced, nbins, den, vec):
        x,y = reduced.T

        u,v = np.mgrid[x.min():x.max():nbins*1j, y.min():y.max():nbins*1j]
        # In if original data dimention > 2, the vizualization will show the 
        # density over the reduced (2D) representation of the data calculated by PCA
        # Otherwise, reduced is equal to original data
        #TODO: Change to use original density function
        val = kde(reduced.T)(np.vstack([u.flatten(), v.flatten()]))

        plt.figure(figsize=(18, 10))
        fig = gds.GridSpec(3, 6)

        plt.subplot(fig[0,0:2])
        plt.title('Data Scatter Plot')
        plt.plot(x, y, 'ko')
        plt.xticks([])
        plt.yticks([])
        plt.subplot(fig[0,2:4])
        plt.title('Gaussian KDE')
        plt.pcolormesh(u, v, val.reshape(u.shape), cmap=plt.cm.BuGn_r)
        plt.xticks([])
        plt.yticks([])
        plt.subplot(fig[0,4:6])
        plt.title('Density Contours')
        plt.pcolormesh(u, v, val.reshape(u.shape), cmap=plt.cm.BuGn_r, shading='gouraud')
        plt.contour(u, v, val.reshape(u.shape))
        plt.xticks([])
        plt.yticks([])

        ax0 = plt.subplot(fig[1:3,0:3], projection='3d')
        ax0.set_title('Mapped Density over 2D Space')
        ax0.set_xticks([])                               
        ax0.set_yticks([])                               
        ax0.set_zticks([])
        ax0.scatter(u, v, val, s=2, c='lightblue')
        ax0.set_xlabel('x Coordinate')
        ax0.set_ylabel('y Coordinate')
        ax0.set_zlabel('Density Value')

        ax1 = plt.subplot(fig[1:3,3:6], projection='3d')
        ax1.set_title('Density Estimate over 2D Space')
        ax1.set_xticks([])                               
        ax1.set_yticks([])                               
        ax1.set_zticks([])
        ax1.scatter(x, y, vec, s=2, c='lightgrey')
        ax1.set_xlabel('x Coordinate')
        ax1.set_ylabel('y Coordinate')
        ax1.set_zlabel('Density Value')

        plt.tight_layout()
        plt.show()

        del x, y, u, v, val