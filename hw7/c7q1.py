#Chapter 7, Q1
#Reference: https://scikit-learn.org/stable/auto_examples/neighbors/plot_classification.html
#on 12/7/2018

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn import neighbors, datasets


#hardcoded points in Ch7, Q1
points = [(0.5, 3.00), (1.0, 4.25), (1.5, 2.00), (2.0, 2.75), (2.5, 1.65),
         (3.0, 2.70), (3.5, 1.00), (4.0, 2.50), (4.5, 2.10), (5.0, 2.75),
         (0.5, 1.75), (1.5, 1.50), (2.5, 4.00), (2.5, 2.10), (3.0, 1.50),
         (3.5, 1.85), (4.0, 3.50), (5.0, 1.45),]
X = np.array(points)

colors = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
         1, 1, 1, 1, 1, 1, 1, 1,]
y = np.array(colors)


n_neighbors = 3
h = .02  # step size in the mesh

# Create color maps
cmap_light = ListedColormap(['#FFAAAA', '#AAAAFF'])
cmap_bold = ListedColormap(['#FF0000', '#0000FF'])

for weights in ['distance']:
    # we create an instance of Neighbours Classifier and fit the data.
    clf = neighbors.KNeighborsClassifier(n_neighbors, weights=weights)
    clf.fit(X, y)

    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, x_max]x[y_min, y_max].
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure()
    plt.pcolormesh(xx, yy, Z, cmap=cmap_light)

    # Plot also the training points
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold, edgecolor='k', s=20)
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.title("2-Class classification (k = %i, weights = '%s')" % (n_neighbors, weights))

plt.show()
