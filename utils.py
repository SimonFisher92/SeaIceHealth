import numpy as np
from matplotlib.colors import ListedColormap


def random_discrete_cmap(num_colors):
    np.random.seed(42)
    colors = np.random.rand(num_colors, 3)
    np.random.shuffle(colors)
    cmap = ListedColormap(colors)
    #must start with white
    cmap.colors[0] = [1, 1, 1]
    return cmap