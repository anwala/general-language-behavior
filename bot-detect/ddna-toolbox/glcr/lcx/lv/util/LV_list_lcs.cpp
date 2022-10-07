#include "LV_list_lcs.hpp"
#include <stdlib.h>
#include <cassert>
LV_list_lcs::LV_list_lcs(int num_words, Result_saver* rs) : 
		back(),
		front()
{
	back.lcp = -1;
	front.lcp = -1;
	this->num_words = num_words;
	this->rs = rs;
	
	items = (LV_list_item**)malloc(num_words*sizeof(LV_list_item*));
	LV_list_item *last_item = &back;
	back.prev = NULL;
	for (int i=0; i<num_words; i++) {
		items[i] = new LV_list_item();
		items[i]->prev = last_item;
		if (last_item!=NULL) {
			last_item->next = items[i];
		}
		last_item = items[i];
	}
	last_item->next = &front;
	front.prev = last_item;
	front.next = NULL;
//	count = 0;
}

LV_list_lcs::~LV_list_lcs() {
	for (int i=0; i<num_words; i++) {
		delete items[i];
	}
	free(items);
}

int LV_list_lcs::get_front_lcp() {
	LV_list_item *front_item = front.prev;
	return front_item->prev->lcp;
}

void LV_list_lcs::list_update(int text, int lcp, int index) {
	LV_list_item *text_item = items[text];
	
	if (front.prev!=text_item) {
		// adjust pointers at old position
		text_item->next->prev = text_item->prev;
		text_item->prev->next = text_item->next;
		
		// adjust pointers at new position
		text_item->prev = front.prev;
		text_item->next = &front;
		
		text_item->prev->next = text_item;
		front.prev = text_item;
	
		// update lcp value
		text_item->prev->lcp = lcp;
	}
	text_item->index = index;
}

void LV_list_lcs::lcp_update(int lcp, int index) {
	LV_list_item *current = front.prev->prev;
	int numtexts = 2;
	while (current->lcp > lcp) {
		rs->save_result(current->lcp, numtexts, current->index, index-1);
		current->lcp = lcp;
		current = current->prev;
		numtexts++;
//		count++;
	}
}
