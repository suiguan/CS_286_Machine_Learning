import numpy as np
import matplotlib.pyplot as plt

xorTruth = {
   (0,0):0,
   (0,1):1,
   (1,0):1,
   (1,1):0
}

def y(w0, w1, w2, w3, w4, w5, x0, x1):
   return w4*max(w0*x0+w2*x1, 0) + w5*max(w1*x0+w3*x1, 0)

def compare(w0, w1, w2, w3, w4, w5):
   for x0, x1 in xorTruth.keys():
      if y(w0,w1,w2,w3,w4,w5,x0,x1) != xorTruth[(x0,x1)]: 
         return False 
   return True

weights = [-1, 1]
for w0 in weights:
   for w1 in weights:
      for w2 in weights:
         for w3 in weights:
            for w4 in weights:
               for w5 in weights:
                  if compare(w0,w1,w2,w3,w4,w5):
                     print("XOR: w0=%d,w1=%d,w2=%d,w3=%d,w4=%d,w5=%d" % (w0,w1,w2,w3,w4,w5))


#plot a solution
w0,w1,w2,w3,w4,w5 = (-1,1,1,-1,1,1)
n = 100
x0 = np.linspace(0, 1, n)
x1 = np.linspace(0, 1, n)
red = (1, 0, 0)
blue = (0, 0, 1)
c = np.zeros((n*n, 3))
x0p = np.zeros((n*n,))
x1p = np.zeros((n*n,))
for i in range(n):
   for j in range(n):
      if y(w0,w1,w2,w3,w4,w5,x0[i],x1[j]) >= 0.5: c[i*n+j]=red 
      else: c[i*n+j] = blue
      x0p[i*n+j] = x0[i]
      x1p[i*n+j] = x1[j]
print("plotting solution for w0,w1,w2,w3,w4,w5=%s,%s,%s,%s,%s,%s" % (w0,w1,w2,w3,w4,w5))
print("graph: red = 1, blue = 0")
plt.scatter(x0p, x1p, c=c)
plt.show()
