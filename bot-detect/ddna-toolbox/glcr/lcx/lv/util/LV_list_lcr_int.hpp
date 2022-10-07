#ifndef WORDLIST_LCR_INT_HPP_
#define WORDLIST_LCR_INT_HPP_
#include "Priority_QLS.hpp"

#include "LV_list_lcr.hpp"
#include "../../Result_saver.hpp"

class LV_list_lcr_int : public LV_list_lcr
{
private:
	LV_list_item **last_lcp;
	int max_lcp;
	Priority_QLS** pqls;

public:
	LV_list_lcr_int(int num_words, int x_repeats, Result_saver* rs, int max_lcp);
	virtual ~LV_list_lcr_int();
	void lcp_update(int lcp, int index);
	void list_update(int text, int lcp, int textlcp, int index);

//	void check_consistency(bool check_no_front_interval);
};

#endif /*WORDLIST_LCR_INT_HPP_*/
