#include "LCS_last_visited.hpp"

#include "util/LV_list_lcs.hpp"
//#include <iostream>
//using namespace std;
LCS_last_visited::LCS_last_visited(GSA *gsa, Result_saver* rs) : LCS(rs) {
	this->gsa = gsa;
}

LCS_last_visited::~LCS_last_visited()
{
}

void LCS_last_visited::get_lcs() {
	LV_list_lcs wl = LV_list_lcs(gsa->num_words, rs);
	for (int i=0; i<gsa->len; i++) {
		int lcp = gsa->lcp[i];
		int text = gsa->text(i);
		int front_lcp = wl.get_front_lcp();
		if (lcp <= front_lcp) {
			wl.lcp_update(lcp, i);
		}
		wl.list_update(text, lcp, i);
	}
	wl.lcp_update(0, gsa->len);
	//	cerr << wl.count<< endl;
}
