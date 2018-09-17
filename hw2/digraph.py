f = open('plaintext.txt', 'r')
s = f.read()
f.close()

CharSet = 'abcdefghijklmnopqrstuvwxyz'
N = len(CharSet)

#init digraph frequency table with 0
A = []
for i in range(N):
   A.append([])
   for j in range(N):
      A[i].append(0)

#add digraph frequency count
prev = None
for c in s:
   idx = CharSet.find(c) 
   if idx < 0: continue
   if prev == None:
      prev = idx
      continue
   A[prev][idx] += 1 
   prev = idx

#add 5 for each element
for i in range(N):
   for j in range(N):
      A[i][j] += 5

#normalize the table
for i in range(N):
   tsum = 0
   for j in range(N):
      tsum += A[i][j]
   for j in range(N):
      A[i][j] = float(A[i][j]) / tsum

#print the digraph frequency
pstr = '{\n'
for i in range(N):
   pstr += '{'
   for j in range(N):
      if j != N-1: pstr += ('%s, ' % A[i][j])
      else: pstr += ('%s' % A[i][j])
   pstr += '},\n'
pstr += '}\n'

print(pstr)



