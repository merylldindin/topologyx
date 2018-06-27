# Author: DINDIN Meryll
# Date: 26/06/2018
# Project: TDAToolbox

from filtration.imports import *

# Aims at barcode discretization
# val refers to a 1D numpy array
# descriptor is the considered pair of the persistence diagram

def functionize(val, descriptor):

    # Temporary function
    def dirichlet(x):
        return 1 if (x > descriptor[0]) and (x < descriptor[1]) else 0

    # Vectorized function
    fun = np.vectorize(dirichlet)

    return fun(val)

# Automated construction of the landscapes
# n_landscapes refers to the amount of landscapes to build
# num_points refers to the amount of points to get as output
# m_n, m_x refer to the extrema for discretization

def build_landscapes(dig, nb_landscapes, num_points, m_n, m_x):

    # Prepares the discretization
    lcd = np.zeros((nb_landscapes, num_points))

    # Observe whether absolute or relative
    if m_n and m_x:
        stp = np.linspace(m_n, m_x, num=num_points)
    else:
        m_n, m_x = np.min(dig), np.max(dig)
        stp = np.linspace(m_n, m_x, num=num_points)

    # Use the triangular functions
    for idx, ele in enumerate(stp):
        val = []
        for pair in dig:
            b, d = pair[0], pair[1]
            if (d+b)/2.0 <= ele <= d: val.append(d - ele)
            elif  b <= ele <= (d+b)/2.0: val.append(ele - b)
        val.sort(reverse=True)
        val = np.asarray(val)
        for j in range(nb_landscapes):
            if (j < len(val)): lcd[j, idx] = val[j]

    return lcd

# Time delay embedded procedure
# val refers to a 1D time-serie
# step corresponds to the time-delay
# dimension is the dimension of the time-delay embedding
# point_size refers to the dimensionnial plot
# graph is a boolean, whether we want to display the result

def vectorize(val, step, dimension=3, point_size=1, graph=False):

    # Working on matrix
    m_i = np.arange(dimension)*(step+1)
    m_j = np.arange(np.max(val.shape[0]-(dimension-1)*(step+1), 0))
    val = val[m_i + m_j.reshape(-1,1)]
    # Memory efficiency
    del m_i, m_j

    if graph:
        # Display
        if dimension == 2:
            plt.figure(figsize=(18,4))
            plt.title('Vectorized Signal')
            plt.scatter(val[:,0], val[:,1], c='grey', marker='x')
            plt.grid()
            plt.show()

        elif dimension == 3:
            lay = go.Layout(margin=dict(l=0, r=0, b=0, t=0))
            img = go.Scatter3d(x=val[:,0], y=val[:,1], z=val[:,2], mode='markers',
                               marker=dict(size=point_size), opacity=0.5)
            fig = tools.make_subplots(rows=1, cols=1)
            fig['data'].append(img)
            pyo.iplot(fig)

    return val