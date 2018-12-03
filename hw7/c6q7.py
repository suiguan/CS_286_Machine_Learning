#chapter 6, Q7.

import math

X1, X2, X3, X4, X5 = (8, 5, 9, 4, 7) #hardcoded data in (6.14)
XList = (X1, X2, X3, X4, X5)

#After the 1st EM-Step, then parameters converged to: (Section 6.5.3)
theta1 = 0.6918
theta2 = 0.5597
t1 = 0.7593
t2 = 0.2407

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

#get all the pji values for the second E step:
pjiList = getPji(t1, theta1, t2, theta2)
print("pji probabilities for the second E step:")
for i in range(len(XList)):
   for j in range(2):
      print("p_%d,%d = %.4f" % (j+1, i+1, pjiList[j][i]))
