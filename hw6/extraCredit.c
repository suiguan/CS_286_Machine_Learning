#include <stdio.h>
#include <stdlib.h>
#include "extraCredit.h"

int winner(int n, int k)
{
   //validate inputs
   if (n < 1 || k < 1) {
      printf("invalid input n %d < 1 or k %d < 1\n", n, k);
      return -1;
   }

   //check memory to build linked list
   LNode_t * head = malloc(n*sizeof(LNode_t));
   if (head == NULL) {
      printf("no memory\n");
      return -1;
   }

   //init the linked list
   for (int i = 0; i < n; i++) {
      (head+i)->val = (i+1); //position is numbered 1-based
      int next = i+1;
      if (next == n) next = 0; //loop around if this is last prisoner
      (head+i)->next = (head+next);
   }

   //start the game until only 1 remaining...
   int remain = n;
   LNode_t * cur = head;
   LNode_t * pre = head+(n-1);
   while (remain > 1) {
      //go to the k-th prisoner
      for (int j = 0; j < k; j++) {
         pre = cur;
         cur = cur->next;
      }

      //eliminate the k-th prisoner 
      pre->next = cur->next;
      cur = pre->next;
      remain--;
   }

   //done, cleanup and return
   int ret = cur->val;
   free(head);
   return ret;
}

int main() {
   int n = 6;
   int k = 2;
   int w = winner(n, k);
   printf("with n = %d, k = %d, winner will be at position %d\n", n, k, w);

   n = 6;
   k = 3;
   w = winner(n, k);
   printf("with n = %d, k = %d, winner will be at position %d\n", n, k, w);
}
