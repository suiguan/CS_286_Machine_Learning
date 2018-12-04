#chapter 6, Q13.

import numpy as np
import math
import matplotlib.pyplot as plt

#initial guess for the parameters
u1 = np.array([[2.5], [65.0]]) 
s1 = np.array([[1.0, 5.0], [5.0, 100.0]])

u2 = np.array([[3.5], [70.0]]) 
s2 = np.array([[2.0, 10.0], [10.0, 200.0]])

thetas = [[u1, s1], [u2, s2]]
taus = [0.6, 0.4]

#hardcoded old faithful data with (duration, wait) in Table 6.6
xData = [
   np.array([[3.6], [79]]), np.array([[1.8], [54]]), np.array([[2.283], [62]]), np.array([[3.333], [74]]), np.array([[2.883], [55]]),
   np.array([[4.533], [85]]), np.array([[1.95], [51]]), np.array([[1.833], [54]]), np.array([[4.7], [88]]), np.array([[3.6], [85]]),
   np.array([[1.6], [52]]), np.array([[4.35], [85]]), np.array([[3.917], [84]]), np.array([[4.2], [78]]), np.array([[1.75], [62]]),
   np.array([[1.8], [51]]), np.array([[4.7], [83]]), np.array([[2.167], [52]]), np.array([[4.8], [84]]), np.array([[1.75], [47]]),
] 

#helper functions
def checkThetas(thetas):
   for idx, (uj, sj) in enumerate(thetas):
      if sj[0,1] != sj[1,0]: raise Exception("Invalid s_%d %s s12 != s21" % (idx, sj))
      p = sj[0,1] / math.sqrt(sj[0,0]*sj[1,1])
      if p <= -1 or p >= 1: raise Exception("Invalid s_%d %s p %.4f invalid" % (idx, sj, p))

#some sanity checks
checkThetas(thetas)

def f(x, theta): #(6.18)
   _u = theta[0]
   _s = theta[1] 
   if _u.shape != x.shape or x.shape != (2,1) or _s.shape != (2,2): raise Exception("invalid shape of X %s , u %s, s %s" % (x.shape, _u.shape, _s.shape))
   det = np.linalg.det(_s) 
   prod = np.matmul(np.transpose(x - _u), np.linalg.inv(_s))
   prod = np.matmul(prod, x - _u)
   return math.exp(-0.5*prod)/(2*math.pi*math.sqrt(det))

def getPji(taus, thetas, xList): #compute all pji
   if len(taus) != len(thetas): raise Exception("taus length must match with thetas")
   pjiList = []
   for _j in range(len(thetas)): pjiList.append([])
   for xi in xList: #(6.10)
      _l = []
      for j in range(len(taus)): _l.append(taus[j]*f(xi, thetas[j]))
      s = sum(_l)
      for j in range(len(taus)): pjiList[j].append(_l[j]/s)
   return pjiList
   
def tj(j, pjiList, numX): #(6.20)
   s = 0
   for i in range(numX): s += pjiList[j-1][i] 
   return s/numX

def uj(j, pjiList, xList): #(6.21)
   sn = 0
   sd = 0
   for i in range(len(xList)):
      xi = xList[i]
      sn += (pjiList[j-1][i] * xi)
      sd += pjiList[j-1][i]
   return sn/sd

def sj(j, uj, pjiList, xList): #(6.22)
   sn = 0
   sd = 0
   for i in range(len(xList)):
      xi = xList[i]
      sn += (pjiList[j-1][i] * np.matmul(xi - uj, np.transpose(xi - uj)))
      sd += pjiList[j-1][i]
   return sn/sd



def getParamStr(taus, thetas):
   numJ = len(taus)
   if numJ != len(thetas): raise Exception("taus length must match with thetas")
   ss = "t = ("
   for j in range(numJ): ss += ("%.4f, " % taus[j])
   ss = ss[:-2] + ")\n"
   for j in range(numJ): 
      ss += ("theta_%d :\nu_%d =\n%s\ns_%d=\n%s\n" % (j, j, thetas[j][0], j, thetas[j][1]))
   return ss


#main(): EM process
numJ = len(taus)
if numJ != len(thetas): raise Exception("taus length must match with thetas")

np.set_printoptions(precision=4)
print("initial guess:")
print(getParamStr(taus, thetas))

minIters = 100 #iterations to run
iters = 0
while True:
   if iters >= minIters: break 
   iters += 1

   #E step: compute all pji
   pjiList = getPji(taus, thetas, xData)

   #M step: re-estimate the parameters
   for j in range(numJ): taus[j] = tj(j, pjiList, len(xData))
   for j in range(numJ): thetas[j][0] = uj(j, pjiList, xData) #uj is index 0 
   for j in range(numJ): thetas[j][1] = sj(j, thetas[j][0], pjiList, xData) #sj is index 1

print("After %d iterations, EM converged to:" % iters) 
print(getParamStr(taus, thetas))

#This is for verify pji after 1st E-step in Table 6.7. Set minIters to 1 and check
#for i in range(len(xData)):
#   for j in range(numJ):
#      print("p_%d,%d = %.4f" % (j+1, i+1, pjiList[j][i]))


#assign data point the highest probability cluster
clusterIds = []
for xi in xData:
   probs = []
   for j in range(numJ): probs.append(f(xi, thetas[j]))
   clusterIds.append(probs.index(max(probs)))

#color constants
red = (1, 0, 0)
blue = (0, 0, 1)
green = (0, 1, 0)
black = (0, 0, 0)
colors = [red, green, blue]

#plot the center of the thetas using black color
c = []
xs = []
ys = []
for j in range(numJ):
   xs.append(thetas[j][0][0,0])
   ys.append(thetas[j][0][1,0])
   c.append(black)

#plot the data point with same color for the same clusters
for idx, xi in enumerate(xData):
   xs.append(xi[0,0])
   ys.append(xi[1,0])
   c.append(colors[clusterIds[idx]])

#plot the clustering solution
plt.scatter(xs, ys, c=c)
plt.show()


