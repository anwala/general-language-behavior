#include "LV_list_lcr.hpp"

#include <cassert>

LV_list_lcr::LV_list_lcr(int num_words, int x_repeats, Result_saver* rs) : 
		back(),
		front()
{
	this->num_words = num_words;
	this->x_repeats = x_repeats;
	this->rs = rs;
	items = (LV_list_item***)malloc(num_words*sizeof(LV_list_item**));
	
	LV_list_item *last_item = &back;
	back.prev = NULL;
	for (int i=0; i<num_words; i++) {
		items[i] = (LV_list_item**)malloc(x_repeats*sizeof(LV_list_item*));
		for (int j=0; j<x_repeats; j++) {
			items[i][j] = new LV_list_item(i);
			items[i][j]->interval_size = 0;
			items[i][j]->prev = last_item;
			if (last_item!=NULL) {
				last_item->next = items[i][j];
			}
			last_item = items[i][j];
		}
		items[i][0]->interval_size = 1;
	}
	last_item->next = &front;
	front.prev = last_item;
	front.next = NULL;
	
	
	front.lcp = -1;
	back.lcp = -2;
	
	this->last_index = (int*)calloc(num_words, sizeof(int));
}

LV_list_lcr::~LV_list_lcr() {
	for (int i=0; i<num_words; i++) {
		for (int j=0; j<x_repeats; j++) {
			delete(items[i][j]);
		}
		free(items[i]);
	}
	free(items);
	free(last_index);
}

int LV_list_lcr::get_front_lcp() {
	LV_list_item *front_item = front.prev;
	return front_item->prev->lcp;
}

void LV_list_lcr::list_update(int text, int lcp, int index) {
	LV_list_item *text_item = items[text][last_index[text]];
	last_index[text] = (last_index[text]+1) % x_repeats;
	
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

//TODO: anpassen!
void LV_list_lcr::lcp_update(int lcp, int index) {
	LV_list_item *current = front.prev->prev;
	int numtexts = 0;
	while (current->lcp > lcp) {
		numtexts += (items[current->text][last_index[current->text]]==current);
		
		rs->save_result(current->lcp, numtexts, current->index, index-1);
		
		current->lcp = lcp;
		current = current->prev;
	}
}

