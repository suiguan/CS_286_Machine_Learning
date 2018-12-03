import math

X1, X2, X3, X4, X5 = (8, 5, 9, 4, 7) #hardcoded data in (6.14)
XList = (X1, X2, X3, X4, X5)

def nCr(n,r):
    fact = math.factorial
    return fact(n) // fact(r) // fact(n-r)

def f(xi, theta):
   return nCr(10, xi) * math.pow(theta, xi) * math.pow(1-theta, 10-xi)
   
def pji(j, t1, theta1, t2, theta2, xi): #(6.10)
   _a = t1*f(xi, theta1)
   _b = t2*f(xi, theta2)
   if j == 1: return _a / (_a + _b)
   elif j == 2: return _b / (_a + _b)
   else: raise Exception("pji invalid j %d" % j)
   
def tj(j, t1, theta1, t2, theta2): #(6.11)
   s = 0
   for xi in XList: s += pji(j, t1, theta1, t2, theta2, xi) 
   return s/len(XList)

def uj(j, t1, theta1, t2, theta2):
   sn = 0
   sd = 0
   for xi in XList:
      sn += (pji(j, t1, theta1, t2, theta2, xi) * xi)
      sd += pji(j, t1, theta1, t2, theta2, xi)
   return sn/sd
   
#EM process

minIters = 10 #mininum iterations

#initial guess for the parameters
theta1 = 0.6 
theta2 = 0.5
t1 = 0.7
t2 = 0.3

print("initial guess:")
print("t = (%.4f, %.4f) theta = (%.4f, %.4f)" % (t1, t2, theta1, theta2)) 

iters = 0
while True:
   #re-estimate the parameters
   _t1 = tj(1, t1, theta1, t2, theta2) 
   _t2 = tj(2, t1, theta1, t2, theta2)
   _theta1 = uj(1, t1, theta1, t2, theta2)/10
   _theta2 = uj(2, t1, theta1, t2, theta2)/10

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



