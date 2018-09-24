#source: https://stackoverflow.com/questions/40822400/how-to-create-a-dotplot-of-two-dna-sequence-in-python?rq=1

import numpy
import matplotlib.pyplot as plt

def makeMatrix(seq1,seq2):
   N = len(seq1)
   M = len(seq2)
   mat = numpy.zeros((M, N))
   for n in range(N):
      for m in range(M):
         if seq1[n] == seq2[m]: mat[m, n] = 1
   return mat

seqx = 'CDABBAFCDBAAEAACEDAEQCDABABABALFLBBAFBSBAAAAA'
seqy = 'AABBAFCDABAEAABCEDCDEQFCDABAAPALFBBASBAAAAA'

plt.imshow(makeMatrix(seqx,seqy))
plt.grid(True)
plt.xticks(numpy.arange(len(list(seqx))),list(seqx))
plt.yticks(numpy.arange(len(list(seqy))),list(seqy))

plt.tight_layout()
plt.show()
