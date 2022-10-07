#include "LV_list_lcs_int.hpp"
#include <stdlib.h>
#include <cassert>

LV_list_lcs_int::LV_list_lcs_int(int num_words, Result_saver *rs, int max_lcp) : LV_list_lcs(num_words, rs)
{
	back.interval_size = 0;
	front.interval_size = 0;
	this->last_lcp = (LV_list_item**)calloc(max_lcp+1, sizeof(LV_list_item*));
}

LV_list_lcs_int::~LV_list_lcs_int() {
	free(last_lcp);
}

inline static void create_interval(LV_list_item* end, LV_list_item* begin, int lcp, int size) {
	end->interval_end = end;
	end->interval_begin = begin;
	
	begin->interval_end = end;
	begin->interval_begin = begin;
	
	end->interval_size = size;
	end->lcp = lcp;
	
}

void LV_list_lcs_int::list_update(int text, int lcp, int textlcp, int index) {
	LV_list_item *text_item = items[text];
	
	if (last_lcp[textlcp]!=text_item || text_item->interval_begin!=text_item) {
		
		// decrease interval size
		last_lcp[textlcp]->interval_size--;
		
		// if text_item is the end of an interval
		if (text_item==last_lcp[textlcp]) {
			create_interval(text_item->next, text_item->interval_begin, text_item->lcp, text_item->interval_size);
			
			last_lcp[text_item->lcp] = text_item->next;
		}
		
		// if text_item is the beginning of an interval
		else if (text_item==last_lcp[textlcp]->interval_begin) {
			create_interval(text_item->interval_end, text_item->prev, text_item->interval_end->lcp, text_item->interval_end->interval_size);
		}
		
		// reset interval pointers
		text_item->interval_end  = text_item;
		text_item->interval_begin  = text_item;
		text_item->interval_size = 1;
	}
		
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

void LV_list_lcs_int::lcp_update(int lcp, int index) {
	LV_list_item *current = front.prev;
	LV_list_item *last_updated = current;
	
	current = current->prev;
	int list_pos = 1;
	
	while (lcp <= current->interval_end->lcp) {
		current = current->interval_end;
		last_updated = current;
		
		list_pos += current->interval_size;
		
		rs->save_result(current->lcp, list_pos, current->index, index-1);
		
		current = current->prev;
	}
	
	front.prev->interval_end = last_updated;
	last_updated->interval_begin = front.prev;
	
	last_updated->interval_size = list_pos;
	last_updated->lcp = lcp;
	
	last_lcp[lcp] = last_updated;

}
/*
void LV_list_lcs_int::check_consistency(bool check_no_front_interval) {
	// check next-pointers
	LV_list_item* current = &this->back;
	for (int i=0; i<=this->n; i++) {
		assert (current->next->prev ==current);
		current = current->next;
	}
	assert(current==&this->front);
	
	
	// check prev-pointers
	current = &this->front;
	for (int i=0; i<=this->n; i++) {
		assert (current->prev->next ==current);
		current = current->prev;
	}
	assert (current==&this->back);
	
	// check intervals
	current = front.prev;
	if (check_no_front_interval) assert(current->interval_end == current);
	int listpos = 1;
	while (listpos<=this->n) {
		if (current->interval_end==current) {
			listpos++;
			if (current->interval_begin==current) {
				assert(current->interval_size==1);
			}
			assert(current->prev->interval_begin == current->prev);
			if (current->prev->interval_end == current->prev) {
				assert(current->prev->interval_size == 1);
			}
			current = current->prev;
		} else {
			LV_list_item* next = current->interval_end;
			assert(next->interval_end == next);
			listpos+=next->interval_size;
			
			assert(current->interval_end->interval_begin == current);
			assert(current->interval_end->interval_size>1);
			for (int i=0; i<next->interval_size-1; i++) {
				current = current->prev;
			}
			assert(next==current);
			assert(current->interval_end == current);
			current = current->prev;
		}
	}
	assert(current==&back);
}
*/








