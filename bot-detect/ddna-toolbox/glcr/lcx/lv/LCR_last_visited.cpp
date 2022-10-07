#include "LCR_last_visited.hpp"

#include "util/LV_list_lcr.hpp"

LCR_last_visited::LCR_last_visited(GSA *gsa, Result_saver* rs) : LCR(rs) {
	this->gsa = gsa;
}

LCR_last_visited::~LCR_last_visited()
{
}

void LCR_last_visited::get_lcr(int x_repeats) {
	LV_list_lcr wl = LV_list_lcr(gsa->num_words, x_repeats, rs);
	
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
}
