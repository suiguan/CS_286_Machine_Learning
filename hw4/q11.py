import numpy as np
import pca

#(q4-11-a)
X1 = np.array([2,-1,0,1,1,-3,5,2])
X2 = np.array([-2,3,2,3,0,2,-1,1])
X3 = np.array([-1,3,3,1,-1,4,5,2])
X4 = np.array([3,-1,0,3,2,-1,3,0])
A, mu, u, eigVal = pca.train([X1, X2, X3, X4])
print("eigenvalues = %s" % eigVal)

#(q4-11-b)
significantIdx = [0, 1, 2] #select the indexes of the significant eigenvalues from the trained PCA 
print("using only significant eigenvalues: %s" % [eigVal[e] for e in significantIdx])
uList = []
for idx in significantIdx: uList.append(u[:,idx]) 
scoreMat = pca.getScoreMat(A, uList)
print("scoreMat = %s" % scoreMat)

Y1 = np.array([1,5,1,5,5,1,1,3])
Y2 = np.array([-2,3,2,3,0,2,-1,1])
Y3 = np.array([2,-3,2,3,0,0,2,-1])
Y4 = np.array([2,-2,2,2,-1,1,2,2])
print("score(Y1) = %s" % pca.score(mu, uList, scoreMat, Y1))
print("score(Y2) = %s" % pca.score(mu, uList, scoreMat, Y2))
print("score(Y3) = %s" % pca.score(mu, uList, scoreMat, Y3))
print("score(Y4) = %s" % pca.score(mu, uList, scoreMat, Y4))
