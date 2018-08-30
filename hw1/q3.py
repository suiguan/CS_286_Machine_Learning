A = [[0.7, 0.3],
     [0.4, 0.6]]

B = [[0.1, 0.4, 0.5],
     [0.7, 0.2, 0.1]]

PI = [0.6, 0.4]


def getAllSeq(lis, t):
   if t < 1: raise Exception("invalid t")
   ret = []
   if t == 1:
      for l in lis:
         ret.append([l])
      return ret
   for i in range(len(lis)):
      m = lis[i]
      for s in getAllSeq(lis, t-1):
         ret.append([m] + s)
   return ret

class BruteForceHMMScoring:
   def getProb(self, stateSeq, obserSeq):
      if len(stateSeq) != len(obserSeq): raise Exception("state seq and observation seq must have same length!")
      prob = 1
      prevState = None
      for t in range(len(obserSeq)): 
         x = stateSeq[t]
         o = obserSeq[t]
         if prevState == None:
            prevState = x
            prob *= PI[x]*B[x][o]
            continue
         prob *= A[prevState][x]*B[x][o]
         prevState = x
      return prob

   def getObserProb(self, obserSeq):
      N = len(PI)
      totalProb = 0
      for stateSeq in getAllSeq(list(range(N)), len(obserSeq)):
         totalProb += self.getProb(stateSeq, obserSeq)
      return totalProb

class AlphaPassHMMScoring:
   def getObserProb(self, obserSeq):
      a = []

      #init alpha 0 for all states
      N = len(PI)
      for s in range(N): a.append(PI[s]*B[s][obserSeq[0]])

      #calculate at recusively
      for t in range(len(obserSeq)):
         if t == 0: continue
         newA = []
         for s in range(N):
            _t = 0
            for j in range(len(a)):
              _t += (a[j] * A[j][s])  
            newA.append(_t * B[s][obserSeq[t]])
         a = newA

      #return the score
      return sum(a)

def main():
   b = BruteForceHMMScoring()
   hs = AlphaPassHMMScoring()
   ts = 0
   for obser in getAllSeq([0,1,2], 4): #go through all possible observation seq with length 4
      s = round(hs.getObserProb(obser), 6)
      if s != round(b.getObserProb(obser), 6): raise Exception("alpha pass has different score than brute force for obser %s" % obser)
      #print("%s score = %s" % (obser, s))
      ts += s
   print("total score = %.6f" % ts)



if __name__ == '__main__':
   main()

