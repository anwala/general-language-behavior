#ifndef WORDLIST_LCS_HPP_
#define WORDLIST_LCS_HPP_
#include "LV_list_item.hpp"
#include "../../Result_saver.hpp"

class LV_list_lcs
{
public:
	LV_list_item** items;
	LV_list_item back;
	LV_list_item front;
	
	int num_words;
	Result_saver *rs;
//	int count;
	LV_list_lcs(int num_words, Result_saver* rs);
	
	virtual ~LV_list_lcs();
	
	int get_front_lcp();
	void lcp_update(int lcp, int index);
	void list_update(int text, int lcp, int index);
};

#endif /*WORDLIST_LCS_HPP_*/
