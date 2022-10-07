#include "GSA.hpp"
#include "../esa/skew.hpp"
#include "../esa/lcp.hpp"
#include <stdio.h>
#include <iostream>
#include <cstring>
#include <fstream>

#include <stdlib.h>
using namespace std;

/**
 * GSA = Generalized Suffix Array
 */
GSA::GSA(int* text, int len, int alphabet_size, int* wordbegin, int num_words)
{
		this->len = len;
		this->wordbegin = new int[num_words+1];
		memcpy(this->wordbegin, wordbegin, (num_words+1)*sizeof(int));
		this->num_words = num_words;
		
		this->otext = new int[len];
		memcpy(this->otext, text, len*sizeof(int));
		
		sa = new int[len];
		inv_sa = new int[len];
		wordindex = new int[len+1];
		lcps = NULL;

		lcp = (int*)calloc(len+1, sizeof(int));
		fprintf(stderr, "compute suffix array ... ");
		//skew:
		suffixArray(text, sa, len, alphabet_size+num_words);

		fprintf(stderr, "ok\n");
		fprintf(stderr, "compute inverse suffix array ... ");
		inv_suffixArray(sa, len);
		fprintf(stderr, "ok\n");
		fprintf(stderr, "compute lcp-table ... ");
		calc_lcptab(sa, inv_sa, text, lcp, len);
		fprintf(stderr, "ok\n");
		fprintf(stderr, "initialize wordindex-table ... ");
		init_wordindex();
		fprintf(stderr, "ok\n");

}

GSA::~GSA()
{
	delete[] sa;
	delete[] inv_sa;
	free(lcp);
	delete[] wordindex;
	delete[] wordbegin;
	delete[] otext;
	if (lcps!=NULL) {
		delete[] lcps;
	}
}

void GSA::write(char *filename, char* buf) {
		ofstream fout;
		fout.open(filename, std::ofstream::out | std::ofstream::app);
		fout << "i,sa,inv_sa,lcp,wordindex,buf+sa\n";
		for(int i=0; i<len; i++) {
			fout << i << ',' << sa[i] << ',' << inv_sa[i] << "," << lcp[i] << ',' << wordindex[i]+1 << ',' << buf+sa[i] << '\n';
		}
		fout.close();
}

void GSA::write_tiny(char *filename, char* buf) {
		ofstream fout;
		fout.open(filename, std::ofstream::out | std::ofstream::app);
		fout << "wordindex\n";
		for(int i=0; i<len; i++) {
			fout << wordindex[i]+1 << '\n';
		}
		fout.close();
}

bool GSA::equals(GSA *gsa) {
	if (len != gsa->len) 
		return false;
	if (num_words != gsa->num_words) 
		return false;
	for (int i=0; i<num_words+1; i++)
		if (wordbegin[i] != gsa->wordbegin[i])
			return false;
	for (int i=0; i<len; i++)
		if (sa[i] != gsa->sa[i]) 
			return false;
	for (int i=0; i<len; i++)
		if (inv_sa[i] != gsa->inv_sa[i]) 
			return false;
	for (int i=0; i<len; i++)
		if (lcp[i] != gsa->lcp[i]) 
			return false;
	for (int i=0; i<len; i++)
		if (wordindex[i] != gsa->wordindex[i]) 
			return false;
	for (int i=0; i<len; i++)
		if (otext[i] != gsa->otext[i]) 
			return false;
	if (lcps!=NULL)
		for (int i=0; i<len; i++)
			if (lcps[i] != gsa->lcps[i]) 
				return false;
	return true;
}

int GSA::text(int i) {
	return wordindex[i];
}

void GSA::init_lcps() {
	lcps = new int[len];
	
	calc_lcptabs(sa, inv_sa, otext, lcps, len, num_words, wordindex);
}

void GSA::inv_suffixArray(int* sa, int len) {
		for(int i=0;i<len;++i) {
			inv_sa[sa[i]] = i;
		}
}
void GSA::init_wordindex() {
	int index = 0;
	int j=0;
	for (int i=0; i<num_words; i++) {
		int next_wordbegin = wordbegin[i+1];
		for(; j<next_wordbegin; j++) {
			wordindex[inv_sa[j]] = index;
		}
		index++;
	}
	wordindex[len]=0;
}

int GSA::get_max_lcp() {
	int max_lcp = 0;
	for (int i=0; i<len; i++) {
		if (lcp[i]>max_lcp) {
			max_lcp = lcp[i];
		}
	}
	return max_lcp;
}

void GSA::print(char* buf) {
	for(int i=0; i<len; i++) {
		printf("%4d & %4d & %4d & %4d & %4d &  %s \\\\\n", i, sa[i], inv_sa[i], lcp[i], wordindex[i]+1, buf+sa[i]);
	}
}
