import numpy as np
import math
import pca

#hardcoded training input vectors in section 4.6 (eq 4.7)
x1 = np.array([2,1,0,3,1,1])
x2 = np.array([2,3,1,2,3,0])
x3 = np.array([1,0,3,3,1,1])
x4 = np.array([2,3,1,0,3,2])

#hardcoded eigenvalues from the trained PCA in section 4.6 (eq 4.9)
e1 = 4.0833
e2 = 1.2364
e3 = 0.7428

#(a)
A, mu = pca.getAMu([x1,x2,x3,x4])
C = (1.0/4)*np.dot(A, np.transpose(A))
print("C = %s" % C)
print("total variance = %.4f" % np.sum(C.diagonal()))

#(b)
print("total variance in projection space = %.4f" % sum([e1,e2,e3]))

