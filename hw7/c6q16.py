#chapter 6, Q16 - DBSCAN
import random
import math

#data points in dbscan.txt
Xs=[(1.0, 5.0), (1.25, 5.35), (1.25, 5.75), (1.5, 6.25), (1.75, 6.75), (2.0, 6.5), (3.0, 7.75), (3.5, 8.25), (3.75, 8.75), (3.95, 9.1), (4.0, 8.5), (2.5, 7.25), (2.25, 7.75), (2.0, 6.5), (2.75, 8.25), (4.5, 8.9), (9.0, 5.0), (8.75, 5.85), (9.0, 6.25), (8.0, 7.0), (8.5, 6.25), (8.5, 6.75), (8.25, 7.65), (7.0, 8.25), (6.0, 8.75), (5.5, 8.25), (5.25, 8.75), (4.9, 8.75), (5.0, 8.5), (7.5, 7.75), (7.75, 8.25), (6.75, 8.0), (6.25, 8.25), (4.5, 8.9), (5.0, 1.0), (1.25, 4.65), (1.25, 4.25), (1.5, 3.75), (1.75, 3.25), (2.0, 3.5), (3.0, 2.25), (3.5, 1.75), (3.75, 8.75), (3.95, 0.9), (4.0, 1.5), (2.5, 2.75), (2.25, 2.25), (2.0, 3.5), (2.75, 1.75), (4.5, 1.1), (5.0, 9.0), (8.75, 5.15), (8.0, 2.25), (8.25, 3.0), (8.5, 4.75), (8.5, 4.25), (8.25, 3.35), (7.0, 1.75), (8.0, 3.5), (6.0, 1.25), (5.5, 1.75), (5.25, 1.25), (4.9, 1.25), (5.0, 1.5), (7.5, 2.25), (7.75, 2.75), (6.75, 2.0), (6.25, 1.75), (4.5, 1.1), (3.0, 4.5), (7.0, 4.5), (5.0, 3.0), (4.0, 3.35), (6.0, 3.35), (4.25, 3.25), (5.75, 3.25), (3.5, 3.75), (6.5, 3.75), (3.25, 4.0), (6.75, 4.0), (3.75, 3.55), (6.25, 3.55), (4.75, 3.05), (5.25, 3.05), (4.5, 3.15), (5.5, 3.15), (4.0, 6.5), (4.0, 6.75), (4.0, 6.25), (3.75, 6.5), (4.25, 6.5), (4.25, 6.75), (3.75, 6.25), (6.0, 6.5), (6.0, 6.75), (6.0, 6.25), (5.75, 6.75), (5.75, 6.25), (6.25, 6.75), (6.25, 6.25), (9.5, 9.5), (2.5, 9.5), (1.0, 8.0)]


def distance(p1, p2):
   return math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))

def getNeighborIdxList(pidx, Xs, e):
   l = []
   for i in range(len(Xs)):
      if distance(Xs[pidx], Xs[i]) <= e: l.append(i)
   return l

def isPtIdxInClusters(pidx, clusters):
   for c in clusters:
      if pidx in c: return True
   return False

#the implementation uses the points index in the List as the unique identifier
def dbscan(Xs, e, m): #dbscan clustering algorithm
   nonVisitedIndex = []
   for i in range(len(Xs)): nonVisitedIndex.append(i) #all points not visited

   clusters = []
   while len(nonVisitedIndex) > 0: #until all points visited 
      idx = random.choice(nonVisitedIndex) #random select a non-visited pt
      nonVisitedIndex.remove(idx) #mark as visited

      ns = getNeighborIdxList(idx, Xs, e)
      if len(ns) < m: #this is not a core point
         continue

      #this is core points, launch a new clusters
      newC = [idx]
      clusters.append(newC)

      #for all core point's neighbors not already in a cluster
      #add to stack as this is the points also get assigned to the same cluster
      stack = []
      for _pidx in ns:
         if not isPtIdxInClusters(_pidx, clusters): stack.append(_pidx)

      while len(stack) > 0:
         pidx = stack.pop()
         newC.append(pidx) #all points in the stack will assign to the cluster
         if pidx in nonVisitedIndex: nonVisitedIndex.remove(pidx) #mark as visited

         _ns = getNeighborIdxList(pidx, Xs, e)
         if len(_ns) < m: continue #not a core point so its neighbors won't expand 

         #this is core point, expand with its neighbors 
         _ns.remove(pidx)
         for _pidx in _ns:
            #push all reachable points to stack
            #if they not already in cluster and the stack
            if not isPtIdxInClusters(_pidx, clusters) and not _pidx in stack:  
               stack.append(_pidx)

   #return
   return clusters

      


#main():

#choice of (e,m) in Q16
ems = [(0.6, 3), (0.75, 4), (1.0, 5), (2.0, 10)]

for e, m in ems:
   totalPts = 0
   clusters = dbscan(Xs, e, m)

   print("For e = %.1f, m = %d, # clusters = %d" % (e, m, len(clusters)))
   for i, c in enumerate(clusters):
      print("cluster %d (len=%d) = %s" % (i, len(c), c))
      totalPts += len(c)

   #pts not in any clusters are the noise
   noise = []
   for idx in range(len(Xs)):
      if not isPtIdxInClusters(idx, clusters): noise.append(idx)
         
   print("noise (len=%d) = %s" % (len(noise), noise))
   totalPts += len(noise)
   print("total # points = %d" % totalPts)
   print("\n")



