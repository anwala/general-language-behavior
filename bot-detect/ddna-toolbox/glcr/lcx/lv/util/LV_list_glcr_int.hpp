#ifndef WORDLIST_GLCR_INT_HPP_
#define WORDLIST_GLCR_INT_HPP_
#include "Priority_QLS.hpp"
#include "LV_list_item.hpp"
#include <stdlib.h>
#include "../../Result_saver.hpp"

class LV_list_glcr_int
{
private:
	LV_list_item*** items;
	LV_list_item back;
	LV_list_item front;
	
	Result_saver *rs;
	int num_words;
	int *D;
	int *list_sizes;
	int *last_index;
	
	LV_list_item **last_lcp;
	int max_lcp;
	Priority_QLS** pqls;
public:
	LV_list_glcr_int(int num_words, int* D, Result_saver *rs, int max_lcp);
	virtual ~LV_list_glcr_int();
	void lcp_update(int lcp, int text, bool clean);
	void list_update(int index, int text, int lcp, int textlcp);

	void check_consistency(bool check_no_front_interval);
};

#endif /*WORDLIST_LCR_INT_HPP_*/
