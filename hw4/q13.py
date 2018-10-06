import numpy as np
import math
import pca

#mean matrix u from (4.8)
mu = np.array([7.0/4, 7.0/4, 5.0/4, 2, 2, 1])

#u1, u2, from (4.10). Note: u3 is not used in the score matrix
u1 = np.array([0.1641, 0.6278, -0.2604, -0.5389, 0.4637, 0.0752])
u2 = np.array([0.2443, 0.1070, -0.8017, 0.4277, -0.1373, -0.2904])
uList = [u1, u2]

#score matrix delta from (4.12)
scoreMat =np.array([[-1.1069, 1.2794, -2.6800, 2.5076],\
                    [1.5480, 0.5484, -1.2085, -0.8879]]) 

#q13 (a)
M1 = np.array([1, -1, 1, -1, -1, 1])
M2 = np.array([-2, 2, 2, -1, -2, 2])
M3 = np.array([1, 3, 0, 1, 3, 1])
M4 = np.array([2, 3, 1, 1, -2, 0])

print("(a)");
print("score(M1) = %.4f" % pca.score(mu, uList, scoreMat, M1))
print("score(M2) = %.4f" % pca.score(mu, uList, scoreMat, M2))
print("score(M3) = %.4f" % pca.score(mu, uList, scoreMat, M3))
print("score(M4) = %.4f" % pca.score(mu, uList, scoreMat, M4))

#q13 (b)
B1 = np.array([-1, 2, 1, 2, -1, 0])
B2 = np.array([-2, 1, 2, 3, 2, 1])
B3 = np.array([-1, 3, 0, 1, 3, -1])
B4 = np.array([0, 2, 3, 1, 1, -2])

#get A matrix from benign samples
_bA, _ = pca.getAMu([B1, B2, B3, B4])

_bScoreMat = pca.getScoreMat(_bA, uList)
print("(b)")
print("benign score matrix:")
print(_bScoreMat)

#return s1, s2, isMalware
#where s1 is score against malware score mat
#where s2 is score against benign score mat
def classify(Y):
   s1 = pca.score(mu, uList, scoreMat, Y)
   s2 = pca.score(mu, uList, _bScoreMat, Y)
   return s1, s2, s1 <= s2

Y1 = np.array([1, 5, 1, 5, 5, 1])
Y2 = np.array([-2, 3, 2, 3, 0, 2])
Y3 = np.array([2, -3, 2, 3, 0 ,0])
Y4 = np.array([2, -2, 2, 2, -1, 1])
print("(c)")
s1, s2, isMalware = classify(Y1)
print("score(Y1, MalwareScoreMat) = %s, score(Y1, BenignScoreMat) = %s, classify = %s" % (s1, s2, "Malware" if isMalware else "Benign"))
s1, s2, isMalware = classify(Y2)
print("score(Y2, MalwareScoreMat) = %s, score(Y2, BenignScoreMat) = %s, classify = %s" % (s1, s2, "Malware" if isMalware else "Benign"))
s1, s2, isMalware = classify(Y3)
print("score(Y3, MalwareScoreMat) = %s, score(Y3, BenignScoreMat) = %s, classify = %s" % (s1, s2, "Malware" if isMalware else "Benign"))
s1, s2, isMalware = classify(Y4)
print("score(Y4, MalwareScoreMat) = %s, score(Y4, BenignScoreMat) = %s, classify = %s" % (s1, s2, "Malware" if isMalware else "Benign"))
    
