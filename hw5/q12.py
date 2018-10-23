from sklearn.svm import LinearSVC

train_x = []
train_y = []
test_x = []
test_y = []

#set which feature to use: a list of [0,1,2] means use all features 
#a list of [0,2] means use only 1st and 3rd features
use_features = [2] 
features_names = ['HMM', 'SSD', 'OGS']

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
      malwareScores = [s1,s2,s3] #HMM, SSD, OGS scores for malware
      benignScores = [s4,s5,s6] #HMM, SSD, OGS scores for benign
      mf = [malwareScores[i] for i in use_features]
      bf = [benignScores[i] for i in use_features]
      if sampleId <= 20:
         train_x.append(mf)
         train_y.append(1) #1 means malware
         train_x.append(bf) #HMM, SSD, OGS scores for benign
         train_y.append(0) #0 means benign
      else:
         test_x.append(mf)
         test_y.append(1) #1 means malware
         test_x.append(bf)
         test_y.append(0) #0 means benign

clf = LinearSVC()
print("starting training the linear svm using the first 20 samples as training data")
clf.fit(train_x, train_y)
print("trained svm coefficient for %s: %s" % ([features_names[i] for i in use_features], clf.coef_,))
print("trained svm mean accuracy on test data (last 20 samples) = %s" % clf.score(test_x, test_y))

