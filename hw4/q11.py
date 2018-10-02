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


#(q4-11-a)
X1 = np.array([2,-1,0,1,1,-3,5,2])
X2 = np.array([-2,3,2,3,0,2,-1,1])
X3 = np.array([-1,3,3,1,-1,4,5,2])
X4 = np.array([3,-1,0,3,2,-1,3,0])
A, mu, u, eigVal = train([X1, X2, X3, X4])
print("eigenvalues = %s" % eigVal)


#(q4-11-b)
significantIdx = [0, 1, 2] #select the indexes of the significant eigenvalues from the trained PCA 
uList = []
for idx in significantIdx: uList.append(u[:,idx]) 
scoreMat = getScoreMat(A, uList)

Y1 = np.array([1,5,1,5,5,1,1,3])
Y2 = np.array([-2,3,2,3,0,2,-1,1])
Y3 = np.array([2,-3,2,3,0,0,2,-1])
Y4 = np.array([2,-2,2,2,-1,1,2,2])
print("score(Y1) = %s" % score(mu, uList, scoreMat, Y1))
print("score(Y2) = %s" % score(mu, uList, scoreMat, Y2))
print("score(Y3) = %s" % score(mu, uList, scoreMat, Y3))
print("score(Y4) = %s" % score(mu, uList, scoreMat, Y4))
