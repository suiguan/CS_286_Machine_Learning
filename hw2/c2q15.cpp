#include <stdio.h>
#include <ctime>
#include <cstdlib>
#include <cmath>
#include <string>
#include <fstream>
#include "hmm.h"

static int Z408[408] = {
     1, 2, 3, 4, 5, 4, 6, 7, 2, 8, 9,10,11,12,13,11, 7,
    14,15,16,17,18,19,20,21, 1,22, 3,23,24,25,26,19,17,
    27,28,19,29, 6,30, 8,31,26,32,33,34,35,19,36,37,38,
    39,40, 4, 1, 2, 7, 3, 9,10,41, 6, 2,42,10,43,26,44,
     8,29,45,27, 5,28,46,47,48,12,20,22,15,14,17,31,19,
    23,16,26,18,36, 1,24,30,38,21,26,13,49,37,50,39,40,
    10,34,33,30,19,44,43, 9, 1,26,18, 7,32,21,39, 2, 7,
    45,46, 4, 3, 2, 7,23,13,26,44,22,27, 6,29,10,10, 8,
    51, 5,24,26,12,30,38,14,26,25,49,37,45,27,47, 1,52,
     7, 3,36,10,16,28,11,21,48,34,40,17,44, 6,22, 8,20,
     5,51,12, 9,15,14,30,37,16,33,45,38,43,29,10,21,22,
    30, 1,36,10,53,32,19,47,48,46,17, 4,23,13,28,35,41,
     3,37,27,49,10, 6,33, 2,45,38,34,15,44,24,22,11,18,
    47,30,25,28, 8,37, 1,49,45,27,43,34,41,38, 5,40, 3,
    50, 6,12, 8,41, 1,52, 7,15,14,48,16,15,32,33, 9, 3,
    29,11,39,47,43,42, 6,17,21,31,36,50,18, 2, 2,25,27,
    34, 8,38,39,51,44, 4, 1, 2, 2, 5,42,41, 3,52, 7,15,
    12,17,13,26,14,26,53,20,52,49,51,16,23, 1,41, 1, 7,
     2, 9,32,37,10, 6,51,16,53,46,19,26,53,29,39,26,14,
    15, 5,17,18,19,24,44,53,32,19,41, 1, 2,52,45,33,53,
    22,25,20, 7,13, 1,50,13,41,36,46,48,31,45,25,11,26,
    53,17,46,52,52,21,17,37, 3, 9,10,13,35,20, 2,18,51,
     5,23,28,32,33,26,53,49,28,30,16,47, 7, 3,35,14,21,
    15,44,13,47, 1,14,30,21,26,44,22,27,38,11,19,30, 8
};
int Z408P[408] =
{
     8,11, 8,10, 4,10, 8,11,11, 8,13, 6,15, 4,14,15,11,
     4, 1, 4, 2, 0,20,18, 4, 8,19, 8,18,18,14,12,20, 2,
     7, 5,20,13, 8,19, 8,18,12,14,17, 4, 5,20,13,19, 7,
     0,13,10, 8,11,11, 8,13, 6,22, 8,11, 3, 6, 0,12, 4,
     8,13,19, 7, 4, 5,14,17,17, 4,18,19, 1, 4, 2, 0,20,
    18, 4,12, 0,13, 8,18,19, 7, 4,12,14,18,19, 3, 0,13,
     6, 4,17,14,20, 4, 0,13, 0,12, 0,11,14, 5, 0,11,11,
    19,14,10, 8,11,11,18,14,12, 4,19, 7, 8,13, 6, 6, 8,
    21, 4,18,12, 4,19, 7, 4,12,14,18,19,19, 7,17, 8,11,
    11, 8,13, 6, 4,23,15, 4,17, 4,13, 2, 4, 8,19, 8,18,
     4,21, 4,13, 1, 4,19,19, 4,17,19, 7, 0,13, 6, 4,19,
    19, 8,13, 6,24,14,20,17,17,14, 2,10,18,14, 5, 5,22,
     8,19, 7, 0, 6, 8,17,11,19, 7, 4, 1, 4,18,19,15, 0,
    17,19,14, 5, 8,19, 8,18,19, 7, 0, 4,22, 7, 4,13, 8,
     3, 8, 4, 8,22, 8,11,11, 1, 4,17, 4, 1,14,17,13, 8,
    13,15, 0,17, 0, 3, 8, 2, 4, 0,13, 3, 0,11,11,19, 7,
     4, 8, 7, 0,21, 4,10, 8,11,11, 4, 3,22, 8,11,11, 1,
     4, 2,14,12, 4,12,24,18,11, 0,21, 4,18, 8,22, 8,11,
    11,13,14,19, 6, 8,21, 4,24,14,20,12,24,13, 0,12, 4,
     1, 4, 2, 0,20,18, 4,24,14,20,22, 8,11,11,19,17,24,
    19,14,18,11,14, 8, 3,14,22,13,14,17, 0,19,14,15,12,
    24, 2,14,11,11, 4, 2,19, 8,14, 6,14, 5,18,11, 0,21,
     4,18, 5,14,17,12,24, 0, 5,19, 4,17,11, 8, 5, 4, 4,
     1, 4,14,17, 8, 4,19, 4,12, 4,19, 7, 7,15, 8,19, 8,
};

static int getZ408CipherRange(int& start, int&end)
{
   start = -1;  
   end = -1;
   for (int i = 0; i < 408; i++) {
      if (start == -1) start = Z408[i];
      if (end == -1) end = Z408[i];
      if (Z408[i] > end) end = Z408[i];
      if (Z408[i] < start) start = Z408[i];
   }
};

//predict the z408 cipher text 
static int predictMapping(HMM* hmm) {
   int minC, maxC;
   getZ408CipherRange(minC, maxC);
   int cor = 0;
   for (int i = 0; i < 408; i++) {
      int cipherChar = Z408[i] - minC; //zero based cipher text
      //find the max prob as the decipher char
      float maxP = 0.0;
      int maxJ = -1;
      for (int j = 0; j < 26; j++) {
         if (*hmm->getB(j, cipherChar) >= maxP) {
            maxP = *hmm->getB(j, cipherChar);
            maxJ = j;
         }
      }
      if (Z408P[i] == maxJ) cor++; //if correctly decrypted
   }
   printf("cor = %d\n", cor);
   return cor;
}

int main(int argc, const char** argv) {
   if (argc != 5) {
      printf("Usage: %s <N> <minIters> <epsilon> <n>\n", argv[0]);
      return -1;
   }
   int start, end;
   getZ408CipherRange(start, end);
   printf("cipher text starts at %d to %d\n", start, end);

   const int N = std::stoi(argv[1]);
   const int M = end - start + 1;
   const int T = 408;
   const int minIters = std::stoi(argv[2]);
   const float epsilon = std::stof(argv[3]);
   const int numTrials = std::stoi(argv[4]);

   //covert observation to zero based
   int obser[T];
   for (int i = 0; i < T; i++) {
      obser[i] = Z408[i] - start; 
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
      hmm->fit(obser, T);

      int cor = predictMapping(hmm);
      if (cor > bestCor) bestCor = cor;

      printf("%d out of %d. Cor = %d. Best so far = %d\n", num, numTrials, cor, bestCor);
      delete hmm;
   }
   printf("best cor %d out of %d trails\n", bestCor, numTrials);

   //clean up and exit
   return 0;
}



