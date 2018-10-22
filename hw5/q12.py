from sklearn.svm import LinearSVC

train_x = []
train_y = []
test_x = []
test_y = []

with open('malwareBenignScores.txt') as f:
   for line in f:
      tokens = line.strip().split()
      try:
         sampleId = int(tokens[0])
      except:
         continue #skip header lines

      s1 = float(tokens[1])
      s2 = float(tokens[2])
      s3 = float(tokens[3])
      s4 = float(tokens[4])
      s5 = float(tokens[5])
      s6 = float(tokens[6])
      if sampleId <= 20:
         train_x.append([s1,s2,s3])
         train_y.append(1) #1 means malware
         train_x.append([s4,s5,s6])
         train_y.append(0) #0 means benign
      else:
         test_x.append([s1,s2,s3])
         test_y.append(1) #1 means malware
         test_x.append([s4,s5,s6])
         test_y.append(0) #0 means benign

clf = LinearSVC(random_state=0, tol=1e-5)
clf.fit(train_x, train_y)
print(clf.coef_)
print(clf.score(test_x, test_y))

