#include "GLCR_last_visited_int.hpp"
#include "util/LV_list_glcr_int.hpp"
#include <iostream>
using namespace std;
GLCR_last_visited_int::GLCR_last_visited_int(GSA* gsa, Result_saver* rs) : GLCR(rs)
{
	this->gsa = gsa;
}

GLCR_last_visited_int::~GLCR_last_visited_int()
{
}

void GLCR_last_visited_int::get_glcr(int* D) {
	LV_list_glcr_int wl = LV_list_glcr_int(gsa->num_words, D, rs, gsa->get_max_lcp());
	bool clean = true;
	for (int i=0; i<gsa->len; i++) {
		int lcp = gsa->lcp[i];
		int text = gsa->text(i);
		
		wl.lcp_update(lcp, text, clean);
		
		if (D[text]==0) {
			rs->flush(lcp);
		}
		wl.list_update(i, text, lcp, gsa->lcps[i]);
		
		clean = D[text]>0;
	}
	wl.lcp_update(0,gsa->text(gsa->len-1), clean);
	rs->flush(0);

}

