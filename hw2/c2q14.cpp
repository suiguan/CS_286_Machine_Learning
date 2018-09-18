#include <stdio.h>
#include <ctime>
#include <cstdlib>
#include <cmath>
#include <string>
#include <fstream>
#include "hmm.h"

static const std::string ObserSet = "abcdefghijklmnopqrstuvwxyz";

//predict the simple shift key assume 
//HHM is trained with: A is fixed digraph matrix, N = M = 26
static int predictMapping(HMM* hmm) {
   //this is the group truth key to be compared
   //e.g., gtKey[0] = 4, then 'a'(0) maps to 'e'(4)
   static const int gtKey[26] = {4, 9, 21, 6, 25, 23, 13, 8, 1, 7, 15, 22, 18, 3, 17, 16, 0, 20, 12, 5, 2, 11, 14, 24, 10, 19};

   int cor = 0;
   for (int i = 0; i < 26; i++) {
      float maxP = 0.0;
      int maxJ = -1;
      for (int j = 0; j < 26; j++) {
         if (*hmm->getB(j, i) >= maxP) {
            maxP = *hmm->getB(j, i);
            maxJ = j;
         }
      }
      if (gtKey[maxJ] == i) cor++;
   }
   printf("cor = %d\n", cor);
   return cor;
}

int main(int argc, const char** argv) {
   if (argc != 7) {
      printf("Usage: %s <txt> <N> <T> <minIters> <epsilon> <n>\n", argv[0]);
      return -1;
   }

   const int N = std::stoi(argv[2]);
   const int M = ObserSet.length();
   int T = std::stoi(argv[3]);
   const int minIters = std::stoi(argv[4]);
   const float epsilon = std::stof(argv[5]);
   const int numTrials = std::stoi(argv[6]);
   int* obsers = (int*)malloc(T*sizeof(int));
   if (!obsers) {
      printf("no memory\n");
      return -2;
   }

   //prepare observation sequence from txt file
   printf("using txt file %s\n", argv[1]);
   std::ifstream is(argv[1], std::ifstream::in);
   char c;
   int i = 0;
   while (is.get(c)) {
      int idx = ObserSet.find(c);
      if (idx == std::string::npos) continue;
      obsers[i] = idx;
      i++;
      if (i >= T) break;
   }
   is.close();
   if (i < T) {
      printf("file %s has %d less than %d chars\n", argv[2], i, T);
      T = i;
   }

   //start training
   int bestCor = 0;
   for (int num = 0; num < numTrials; num++) {
      HMM* hmm = new HMM(N, M, minIters, epsilon);
      if (!hmm) {
         printf("no memory\n");
         return -3;
      }

      printf("start training HMM for seq N = %d, M = %d, minIters = %d, eps = %.6f, T = %d\n", N, M, minIters, epsilon, T);
      hmm->fit(obsers, T);

      int cor = predictMapping(hmm);
      if (cor > bestCor) bestCor = cor;

      printf("%d out of %d. Cor = %d. Best so far = %d\n", num, numTrials, cor, bestCor);
      delete hmm;
   }
   printf("best cor %d out of %d trails\n", bestCor, numTrials);

   //clean up and exit
   free(obsers);
   return 0;
}



