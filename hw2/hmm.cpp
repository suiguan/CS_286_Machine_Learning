#include <stdio.h>
#include <ctime>
#include <cstdlib>
#include <cmath>
#include <string>
#include "hmm.h"

#define MAX_INT 9223372036854775807

HMM::HMM(int N, int M, int minIters, float epsilon)
{
   mN = N;
   mM = M;
   mMinIters = minIters;
   mEps = epsilon;
   mOldLogProb = -MAX_INT;

   mA = NULL;
   mB = NULL;
   mPI = NULL;

   mC = NULL;
   mAlpha = NULL;
   mBeta = NULL;
   mGamma = NULL;
   mDiGamma = NULL;
}
HMM::~HMM()
{
   freeTables();
}

void HMM::freeTables()
{
   if (mA) {
      free(mA);
      mA = NULL;
   }
   if (mB) {
      free(mB);
      mB = NULL;
   }
   if (mPI) {
      free(mPI);
      mPI = NULL;
   }
   if (mC) {
      free(mC);
      mC = NULL;
   }
   if (mAlpha) {
      free(mAlpha);
      mAlpha = NULL;
   }
   if (mBeta) {
      free(mBeta);
      mBeta = NULL;
   }
   if (mGamma) {
      free(mGamma);
      mGamma = NULL;
   }
   if (mDiGamma) {
      free(mDiGamma);
      mDiGamma = NULL;
   }
}

void HMM::printModel()
{
   printf("A = \n");
   for (int i = 0; i < mN; i++) {
      std::string msg = std::to_string(i) + ": ";
      for (int j = 0; j < mN; j++) {
         msg += std::to_string(*getA(i, j)) + " ";
      }
      printf("%s\n", msg.c_str());
   }
   printf("B = \n");
   for (int i = 0; i < mN; i++) {
      std::string msg = std::to_string(i) + ": ";
      for (int j = 0; j < mM; j++) {
         msg += std::to_string(*getB(i, j)) + " ";
      }
      printf("%s\n", msg.c_str());
   }
   printf("PI = \n");
   std::string msg = "";
   for (int i = 0; i < mN; i++) {
      msg += std::to_string(*getPI(i)) + " ";
   }
   printf("%s\n", msg.c_str());
}

void HMM::fit(int* obserArr, int T)
{
   int iters = 0;
   float logProb = -MAX_INT;
   float diff = MAX_INT;
   setupTable(T);
   randomInit();
   printModel();
   while (iters < mMinIters || diff > mEps) {
      logProb = getScore(obserArr, T);
      backwardPass(obserArr, T);
      calcGammaDigamma(obserArr, T);
      reEstimateModel(obserArr, T);

      diff = std::abs(logProb - mOldLogProb); 
      mOldLogProb = logProb;

      if (iters % 100 == 0) {
         printf("score = %.3f\n", logProb);
         printModel();
      }

      iters += 1;
   }
}

float HMM::getScore(int* obserArr, int T)
{
   forwardPass(obserArr, T);
   float logProb = 0;
   for (int t = 0; t < T; t++) logProb += std::log(*(getC(t))); 
   return -logProb;
}

void HMM::setupTable(int T)
{
   freeTables();

   mA = (float*)malloc(mN*mN*sizeof(float));
   if (!mA) {
      printf("No memory!\n");
      exit(-1);
   }
   mB = (float*)malloc(mN*mM*sizeof(float));
   if (!mB) {
      printf("No memory!\n");
      exit(-1);
   }
   mPI = (float*)malloc(mN*sizeof(float));
   if (!mPI) {
      printf("No memory!\n");
      exit(-1);
   }

   mC = (float*)malloc(T*sizeof(float));
   if (!mC) {
      printf("No memory!\n");
      exit(-1);
   }
   mAlpha = (float*)malloc(T*mN*sizeof(float));
   if (!mAlpha) {
      printf("No memory!\n");
      exit(-1);
   }
   mBeta = (float*)malloc(T*mN*sizeof(float));
   if (!mBeta) {
      printf("No memory!\n");
      exit(-1);
   }
   mGamma = (float*)malloc(T*mN*sizeof(float));
   if (!mGamma) {
      printf("No memory!\n");
      exit(-1);
   }
   mDiGamma = (float*)malloc(T*mN*mN*sizeof(float));
   if (!mDiGamma) {
      printf("No memory!\n");
      exit(-1);
   }
}
float HMM::getRandVal(int k)
{
   float r = float(rand())/RAND_MAX;
   float v = 1.0/k; 
   float delta = 0.1 * v;
   return v + -delta + (r * 2 * delta);
} 

void HMM::normalizeArr(float* arr, int T)
{
   float sum = 0;
   for (int idx = 0; idx < T; idx++) sum += arr[idx];
   if (sum == 0) {
      printf("error! can't normalize all 0\n");
      exit(-1);
   }
   for (int idx = 0; idx < T; idx++) arr[idx] /= sum;
}
void HMM::randomInit()
{
   srand(time(NULL));
   for (int idx = 0; idx < mN; idx++) {
      for (int jdx = 0; jdx < mN; jdx++) {
         *getA(idx, jdx) = getRandVal(mN);
      }
      normalizeArr(mA+(idx*mN), mN);
   }
   for (int idx = 0; idx < mN; idx++) {
      for (int jdx = 0; jdx < mM; jdx++) {
         *getB(idx, jdx) = getRandVal(mM);
      }
      normalizeArr(mB+(idx*mM), mM);
   }
   for (int idx = 0; idx < mN; idx++) {
      *getPI(idx) = getRandVal(mN);
   }
   normalizeArr(mPI, mN);
} 

void HMM::forwardPass(int* obserArr, int T)
{
   //compute a0[i]
   *getC(0) = 0;
   for (int idx = 0; idx < mN; idx++) {
      float _a = (*getPI(idx)) * (*getB(idx, obserArr[0])); 
      *getAlpha(0, idx) = _a;
      *getC(0) = (*getC(0)) + _a;
   }

   //scale the a0(i)
   *getC(0) = 1.0 / (*getC(0));
   for (int idx = 0; idx < mN; idx++) {
      *getAlpha(0, idx) = (*getAlpha(0, idx)) * (*getC(0));
   }

   //compute at(i)
   for (int t = 1; t < T; t++) {
      *getC(t) = 0;
      for (int idx = 0; idx < mN; idx++) {
         *getAlpha(t, idx) = 0;
         for (int jdx = 0; jdx < mN; jdx++) {
            *getAlpha(t, idx) = (*getAlpha(t, idx)) +  ((*getAlpha(t-1, jdx)) * (*getA(jdx, idx)));
         }
         *getAlpha(t, idx) = (*getAlpha(t, idx)) * (*getB(idx, obserArr[t]));
         *getC(t) = (*getC(t)) + (*getAlpha(t, idx));
      }

      //scale at(i)
      *getC(t) = 1.0 / (*getC(t));
      for (int idx = 0; idx < mN; idx++) {
         *getAlpha(t, idx) = (*getAlpha(t, idx)) * (*getC(t));
      }
   }
}

void HMM::backwardPass(int* obserArr, int T)
{
   //let beta_t-1(i) = 1 scaled by cT-1
   for (int idx = 0; idx < mN; idx++) {
      *getBeta(T-1, idx) = *getC(T-1);
   }

   //beta-pass
   for (int t = T-2; t > 0; t--) {
      for (int idx = 0; idx < mN; idx++) {
         *getBeta(t, idx) = 0;
         for (int jdx = 0; jdx <mN; jdx++) {
            *getBeta(t, idx) += (*getA(idx, jdx) * (*getB(jdx, obserArr[t+1])) * (*getBeta(t+1, jdx)));
         }

         //scale beta_ti with same scale factor as a_ti
         *getBeta(t, idx) = (*getBeta(t, idx)) * (*getC(t));
      }
   }
}

void HMM::calcGammaDigamma(int* obserArr, int T)
{
   for (int t = 0; t < T-1; t++) {
      for (int idx = 0; idx < mN; idx++) {
         *getGamma(t, idx) = 0;
         for (int jdx = 0; jdx < mN; jdx++) {
            //No need to normalize since using scaled alpha and beta 
            *getDiGamma(t, idx, jdx) = (*getAlpha(t, idx)) * (*getA(idx, jdx)) * (*getB(jdx, obserArr[t+1])) * (*getBeta(t+1, jdx));
            *getGamma(t, idx) = (*getGamma(t, idx)) + (*getDiGamma(t, idx, jdx));
         }
      }
   }

   //special case for gamma_t-1(i)
   //No need to normalize since using scaled alpha and beta 
   for (int idx = 0; idx < mN; idx++) *getGamma(T-1, idx) = *getAlpha(T-1, idx);
  
}

void HMM::reEstimateModel(int* obserArr, int T)
{
   //re-estimate PI
   for (int idx = 0; idx < mN; idx++) *getPI(idx) = *getGamma(0, idx);

   //re-estimate A
   for (int idx = 0; idx < mN; idx++) {
      for (int jdx = 0; jdx < mN; jdx++) {
         float numer = 0;
         float denom = 0;
         for (int t = 0; t < T-1; t++) {
            numer += *getDiGamma(t, idx, jdx);
            denom += *getGamma(t, idx);
         }
         if (numer == 0) *getA(idx, jdx) = 0;
         else *getA(idx, jdx) = numer / denom;
      }
   }

   //re-estimate B
   for (int idx = 0; idx < mN; idx++) {
      for (int jdx = 0; jdx < mN; jdx++) {
         float numer = 0;
         float denom = 0;
         for (int t = 0; t < T; t++) {
            if (obserArr[t] == jdx) numer += *getGamma(t, idx);
            denom += *getGamma(t, idx);
         }
         if (numer == 0) *getB(idx, jdx) = 0;
         else *getB(idx, jdx) = numer / denom;
      }
   }
}


float* HMM::getA(int i, int j)
{
   return mA + (i*mN) + j;
}
float* HMM::getB(int i, int j)
{
   return mB + (i*mM) + j;
}
float* HMM::getPI(int i)
{
   return mPI + i; 
}

float* HMM::getC(int t)
{
   return mC + t; 
}
float* HMM::getAlpha(int t, int i)
{
   return mAlpha + (t*mN) + i; 
}
float* HMM::getBeta(int t, int i)
{
   return mAlpha + (t*mN) + i;
}
float* HMM::getGamma(int t, int i)
{
   return mGamma + (t*mN) + i;
}
float* HMM::getDiGamma(int t, int i, int j)
{
   return mDiGamma + (t*mN*mN) + (i*mN) + j;
}

int main() {
   int N = 2;
   int M = 2;
   int T = 10;
   int minIters = 1000;
   int epsilon = 0.00001;

   HMM* hmm = new HMM(N, M, minIters, epsilon);
   int obsers[T] = {0, 1, 1, 1, 1, 1, 1, 1, 1, 1};
   hmm->fit(obsers, T);
   return 0;
}



