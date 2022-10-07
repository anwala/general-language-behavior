#ifndef WORDLIST_lcr_HPP_
#define WORDLIST_lcr_HPP_
#include "LV_list_item.hpp"
#include <stdlib.h>
#include "../../Result_saver.hpp"

class LV_list_lcr
{
protected:
	LV_list_item*** items;
	LV_list_item back;
	LV_list_item front;
	
	int num_words;
	int x_repeats;
	Result_saver *rs;
	int *last_index;
	
public:	
	LV_list_lcr(int num_words, int x_repeats, Result_saver* rs);
	
	virtual ~LV_list_lcr();
	
	int get_front_lcp();
	
	void lcp_update(int lcp, int index);
	void list_update(int text, int lcp, int index);
	
};

#endif /*WORDLIST_HPP_*/
