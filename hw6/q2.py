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

def compute(w0,w1,w2,w3,w4,w5):
   x0 = 0
   x1 = 0
   print("input (%s, %s) , y = %s" % (x0, x1, y(w0,w1,w2,w3,w4,w5,x0,x1)))
   x0 = 0
   x1 = 0.5
   print("input (%s, %s) , y = %s" % (x0, x1, y(w0,w1,w2,w3,w4,w5,x0,x1)))
   x0 = 0
   x1 = 1
   print("input (%s, %s) , y = %s" % (x0, x1, y(w0,w1,w2,w3,w4,w5,x0,x1)))
   x0 = 0.5
   x1 = 0
   print("input (%s, %s) , y = %s" % (x0, x1, y(w0,w1,w2,w3,w4,w5,x0,x1)))
   x0 = 0.5
   x1 = 0.5
   print("input (%s, %s) , y = %s" % (x0, x1, y(w0,w1,w2,w3,w4,w5,x0,x1)))
   x0 = 0.5
   x1 = 1
   print("input (%s, %s) , y = %s" % (x0, x1, y(w0,w1,w2,w3,w4,w5,x0,x1)))
   x0 = 1
   x1 = 0
   print("input (%s, %s) , y = %s" % (x0, x1, y(w0,w1,w2,w3,w4,w5,x0,x1)))
   x0 = 1
   x1 = 0.5
   print("input (%s, %s) , y = %s" % (x0, x1, y(w0,w1,w2,w3,w4,w5,x0,x1)))
   x0 = 1
   x1 = 1
   print("input (%s, %s) , y = %s" % (x0, x1, y(w0,w1,w2,w3,w4,w5,x0,x1)))

weights = [-1, 1]
for w0 in weights:
   for w1 in weights:
      for w2 in weights:
         for w3 in weights:
            for w4 in weights:
               for w5 in weights:
                  if compare(w0,w1,w2,w3,w4,w5):
                     print("XOR: w0=%d,w1=%d,w2=%d,w3=%d,w4=%d,w5=%d" % (w0,w1,w2,w3,w4,w5))
                     compute(w0,w1,w2,w3,w4,w5)
