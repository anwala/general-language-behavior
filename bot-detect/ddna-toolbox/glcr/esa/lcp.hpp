#ifndef LCP_HPP_
#define LCP_HPP_

#include "typedefs.h"

void calc_lcptab(int* suftab,int* inv_suftab,int* text,int* lcptab,int n);
void calc_lcptabs(int* suftab, int* inv_suftab, int* text, int* lcptabs, int n, int num_words, int* wordindex);

#endif /*LCP_HPP_*/
