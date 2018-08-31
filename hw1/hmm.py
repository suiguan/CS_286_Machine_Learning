import math
import random
import numpy as np

try:
   from sys import maxint
except:
   maxint = 9223372036854775807

class HMM:
   def __init__(self, N, M, minIters, epsilon):
      self.N = N
      self.M = M
      self.minIters = minIters
      self.epsilon = epsilon
      self.oldLogProb = -maxint
      self.randomInit()

   def setupTable(self, T):
      self.c = np.zeros((T,), dtype=np.float32)
      self.alpha = np.zeros((T, self.N), dtype=np.float32)
      self.beta = np.zeros((T, self.N), dtype=np.float32)
      self.gamma = np.zeros((T, self.N), dtype=np.float32)
      self.diGamma = np.zeros((T, self.N, self.N), dtype=np.float32)

   def getRandVal(self, k): #return a random value around 1/k
      v = 1.0/k
      delta = 0.1 * v
      return v + (-delta + random.random() * 2 * delta);

   def getNorm(self, pList):
      s = sum(pList)
      norm = [float(p) / s for p in pList]
      if round(sum(norm), 6) != 1: raise Exception("invalid normalized")
      return norm

   def randomInit(self):
      #init A
      self.A = []
      for i in range(self.N):
         self.A.append([])
         for j in range(self.N):
            self.A[i].append(self.getRandVal(self.N))
         self.A[i] = self.getNorm(self.A[i])

      #init B
      self.B = []
      for i in range(self.N):
         self.B.append([])
         for j in range(self.M):
            self.B[i].append(self.getRandVal(self.M))
         self.B[i] = self.getNorm(self.B[i])

      #init PI
      self.PI = []
      for i in range(self.N): self.PI.append(self.getRandVal(self.N))
      self.PI = self.getNorm(self.PI)

      #print("randomInit A = %s" % self.A)
      #print("randomInit B = %s" % self.B)
      #print("randomInit PI = %s" % self.PI)

   def forwardPass(self, obserSeq):
      #compute a0(i)
      for t in range(len(obserSeq)):
         for i in range(self.N): 
            if t == 0:
                _a = self.PI[i] * self.B[i][obserSeq[0]]
                self.alpha[t][i] = _a
                self.c[0] += _a 
                continue
            #self.alpha[t][i] = 0
            

      # scale the a0(i)
      self.c[0] = 1 / self.c[0] 
      for i in range(self.N):
         self.alpha[0][i] = self.alpha[0][i] * self.c[0]
      
      # compute at(i)
      for t in range(1, len(obserSeq)):
         for i in range(self.N):
            for j in range(self.N):
               self.alpha[t][i] = self.alpha[t][i] + (self.alpha[t-1][j]*self.A[j][i])
            self.alpha[t][i] = self.alpha[t][i] * self.B[i][obserSeq[t]]
            self.c[t] = self.c[t] + self.alpha[t][i]

         #scale at(i)
         self.c[t] = 1 / self.c[t]
         for i in range(self.N):
             self.alpha[t][i] = self.c[t] * self.alpha[t][i]


   def backwardPass(self, obserSeq):
      T = len(obserSeq)

      #let beta_t-1(i) = 1 scaled by cT-1
      for t in range(T):
         for i in range(self.N):
            if t == T - 1:
               self.beta[t][i] = self.c[t]
               continue
            #self.beta[t][i] = 0

      #beta-pass
      for t in reversed(range(T-1)):
         for i in range(self.N):
            for j in range(self.N):
               self.beta[t][i] = self.beta[t][i] + (self.A[i][j]*self.B[j][obserSeq[t+1]]*self.beta[t+1][j])

            # scale beta_ti with same scale factor as a_ti
            self.beta[t][i] = self.beta[t][i] * self.c[t] 

   def calcGammaDigamma(self, obserSeq):
      T = len(obserSeq)
      for t in range(T - 1):
         denom = 0
         for i in range(self.N):
            #self.gamma[t][i] = 0
            for j in range(self.N):
               #self.diGamma[t][i][j] = 0
               denom = denom + (self.alpha[t][i]*self.A[i][j]*self.B[j][obserSeq[t+1]]*self.beta[t+1][j])

         for i in range(self.N):
            for j in range(self.N):
               self.diGamma[t][i][j] = (self.alpha[t][i]*self.A[i][j]*self.B[j][obserSeq[t+1]]*self.beta[t+1][j]) / denom
               self.gamma[t][i] = self.gamma[t][i] + self.diGamma[t][i][j]

      #add gamma_t-1(i)
      #self.gamma.append([])

      #special case for gamma_t-1(i)
      denom = 0
      for i in range(self.N): denom = denom + self.alpha[T-1][i]
      for i in range(self.N): self.gamma[T-1][i] = self.alpha[T-1][i] / denom


   def reEstimateModel(self, obserSeq):
      T = len(obserSeq)

      #re-estimate PI
      for i in range(self.N):
         self.PI[i] = self.gamma[0][i]

      #re-estimate A
      for i in range(self.N):
         for j in range(self.N):
            numer = 0
            denom = 0
            for t in range(T-1): 
               numer += self.diGamma[t][i][j]
               denom += self.gamma[t][i]
            if numer == 0: self.A[i][j] = 0 
            else: self.A[i][j] = numer / denom

      #re-estimate B
      for i in range(self.N):
         for j in range(self.M):
            numer = 0
            demon = 0
            for t in range(T):
               if obserSeq[t] == j: numer += self.gamma[t][i]
               denom += self.gamma[t][i]
            self.B[i][j] = numer / denom


   def getScore(self, obserSeq):
      T = len(obserSeq)
      logProb = 0
      for t in range(T): logProb += math.log(self.c[t]) 
      return -logProb


   def fit(self, obserSeq):
      if len(obserSeq) == 0: raise Exception("Cannot train HMM with empty seq")
      iters = 0
      logProb = 1 
      diff = maxint
      while iters < self.minIters or diff > self.epsilon:
         self.setupTable(len(obserSeq))
         self.forwardPass(obserSeq)
         self.backwardPass(obserSeq)
         self.calcGammaDigamma(obserSeq)
         self.reEstimateModel(obserSeq)
         logProb = self.getScore(obserSeq)
         if iters % 10 == 0: print("%d: score = %s" % (iters, logProb))
         diff = abs(logProb - self.oldLogProb)
         self.oldLogProb = logProb
         iters += 1
      return self.A, self.B, self.PI


def main():
   #hyperparameters:
   observationSet = 'abcdefghijklmnopqrstuvwxyz '
   N = 2
   M = len(observationSet)
   T = 50000
   minIterations = 20
   epsilon = 10
   numRandomInit = 2
   
   #first, read the entire txt
   print("reading the text file")
   f = open('brown.txt', 'r')
   txt = f.read()
   f.close()

   #then, prepared the observation sequence
   print("preparing the observation sequence")
   obserSeq = []
   for ch in txt:
      obser = observationSet.find(ch.lower())
      if obser >= 0: obserSeq.append(obser)
      if len(obserSeq) >= T: break

   #start training an HMM
   print("start HMM training, unique observation str = %s" % observationSet)
   print("using N = %d, M = %d, T = %d, min iterations = %d, epsilon = %s" % (N, M, T, minIterations, epsilon))

   #create an HMM
   hmm = HMM(N, M, minIterations, epsilon) 
   for i in range(numRandomInit - 1): hmm.randomInit()

   #fit the HMM with obserSeq
   A, B, PI = hmm.fit(obserSeq)

   #HMM training finished
   print("HMM training finished. Model:")
   print("====== A ======")
   for i in range(N): print("state %d = %s" % (i, A[i]))
   print("====== B ======")
   for i in range(N): print("state %d = %s" % (i, B[i]))
   print("PI = %s" % PI)

if __name__ == '__main__':
   main()
