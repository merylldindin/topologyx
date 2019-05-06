# Author:  DINDIN Meryll
# Date:    26/06/2018
# Project: TdaToolbox

try: from filtration.imports import *
except: from imports import *

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
