T = 50000
charSet = 'abcdefghijklmnopqrstuvwxyz'
f = open('brown.txt', 'r')
txt = f.read()
f.close()

shifted_length = 12 #this is the encryption key

plaintext = ''
encrypted = ''
for ch in txt:
   idx = charSet.find(ch.lower())
   if idx >= 0: 
      plaintext += charSet[idx]
      encrypted += charSet[(idx + shifted_length ) % len(charSet)]
   if len(plaintext) >= T: break

with open('plaintext.txt', 'w') as f:
   f.write(plaintext)

with open('encrypted.txt', 'w') as f:
   f.write(encrypted)


