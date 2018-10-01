import numpy as np
import math

#mean matrix u from (4.8)
u = np.array([7.0/4, 7.0/4, 5.0/4, 2, 2, 1])

#u1, u2, u3 from (4.10)
u1 = np.array([0.1641, 0.6278, -0.2604, -0.5389, 0.4637, 0.0752])
u2 = np.array([0.2443, 0.1070, -0.8017, 0.4277, -0.1373, -0.2904])
u3 = np.array([-0.0710, 0.2934, 0.3952, 0.3439, 0.3644, -0.7083])

#score matrix delta from (4.12)
scoreMat =np.array([[-1.1069, 1.2794, -2.6800, 2.5076],\
                    [1.5480, 0.5484, -1.2085, -0.8879]]) 

def score(Y):
   yHat = Y - u
   #only uses two most significant u1 and u2 
   w = np.array([np.dot(yHat, u1), np.dot(yHat, u2)])
   #score: min distance with each column in the score matrix
   scores = []
   for column in range(scoreMat.shape[1]):
      distance = math.sqrt(np.sum((w - scoreMat[:,column])**2))
      scores.append(distance)
   return min(scores)

Y1 = np.array([2, 3, 1, 0, 3, 2])
Y2 = np.array([-4, -5, 0, 3, 1, -2])
Y3 = np.array([2, 3, 0, 1, 3, 2])
Y4 = np.array([3, 2, 1, 0, 3, 2])

print("score(Y1) = %.2f" % score(Y1))
print("score(Y2) = %.2f" % score(Y2))
print("score(Y3) = %.2f" % score(Y3))
print("score(Y4) = %.2f" % score(Y4))

