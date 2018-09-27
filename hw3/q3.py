seqs = [
   list("A-AB-BAFCD-B-AAEA0ACEDA-EQ---A-ABCDBALF4-BBASB---AAAAFB"),
   list("A-ABNBAFCD-B-AAEAABCEDA-EQ-CDABAB--BA-F4NBBM-BTYBAAAA--"),
   list("A-AB-BAFCDAB-A-EAA-CEDCDEQA--ABFBAN---F4-BBAFBTYBAAAA--"),
   list("2AAB-BAFCDAB-A-EAABCEDCDEQFCDABA-APAL-F4-BBA--SBAAAAA--"),
   list("CDAB-BAFCDB1-AAEAA-CEDA-EQ-CDABABABAL-F4LBBAFBSBAAAAA--"),
   list("CDABAAA----B-A-EA-ACEDCDEQ---A-ABCD-A-F4-BBASB---AAAAFB"),
   list("CDAB--A-CDAB-A-EAA-CEDA-EQ-CDABCDCDAA-F4MBB--ATYBAAAA--"),
   list("--AA-BA-CDB--AAEAA-CEDCDEQ-CDABPBA-AB-F4-BBAFBSBMAAAA--"),
   list("CDAB--RBAFABPAAEA-ACEDCDEQAABCDAFAL---F4NBBASB---AAAAMB"),
   list("A-ABAA-----B-AAEA-ACEDCDEQAABAFA------F4BNBASB---AAAAFB"),
]

def getObserTable(seqs):
   obserTable = {}
   for seq in seqs:
      for c in seq: 
         if c != "-": obserTable[c] = 0 
   return obserTable

numSeqs = len(seqs)
seqLen = len(seqs[0])
M = len(getObserTable(seqs))

def getColumns(col, seqs):
   return [c[col] for c in seqs]

def getEmissionProb(startCol, endCol, seqs):
   obsers = []
   for i in range(startCol, endCol): 
      for o in getColumns(i, seqs):
         if o != "-": obsers.append(o)
   t = getObserTable(seqs)
   for o in obsers: t[o] += 1
   for o in t: t[o] += 1 #add 1 rules to avoid zero-probability
   for o in t: t[o] = float(t[o]) / (len(obsers) + M)
   return t

print("numSeqs = %d, seqLen = %d, M = %d\n\n" % (numSeqs, seqLen, M))

def isColumnConservative(majority, col, seqs):
   numEle = 0
   for o in getColumns(col, seqs):
      if o != "-": numEle += 1
   return numEle >= majority

majority = int(numSeqs/2) + (numSeqs % 2)

match_state_idx = 0
insert_state_idx = 0

insert_state_start_col = None
insert_state_end_col = None

col = 0
while col < seqLen: 
   if isColumnConservative(majority, col, seqs): #this is match state
      print("Column %d is a MATCH state (M_%d) with emission prob:" % (col, match_state_idx))
      probTable = getEmissionProb(col, col+1, seqs)
      msg = ""
      for key in probTable: msg += "E(%s) = %.3f, " % (key, probTable[key])
      print(msg + "\n")
      match_state_idx += 1

   else: #this is insert state, if next also insert state, then merged into a single insert state
      if insert_state_start_col == None: insert_state_start_col = col
      if col >= seqLen - 1 or isColumnConservative(majority, col+1, seqs):
         #this is last column or next state is a match state, so this is end of insert state
         insert_state_end_col = col+1

      if insert_state_end_col != None:
         print("Column %d through %d is an INSERT state (I_%d) with emission prob:" % (insert_state_start_col, insert_state_end_col-1, insert_state_idx))
         probTable = getEmissionProb(insert_state_start_col, insert_state_end_col, seqs)
         msg = ""
         for key in probTable: msg += "E(%s) = %.3f, " % (key, probTable[key])
         print(msg + "\n")
         insert_state_idx += 1
         insert_state_start_col = None
         insert_state_end_col = None

   col += 1



