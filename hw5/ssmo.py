import random
import numpy as np 

def _f(X, train_data, lamdas, b):
   n = len(train_data)
   s = 0
   for k in range(n):
      Xk = train_data[k][0]
      zk = train_data[k][1]
      s += (lamdas[k]*zk*np.dot(Xk, X))
   s += b
   return s

#SSMO: simplified version of SMO (assume i,j selections is given) to train a SVM
#Inputs:
#train_data: list of training data (X_i, z_i), 
#  where X_i is a np.array of the feature vector, z_i is label +1/-1
#C: regularization parameter > 0
#e: numerical tolerance
#patterns: list of selected indices (i, j) with i != j to be used in the SSMO 
#  if patterns is an INT: then i,j will be selected the following way:
#  "patterns" number of paris: i from 0 ... n-1, j random. Re-select j if i == j
#maxIters: max number of iterations, each iterations go through all (i,j) in patterns
def ssmo(train_data, C, e, patterns, maxIters):
   if C <= 0 or e <= 0: raise Exception("Invalid C %s or e %s" % (C, e))

   n = len(train_data)

   #initialize
   lamdas = []
   for i in range(n): lamdas.append(0)
   b = 0

   #random init patterns if (i,j) list is not given
   if type(patterns) == int:
      if patterns <= 0: raise Exception("Invalid patterns %d" % patterns)
      _p = []
      while len(_p) < patterns:
         for i in range(n):
            j = i 
            while j == i: j = random.randint(0, n-1)
            _p.append((i,j))
            if len(_p) >= patterns: break
      patterns = _p


   iters = 0
   while True: #repeat
      updated=False

      #select (i,j) and i!=j
      for i, j in patterns:
         if i == j: raise Exception("Invalid i %d == j %d" % (i,j))
         Xi = train_data[i][0]
         Xj = train_data[j][0]
         zi = train_data[i][1]
         zj = train_data[j][1]
         d = (2*np.dot(Xi, Xj)) - np.dot(Xi, Xi) - np.dot(Xj, Xj) 

         if abs(d) <= e: continue

         updated = True
         Ei = _f(Xi, train_data, lamdas, b) - zi 
         Ej = _f(Xj, train_data, lamdas, b) - zj 
         _lamda_i = lamdas[i]
         _lamda_j = lamdas[j]
         lamdas[j] -= (zj*(Ei-Ej)/d)
         if zi == zj:
            l = max(0, lamdas[i] + lamdas[j] - C)
            h = min(C, lamdas[i] + lamdas[j])
         else:
            l = max(0, lamdas[j] - lamdas[i])
            h = min(C, C + lamdas[j] - lamdas[i])
         if lamdas[j] > h: lamdas[j] = h
         #if lamdas[j] >= l and lamdas[j] <= h: lamdas[j] = lamdas[j]
         if lamdas[j] < l: lamdas[j] = l
         lamdas[i] += (zi*zj*(_lamda_j - lamdas[j]))
         bi = b - Ei - (zi*(lamdas[i] - _lamda_i)*np.dot(Xi, Xi)) - (zj*(lamdas[j] - _lamda_j)*np.dot(Xi, Xj))
         bj = b - Ej - (zi*(lamdas[i] - _lamda_i)*np.dot(Xi, Xj)) - (zj*(lamdas[j] - _lamda_j)*np.dot(Xj, Xj))
         if lamdas[i] > 0 and lamdas[i] < C: b = bi
         if lamdas[j] > 0 and lamdas[j] < C: b = bj
         else: b = (bi + bj) / 2
         
      if not updated or iters >= maxIters: break
      iters += 1

   #return
   return lamdas, b

def getSepEq(train_data, lamdas, b):
   ws = []
   feature_dim = train_data[0][0].shape[0]
   for k in range(feature_dim): ws.append(0)
   for i in range(len(train_data)):
      Xi = train_data[i][0]
      zi = train_data[i][1]
      for k in range(feature_dim): ws[k] += (lamdas[i]*zi*Xi[k])

   eq = ""
   for k in range(feature_dim): eq += ("%+.3f(x_%d) " % (ws[k], k))
   eq += (" %+.3f = 0" % b)
   return eq

if __name__ == '__main__':
   #train data from q15.
   train_data = [(np.array([3,3]), 1), (np.array([3,4]), 1), (np.array([2,3]), 1), (np.array([1,1]), -1), (np.array([1,3]), -1), (np.array([2,2]), -1), ]

   #run ssmo
   C = 2.5
   e = 0.00001
   #patterns from q15a, since it is 0-based, so pair index is 1 less what is in the book Ch-SVM: q15
   patterns = [(0,1), (1,2), (2,3), (3,4), (4,5), #row1
               (0,2), (1,3), (2,4), (3,5), #row2
               (0,3), (1,4), (2,5), #row3
               (0,4), (1,5), #row4
               (0,5), #row5
               (1,0), (2,1), (3,2), (4,3), (5,4), #row6
               (2,0), (3,1), (4,2), (5,3), #row7
               (3,0), (4,1), (5,2), #row 8
               (4,0), (5,1), #row 9
               (5,0), #row 10
              ]

   #q15-(a)
   print("q15-(a):")
   lamdas, b = ssmo(train_data, C, e, patterns, 10) 
   print("lambdas 1 to %d = %s" % (len(lamdas), lamdas))
   print("b = %s" % b)
   print("separation plane formula: %s" % getSepEq(train_data, lamdas, b))

   print("\n")

   #q15-(b)
   print("q15-(b):")
   lamdas, b = ssmo(train_data, C, e, 1000, 10) 
   print("lambdas 1 to %d = %s" % (len(lamdas), lamdas))
   print("b = %s" % b)
   print("separation plane formula: %s" % getSepEq(train_data, lamdas, b))
