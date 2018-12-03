#chapter 6, Q8.

import math

X1, X2, X3, X4, X5 = (8, 5, 9, 4, 7) #hardcoded data in (6.14)
XList = (X1, X2, X3, X4, X5)

#initial guess for the parameters
theta1 = 0.6 
theta2 = 0.5
t1 = 0.7
t2 = 0.3


def nCr(n,r):
    fact = math.factorial
    return fact(n) // fact(r) // fact(n-r)

def f(xi, theta):
   return nCr(10, xi) * math.pow(theta, xi) * math.pow(1-theta, 10-xi)
   
def getPji(t1, theta1, t2, theta2): #compute all pji
   pjiList = [[], []] #j = 1 or 2 
   for xi in XList: #(6.10)
      _a = t1*f(xi, theta1)
      _b = t2*f(xi, theta2)
      pjiList[0].append(_a / (_a + _b))
      pjiList[1].append(_b / (_a + _b))
   return pjiList
   
def tj(j, pjiList): #(6.11)
   if j != 1 and j != 2: raise Exception("tj: j can only be 1 or 2")
   s = 0
   for i in range(len(XList)): s += pjiList[j-1][i] 
   return s/len(XList)

def uj(j, pjiList): #(6.12)
   if j != 1 and j != 2: raise Exception("uj: j can only be 1 or 2")
   sn = 0
   sd = 0
   for i in range(len(XList)):
      xi = XList[i]
      sn += (pjiList[j-1][i] * xi)
      sd += pjiList[j-1][i]
   return sn/sd
   

#main(): EM process
print("initial guess:")
print("t = (%.4f, %.4f) theta = (%.4f, %.4f)" % (t1, t2, theta1, theta2)) 

minIters = 10 #mininum iterations
iters = 0
while True:
   #E step: compute all pji
   pjiList = getPji(t1, theta1, t2, theta2)

   #M step: re-estimate the parameters
   _t1 = tj(1, pjiList) 
   _t2 = tj(2, pjiList)
   _theta1 = uj(1, pjiList)/10 #binomial distribution with N = 10
   _theta2 = uj(2, pjiList)/10

   #Check if parameters have converged
   diff = abs(_t1 - t1) + abs(_t2 - t2) + abs(_theta1 - theta1) + abs(_theta2 - theta2)
   t1 = _t1
   t2 = _t2
   theta1 = _theta1
   theta2 = _theta2

   iters += 1
   if iters <= minIters: continue
   if diff < 0.00001: break #threshold to stop
   
print("After %d iterations, EM converged to:" % iters) 
print("t = (%.4f, %.4f) theta = (%.4f, %.4f)" % (t1, t2, theta1, theta2)) 



