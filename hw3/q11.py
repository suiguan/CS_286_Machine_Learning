
#key-value pair values represents 
#the possible next state given currently at the 'key' state
state2 = {
   'begin' : ['I0', 'I1','I2', 'M1', 'M2'], 
   'I0' : ['I0', 'I1','I2', 'M1', 'M2'], 
   'M1' : ['I1','I2', 'M2'], 
   'I1' : ['I1','I2',  'M2'], 
   'M2' : ['I2'], 
   'I2' : ['I2'], 
}
state3 = {
   'begin' : ['I0', 'I1','I2', 'I3', 'M1', 'M2', 'M3'], 
   'I0' : ['I0', 'I1','I2', 'I3', 'M1', 'M2', 'M3'], 
   'M1' : ['I1','I2', 'I3', 'M2', 'M3'], 
   'I1' : ['I1','I2', 'I3', 'M2', 'M3'], 
   'M2' : ['I2', 'I3', 'M3'], 
   'I2' : ['I2', 'I3', 'M3'], 
   'M3' : ['I3'], 
   'I3' : ['I3'], 
}

def getPHMMAllStates(seq, startState, stateDict, prev, results):
   seq = seq[1:]
   for s in stateDict[startState]:
      p = prev + [s,]
      if len(seq) == 0: results.append(p) 
      else: getPHMMAllStates(seq, s, stateDict, p, results)


if __name__ == '__main__':
   stateDict = state2
   results = []
   seq = ('x0', 'x1', 'x2')
   getPHMMAllStates(seq, 'begin', stateDict, [], results) 

   N = 0
   for k in stateDict.keys(): 
      if k.startswith('M'): N += 1 
   print("For PHMM (N=%d), number of all states for seq len %d = %d" % (N, len(seq), len(results)))
   for r in results: print(r)
