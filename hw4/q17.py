import numpy as np
import math

#u1, u2, u3 from (4.10)
u1 = np.array([0.1641, 0.6278, -0.2604, -0.5389, 0.4637, 0.0752])
u2 = np.array([0.2443, 0.1070, -0.8017, 0.4277, -0.1373, -0.2904])
u3 = np.array([-0.0710, 0.2934, 0.3952, 0.3439, 0.3644, -0.7083])

#eigenvalues from (4.9)
e1 = 4.0833
e2 = 1.2364
e3 = 0.7428

print("l1 = %s" % (math.sqrt(e1)*u1,))
print("l2 = %s" % (math.sqrt(e2)*u2,))
print("l3 = %s" % (math.sqrt(e3)*u3,))
