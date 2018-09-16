import random

T = 1000000
charSet = 'abcdefghijklmnopqrstuvwxyz'
f = open('brown.txt', 'r')
txt = f.read()
f.close()

lookup = {}
for c in charSet:
   idx = charSet.find(c)
   s = idx
   usedC = False
   while s == idx or usedC:
      s = int(random.random() * 26)
      usedC = False
      for k in lookup:
         if lookup[k] == charSet[s]: usedC = True
   lookup[c] = charSet[s]
print("encryption key = %s" % lookup)

plaintext = ''
encrypted = ''
for ch in txt:
   idx = charSet.find(ch.lower())
   if idx >= 0: 
      plaintext += charSet[idx]
      encrypted += lookup[charSet[idx]]
   if len(plaintext) >= T: break

with open('plaintext.txt', 'w') as f:
   f.write(plaintext)

with open('encrypted.txt', 'w') as f:
   f.write(encrypted)

with open('key.txt', 'w') as f:
   f.write("%s" % lookup)

