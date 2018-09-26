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
   F = np.zeros((N, M))
   G = np.zeros((N, M))

   #init
   for i in range(N):
      G[i,0] = 0
      F[i,0] = 0

   for j in range(M):
      G[0,j] = j
      s = 0
      for n in range(0, j): s+=gapPenalty(n)
      F[0,j] = s

   #dynamic program
   for i in range(1, N):
      for j in range(1, M):
         c1 = F[i-1, j-1] + subScore(seq1[i], seq2[j])
         c2 = F[i-1, j] + gapPenalty(G[i-1, j])
         c3 = F[i, j-1] + gapPenalty(G[i, j-1])
         F[i,j] = max(c1, c2, c3)
         if F[i,j] == c1: G[i,j] = 0
         if F[i,j] == c2: G[i,j] = G[i-1, j] + 1
         if F[i,j] == c3: G[i,j] = G[i, j-1] + 1
         print("F[%d, %d] = %d" % (i, j, F[i,j]))

   return F[N-1, M-1]

def getSeq(seq):
   s = []
   for c in seq: s.append(OBSER.index(c))
   return s

if __name__ == '__main__':
   seq1 = 'EJG'
   seq2 = 'GEECG'
   seq3 = 'CGJEE'
   seq4 = 'JJGECCG'
   print(getOptimalScore(getSeq(seq1), getSeq(seq2)))
   print(getOptimalScore(getSeq(seq2), getSeq(seq1)))
   raise Exception("done")
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


