import numpy as np
import math

def train(xList):
   N = len(xList) #number of train data

   #reshape each train vector to 1xm matrix
   arr = []
   for x in xList: arr.append(x.reshape((-1, 1)))

   #create the B matrix
   B = np.concatenate(arr, axis=1)

   #subtract row mean to create A matrix
   row_mean = np.mean(B, axis=1)
   A = B - row_mean.reshape((-1, 1))

   #use SVD to train our PCA
   u, s, vh = np.linalg.svd(A)

   return A, row_mean, u, (s**2 / N) #because S matrix has square root of the eigenvalues and we do not divide 1/n in the A matrix
   
def getScoreMat(A, uList):
   uRowMat = np.concatenate([u.reshape((1,-1)) for u in uList], axis=0)
   return np.dot(uRowMat, A)

def score(mu, uList, scoreMat, Y):
   yHat = Y - mu
   w = np.array([np.dot(yHat, u) for u in uList])
   #score: min distance with each column in the score matrix
   scores = []
   for column in range(scoreMat.shape[1]):
      distance = math.sqrt(np.sum((w - scoreMat[:,column])**2))
      scores.append(distance)
   return min(scores)
