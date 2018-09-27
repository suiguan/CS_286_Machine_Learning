import numpy as np 
OBSER = 'EGCJ'
SUBMATRIX = np.array([[9, -4, 2, 2], [-4, 9, -5, -5], [2, -5, 10, 7], [2, -5, 7, 10]])

def subScore(x, y):
   return SUBMATRIX[x, y]

def gapPenalty(n):
   return -3 * n

def getOptimalScore(seq1, seq2):
   N = len(seq1)
   M = len(seq2)
   F = np.zeros((N+1, M+1))
   G = np.zeros((N+1, M+1))

   #init
   for i in range(N+1):
      G[i,0] = 0
      F[i,0] = 0

   for j in range(M+1):
      G[0,j] = j
      s = 0
      for n in range(1, j+1): s+=gapPenalty(n)
      F[0,j] = s

   #dynamic program
   for i in range(1, N+1):
      for j in range(1, M+1):
         c1 = F[i-1, j-1] + subScore(seq1[i-1], seq2[j-1])
         c2 = F[i-1, j] + gapPenalty(G[i-1, j])
         c3 = F[i, j-1] + gapPenalty(G[i, j-1])
         F[i,j] = max(c1, c2, c3)
         if F[i,j] == c1: G[i,j] = 0
         elif F[i,j] == c2: G[i,j] = G[i-1, j] + 1
         elif F[i,j] == c3: G[i,j] = G[i, j-1] + 1
         else: raise Exception("Impossible")

   return F[N, M]

def getSeq(seq):
   s = []
   for c in seq: s.append(OBSER.index(c))
   return s

if __name__ == '__main__':
   seq1 = 'EJG'
   seq2 = 'GEECG'
   seq3 = 'CGJEE'
   seq4 = 'JJGECCG'
   seqs = [seq1, seq2, seq3, seq4]
   scores = []
   for i in range(len(seqs)):
      scores.append([])
      for j in range(len(seqs)):
         if i == j: 
            scores[i].append(None)
            continue
         scores[i].append(getOptimalScore(getSeq(seqs[i]), getSeq(seqs[j])))
   
   #print the pairwise score table
   msg = '  \t'
   for i in range(len(seqs)): msg += '%d    \t' % i
   msg += '\n'
   for i in range(len(seqs)):
      msg += '%d \t' % i
      for j in range(len(seqs)):
         if scores[i][j] == None: msg += '  -  \t'
         else: msg += '%.3f\t' % scores[i][j] 
      msg += '\n'
   print(msg) 

