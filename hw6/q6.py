import math
def forward(ws, x0, x1, z):
   v0 = ws[0];
   v1 = ws[1];
   v2 = ws[2];
   v3 = ws[3];
   v4 = ws[4];
   v5 = ws[5];
   v6 = x0*v0 + x1*v2
   v7 = x0*v1 + x1*v3
   v8 = 1 + math.exp(-v6)
   v9 = 1 + math.exp(-v7)
   v10 = v4/v8
   v11 = v5/v9
   v12 = (v10 + v11 - z)**2 / 2
   return (v6, v7, v8, v9, v10, v11, v12)

def backward(ws, x0, x1, z, v6, v7, v8, v9, v10, v11, v12):
   dz = 1
   dv11 = v10 + v11 - z
   dv10 = v10 + v11 - z
   dv9 = -ws[5] * dv11 / (v9 **2)
   dv8 = -ws[4] * dv10 / (v8 **2)
   dv7 = -math.exp(-v7)*dv9
   dv6 = -math.exp(-v6)*dv8
   dv5 = dv11 / v9
   dv4 = dv10 / v8
   dv3 = x1*dv7
   dv2 = x1*dv6
   dv1 = x0*dv7
   dv0 = x0*dv6
   return (dv0, dv1, dv2, dv3, dv4, dv5)

def sgd(alpha, ws, x0, x1, z):
   v6, v7, v8, v9, v10, v11, v12 = forward(ws, x0, x1, z)
   dv0, dv1, dv2, dv3, dv4, dv5 = backward(ws, x0, x1, z, v6, v7, v8, v9, v10, v11, v12)

   #update weights
   ws[0] -= (alpha*dv0)
   ws[1] -= (alpha*dv1)
   ws[2] -= (alpha*dv2)
   ws[3] -= (alpha*dv3)
   ws[4] -= (alpha*dv4)
   ws[5] -= (alpha*dv5)
    

#data format: X0, X1, Z1
train = [
   (0.6, 0.4, 1), 
   (0.1, 0.2, 0), 
   (0.8, 0.6, 0), 
   (0.3, 0.7, 1), 
   (0.7, 0.3, 1), 
   (0.7, 0.7, 0), 
   (0.2, 0.9, 1), 
]

test = [
   (0.55, 0.11, 1),
   (0.32, 0.21, 0),
   (0.24, 0.64, 1),
   (0.86, 0.68, 0),
   (0.53, 0.79, 0),
   (0.46, 0.54, 1),
   (0.16, 0.51, 1),
   (0.52, 0.94, 0),
   (0.46, 0.87, 1),
   (0.96, 0.63, 0),
]

ws = [1,2,-1,1,-2,1] #initial weights (w0,w1,w2,w3,w4,w5)


if __name__ == '__main__':
   alpha = 0.1
   epochs = 10000

   #train MLP
   print("starting training MLP using SGD with alpha %s, %d epochs" % (alpha, epochs))
   print("Initial weights (w0,w1,w2,w3,w4,w5) = ")
   print(ws)
   for ep in range(epochs):
      for x0, x1, z in train: 
         sgd(alpha, ws, x0, x1, z)
   print("Finished training. Final weights (w0,w1,w2,w3,w4,w5) = ")
   print(ws)

   #calculate accuracy on train data
   print("computed MLP results for each training sample:")
   correct = 0
   for x0, x1, z in train: 
      _, _, _, _, v10, v11, _ = forward(ws, x0, x1, z)
      pred = v10 + v11
      print("train sample (x0, x1) = (%s, %s), MLP output %s, expected %d" % (x0, x1, pred, z))
      if int(pred + 0.5) == z: correct += 1
   print("train accuracy: %d/%d = %.3f%%" % (correct, len(train), correct*100/len(train)))

   #calculate accuracy on test data
   correct = 0
   for x0, x1, z in test: 
      _, _, _, _, v10, v11, _ = forward(ws, x0, x1, z)
      if int(v10 + v11 + 0.5) == z: correct += 1
   print("test accuracy: %d/%d = %.3f%%" % (correct, len(test), correct*100/len(test)))
