import numpy as np
import math
import pca

#mean matrix u from (4.8)
mu = np.array([7.0/4, 7.0/4, 5.0/4, 2, 2, 1])

#u1, u2, u3 from (4.10)
u1 = np.array([0.1641, 0.6278, -0.2604, -0.5389, 0.4637, 0.0752])
u2 = np.array([0.2443, 0.1070, -0.8017, 0.4277, -0.1373, -0.2904])
u3 = np.array([-0.0710, 0.2934, 0.3952, 0.3439, 0.3644, -0.7083])

#score matrix delta from (4.12)
scoreMat =np.array([[-1.1069, 1.2794, -2.6800, 2.5076],\
                    [1.5480, 0.5484, -1.2085, -0.8879]]) 

Y1 = np.array([2, 3, 1, 0, 3, 2])
Y2 = np.array([-4, -5, 0, 3, 1, -2])
Y3 = np.array([2, 3, 0, 1, 3, 2])
Y4 = np.array([3, 2, 1, 0, 3, 2])

print("score(Y1) = %.4f" % pca.score(mu, [u1,u2], scoreMat, Y1))
print("score(Y2) = %.4f" % pca.score(mu, [u1,u2], scoreMat, Y2))
print("score(Y3) = %.4f" % pca.score(mu, [u1,u2], scoreMat, Y3))
print("score(Y4) = %.4f" % pca.score(mu, [u1,u2], scoreMat, Y4))

