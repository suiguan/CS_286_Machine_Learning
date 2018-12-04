#chapter 7 Q1

import numpy as np
import matplotlib.pyplot as plt
import math

red = (1, 0, 0)
blue = (0, 0, 1)
green = (0, 1, 0)

#data points and colors from Ch-7 Q1
points = [(0.5, 3.00), (1.0, 4.25), (1.5, 2.00), (2.0, 2.75), (2.5, 1.65),
         (3.0, 2.70), (3.5, 1.00), (4.0, 2.50), (4.5, 2.10), (5.0, 2.75),
         (0.5, 1.75), (1.5, 1.50), (2.5, 4.00), (2.5, 2.10), (3.0, 1.50),
         (3.5, 1.85), (4.0, 3.50), (5.0, 1.45),]

colors = [red, red, red, red, red, red, red, red, red, red, 
         blue, blue, blue, blue, blue, blue, blue, blue,]

#plot each points with their colors
xs = np.array([p[0] for p in points])
ys = np.array([p[1] for p in points])
plt.figure(0)
plt.scatter(xs, ys, c=colors)


def distance(p1, p2):
   return math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))

def kNearestNeighbors(p0, points, k):
   nearest = []
   for _k in range(k): nearest.append(None)

   for pidx, p in enumerate(points):
      d = distance(p0, p)
      for i in range(k):
         n = nearest[i]
         if n == None: 
            nearest[i] = (pidx, d) 
            break
         else:
            _, _d = n
            if d < _d: 
               nearest[i] = (pidx, d)
               d = _d #changes the distance to the one that has pop out from the list
                      #if there this one is part of the nearest, it will replace with later entries 
   
   idx = None
   for i, n in enumerate(nearest): 
      if n == None: 
         idx = i 
         break

   if idx != None: nearest = nearest[:idx]
   
   #create counter to find the majority
   counter = {}
   for idx, _ in nearest:
      c = colors[idx]
      if not c in counter: counter[c] = 0
      counter[c] += 1

   maxCount = None
   majorityC = None
   for c in counter.keys():
      if maxCount == None: 
         maxCount = counter[c] 
         majorityC = c
      elif counter[c] > maxCount: 
         maxCount = counter[c]
         majorityC = c
   if maxCount == None or maxCount < k/2: print("maxCount %s error. k = %d" % (maxCount, k))
   return majorityC

n = 100
x0 = np.linspace(0, 6, n)
x1 = np.linspace(0, 6, n)
c = np.zeros((n*n, 3))
x0p = np.zeros((n*n,))
x1p = np.zeros((n*n,))
for i in range(n):
   for j in range(n):
      c[i*n+j] = kNearestNeighbors((x0[i], x1[j]), points, 3)
      x0p[i*n+j] = x0[i]
      x1p[i*n+j] = x1[j] 

plt.figure(1)
plt.scatter(x0p, x1p, c=c)

#display graphs
plt.show()
