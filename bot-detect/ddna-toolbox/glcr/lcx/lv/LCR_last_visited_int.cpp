#include "LCR_last_visited_int.hpp"

#include "util/LV_list_lcr_int.hpp"

LCR_last_visited_int::LCR_last_visited_int(GSA *gsa, Result_saver* rs) : LCR(rs) {
	this->gsa = gsa;
}

LCR_last_visited_int::~LCR_last_visited_int()
{
}

void LCR_last_visited_int::get_lcr(int x_repeats) {
	
	LV_list_lcr_int wl = LV_list_lcr_int(gsa->num_words, x_repeats, rs, gsa->get_max_lcp());
	
	for (int i=0; i<gsa->len; i++) {
			int lcp = gsa->lcp[i];
			int text = gsa->text(i);
			wl.lcp_update(lcp, i);
			wl.list_update(text, lcp, gsa->lcps[i], i);
	}
	wl.lcp_update(0, gsa->len);
}

