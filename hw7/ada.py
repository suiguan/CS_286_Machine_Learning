#Problem #1 in AdaBoost : https://www.cs.sjsu.edu/~stamp/ML/files/ada.pdf
import math

#Data in Table 2
z = [-1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1]
c0 = [1, -1, -1, -1, 1, 1, -1, -1, -1, 1, -1, 1, -1, -1, -1, -1, -1, -1, 1, 1, -1, 1, 1, 1, 1]
c1 = [-1, 1, -1, 1, -1, 1, -1, 1, 1, 1, -1, -1, 1, 1, -1, -1, -1, 1, 1, -1, 1, -1, 1, -1, -1]
c2 = [-1, 1, 1, 1, -1, 1, -1, 1, 1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, -1, -1, -1, -1, 1, -1]
c3 = [-1, 1, 1, 1, -1, -1, -1, -1, 1, 1, -1, 1, 1, -1, 1, -1, -1, 1, 1, 1, -1, 1, 1, -1, -1]
c4 = [-1, 1, 1, -1, -1, -1, 1, -1, -1, -1, 1, 1, -1, 1, 1, 1, -1, 1, -1, -1, -1, 1, -1, -1, 1]
c5 = [1, -1, 1, -1, -1, -1, 1, 1, -1, 1, 1, -1, -1, -1, 1, 1, -1, -1, -1, 1, -1, 1, 1, 1, -1]
c6 = [1, 1, -1, 1, 1, 1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, 1, 1, -1, -1, 1, -1, -1]
c7 = [-1, 1, -1, 1, -1, 1, 1, 1, -1, 1, 1, -1, -1, 1, 1, 1, -1, -1, 1, -1, 1, -1, 1, 1, -1]
c8 = [-1, -1, 1, -1, 1, -1, 1, 1, -1, 1, 1, -1, -1, -1, -1, 1, -1, 1, -1, 1, 1, 1, -1, -1, -1]
c9 = [-1, -1, -1, 1, 1, 1, 1, -1, -1, -1, 1, -1, -1, 1, 1, -1, 1, 1, 1, -1, -1, 1, -1, 1, -1]
c10 = [-1, 1, -1, -1, -1, -1, 1, -1, 1, -1, -1, 1, -1, 1, 1, 1, -1, 1, 1, -1, -1, -1, 1, 1, 1]
c11 = [1, 1, -1, 1, -1, -1, -1, -1, 1, -1, -1, -1, 1, -1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1]
c12 = [1, -1, -1, -1, 1, 1, -1, 1, -1, 1, 1, -1, 1, 1, 1, 1, -1, 1, -1, -1, -1, 1, -1, 1, 1]
c13 = [-1, 1, -1, 1, -1, 1, 1, -1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 1, 1, 1, -1, -1, 1, -1]
c14 = [1, 1, 1, -1, 1, 1, -1, -1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1, 1, -1, 1, -1, 1, 1]
c15 = [1, 1, -1, 1, 1, -1, 1, 1, -1, 1, -1, -1, -1, 1, -1, -1, 1, -1, 1, -1, -1, -1, -1, 1, 1]
c16 = [-1, -1, -1, -1, 1, 1, 1, -1, 1, -1, -1, -1, -1, 1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1]
c17 = [-1, 1, 1, 1, -1, -1, -1, 1, 1, -1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1, 1, -1, 1, -1, 1]
c18 = [1, -1, -1, 1, 1, -1, -1, 1, -1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, -1, 1, -1, -1, -1]
c19 = [1, -1, -1, -1, -1, 1, 1, -1, 1, 1, -1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, -1]
c20 = [-1, 1, 1, -1, -1, 1, 1, 1, -1, -1, -1, 1, 1, 1, 1, -1, 1, -1, -1, -1, -1, 1, -1, 1, 1]
c21 = [-1, 1, 1, -1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, -1, -1, 1, 1, 1, 1, 1, -1]
c22 = [1, -1, -1, -1, 1, -1, 1, 1, 1, -1, -1, 1, -1, -1, -1, 1, -1, 1, -1, 1, -1, -1, -1, 1, -1]
c23 = [1, 1, -1, 1, 1, -1, -1, -1, 1, 1, -1, -1, -1, -1, 1, 1, -1, 1, -1, 1, -1, -1, 1, 1, -1]
c24 = [-1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, -1, -1, -1, -1, -1, 1, 1, 1, 1, -1, -1, 1, 1]
c25 = [1, 1, -1, 1, -1, 1, 1, -1, -1, 1, 1, -1, 1, 1, 1, 1, 1, -1, -1, 1, 1, 1, -1, 1, -1]
c26 = [-1, -1, 1, -1, 1, -1, -1, 1, 1, 1, -1, -1, 1, 1, -1, -1, -1, -1, 1, 1, 1, 1, -1, 1, -1]
c27 = [-1, 1, -1, 1, 1, 1, -1, -1, 1, 1, -1, 1, 1, 1, 1, 1, 1, -1, 1, 1, -1, -1, 1, -1, 1]
c28 = [1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, 1, 1, -1, 1, -1]
c29 = [1, 1, -1, 1, 1, 1, -1, -1, -1, 1, -1, -1, 1, -1, 1, 1, -1, -1, 1, 1, 1, 1, 1, -1, -1]
cs = [c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19, c20, c21, c22, c23, c24, c25, c26, c27, c28, c29]

def sign(s):
   if s < 0: return -1
   else: return 1

def hits(c, z, numX):
   h = 0
   for xi in range(numX):
      if sign(c[xi]) == z[xi]: h += 1
   return h

def ada(cs, z, numX): #Algorithm 3.1: AdaBoost
   L = len(cs) 

   #initialize
   Cm = []
   for xi in range(numX): Cm.append(0)
   uj = []
   for j in range(L): uj.append(0)

   CmList = []
   #repeat ada boost
   for m in range(L):
      wi = []
      for xi in range(numX): wi.append(math.exp(-z[xi]*Cm[xi]))
      W = sum(wi)
      W2 = None
      t = None
      for j in range(L):
         if uj[j] == 0: #classifer cj has not yet been used
            subWi = []
            for xi in range(numX):
               if z[xi] != cs[j][xi]: subWi.append(wi[xi])
            Y = sum(subWi)
            if W2 == None or Y < W2:
               W2 = Y
               t = j

      if t == None: raise Exception("Not found t!")
      km = cs[t]
      uj[t] = 1 #marks classifer cj as used
      rm = W2/W
      am = (0.5)*math.log((1-rm)/rm)
      for xi in range(numX):
         Cm[xi] = Cm[xi] + (am*km[xi])

      #We can return earlier if hits already == numX
      #numHits = hits(Cm, z, numX) 

      #keep all intermediate Cm
      CmList.append(list(Cm))

   #return
   return CmList


#main(): for this problem we just need the print in ada()
numX = len(z)
CmList = ada(cs, z, numX)

subset = None #print only subset [3,4, etc...] of the Classifiers, set to None to print all

#print the result Table
msg = "zi\t"
for i in range(len(CmList)): 
   if subset == None or i in subset: msg += ("C%d\t" % (i+1,))
msg += "\n\n"
for xi in range(numX):
   msg += "%+d\t" % z[xi]
   for i, cm in enumerate(CmList): 
      if subset == None or i in subset: msg += ("%+.4f\t" % cm[xi])
   msg += "\n"

msg += "\nHits\t"
for i, cm in enumerate(CmList): 
   if subset == None or i in subset: msg += ("%d\t" % hits(cm, z, numX))
msg += "\n"

#print
print(msg)




