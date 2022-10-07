#include "LCS_last_visited_int.hpp"

#include "util/LV_list_lcs_int.hpp"

LCS_last_visited_int::LCS_last_visited_int(GSA *gsa, Result_saver* rs) : LCS(rs) {
	this->gsa = gsa;
}

LCS_last_visited_int::~LCS_last_visited_int()
{
}

void LCS_last_visited_int::get_lcs() {
	LV_list_lcs_int wl = LV_list_lcs_int(gsa->num_words, rs, gsa->get_max_lcp());
	
	for (int i=0; i<gsa->len; i++) {
			int lcp = gsa->lcp[i];
			int text = gsa->text(i);

			wl.lcp_update(lcp, i);
			
			wl.list_update(text, lcp, gsa->lcps[i], i);
	}
	wl.lcp_update(0, gsa->len);
}
