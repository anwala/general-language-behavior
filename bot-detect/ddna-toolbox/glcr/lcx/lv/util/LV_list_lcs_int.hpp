#ifndef WORDLIST_LCS_INT_HPP_
#define WORDLIST_LCS_INT_HPP_

#include "LV_list_lcs.hpp"
#include "../../Result_saver.hpp"

class LV_list_lcs_int : public LV_list_lcs
{
private:
	LV_list_item **last_lcp;
public:
	LV_list_lcs_int(int num_words, Result_saver* rs, int max_lcp);
	virtual ~LV_list_lcs_int();
	void list_update(int text, int lcp, int textlcp, int index);
	void lcp_update(int lcp, int index);
//	void check_consistency(bool check_no_front_interval);
};

#endif /*WORDLIST_LCS_INT_HPP_*/

