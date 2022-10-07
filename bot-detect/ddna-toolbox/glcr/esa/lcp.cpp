#include <algorithm>
#include "lcp.hpp"

using namespace std;

/**
 * calculate lcp table for suffix array
 */
void calc_lcptab(int* suftab, int* inv_suftab, int* text, int* lcptab, int n) {
	lcptab[0]=0;
	int i,j,k,l=0;
	
	for (i=0; i<n; i++) {
		if( (j = inv_suftab[i]) ) {
			k = suftab[j-1];
			while(text[k+l]==text[i+l]) {
				++l;
			}
			lcptab[j]=l;
			l=max(l-1,0);
		}
	}
}

/**
 * calculate lcp tabs for each text using the generalized suffix array
 */
void calc_lcptabs(int* suftab, int* inv_suftab, int* text, int* lcptabs, int n, int num_words, int* wordindex) {
	int* last_occ = new int[n];
	int* last_wordocc = new int[num_words];
	int* l = new int[num_words];
	for (int i=0; i<num_words; i++) {
		last_wordocc[i] = 0;
		l[i] = 0;
	}
	
	for (int i=0; i<n; i++) {
		int t = wordindex[i];
		last_occ[i] = last_wordocc[t];
		last_wordocc[t] = i;
	}
	
	int i,j,k;
	lcptabs[0] = 0;
	for (i=0; i<n; i++) {
		if( (j = inv_suftab[i]) ) {
			int t = wordindex[j];
			k = suftab[last_occ[j]];
			while(text[k+l[t]]==text[i+l[t]]) {
				l[t]++;
			}
			lcptabs[j] = l[t];
			l[t] = max(l[t]-1,0);
		}
	}
	delete[] last_occ;
	delete[] last_wordocc;
	delete[] l;
}
