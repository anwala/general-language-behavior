#ifndef WORDLIST_ITEM_HPP_
#define WORDLIST_ITEM_HPP_

class LV_list_item
{
public:
	LV_list_item* next;
	LV_list_item* prev;
	int text;
	int lcp;
	int index;
	bool clean;
	
	LV_list_item* interval_end;
	LV_list_item* interval_begin;
	int interval_size;
	
	LV_list_item();
	LV_list_item(int text);
	virtual ~LV_list_item();
	
};

#endif /*WORDLIST_ITEM_HPP_*/
