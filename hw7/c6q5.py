#chapter 6, Q5.

import random
import math
import numpy as np
import matplotlib.pyplot as plt

numK = 3 #choice of K, can only be 2 or 3

#hardcoded old faithful data with (duration, wait) in Table 6.6
data =\
   [
   (3.6, 79), (1.8, 54), (2.283, 62), (3.333, 74), (2.883, 55),
   (4.533, 85), (1.95, 51), (1.833, 54), (4.7, 88), (3.6, 85),
   (1.6, 52), (4.35, 85), (3.917, 84), (4.2, 78), (1.75, 62),
   (1.8, 51), (4.7, 83), (2.167, 52), (4.8, 84), (1.75, 47),
   ]  

#initial random centroids
minDuration = min([d[0] for d in data])
maxDuration = max([d[0] for d in data])
minWait = min([d[1] for d in data])
maxWait = max([d[1] for d in data])

if numK == 2:
   centroids =\
   [
   (random.uniform(minDuration, maxDuration), random.uniform(minWait, maxWait)),
   (random.uniform(minDuration, maxDuration), random.uniform(minWait, maxWait)),
   ]
elif numK == 3:
   centroids =\
   [
   (random.uniform(minDuration, maxDuration), random.uniform(minWait, maxWait)),
   (random.uniform(minDuration, maxDuration), random.uniform(minWait, maxWait)),
   (random.uniform(minDuration, maxDuration), random.uniform(minWait, maxWait)),
   ]
else:
   raise Exception("Unsupported K %d" % numK)

def distance(x1, x2):
   return math.sqrt(math.pow((x1[0] - x2[0]), 2) + math.pow((x1[1] - x2[1]), 2))

def getCentroidIdx(centroids, d):
   l = [distance(d, c) for c in centroids]
   return l.index(min(l))

def distortion(centroids, cIdxList, data):
   ret = 0
   for j in range(len(data)):
      d = data[j]
      c = centroids[cIdxList[j]]
      ret += distance(d, c)
   return ret

def centerOfMass(data):
   n = len(data)
   return sum([d[0] for d in data])/n , sum([d[1] for d in data])/n
      
   
def KMeans(centroids, data, thr):
   K = len(centroids)
   cIdxList = []
   for d in data: cIdxList.append(getCentroidIdx(centroids, d))

   prevDistort = None
   curDistort = None 
   while prevDistort == None or curDistort == None or curDistort - prevDistort > thr: 
      prevDistort = curDistort
      
      #re-calcuate the centroids using center of mass
      for j in range(K):
         cluster = []
         for didx in range(len(data)):
            if cIdxList[didx] == j: cluster.append(data[didx]) 
         if len(cluster) != 0: centroids[j] = centerOfMass(cluster)

      #compute the new distortion
      curDistort = distortion(centroids, cIdxList, data) 

   return cIdxList


dataCentroidsIdx = KMeans(centroids, data, 0.1) 

#visualize the clusters
red = (1, 0, 0)
blue = (0, 0, 1)
green = (0, 1, 0)
colors = [red, green, blue]
c = []
for cIdx in dataCentroidsIdx: c.append(colors[cIdx])
plt.scatter([d[0] for d in data], [d[1] for d in data], c=c)
plt.show()
