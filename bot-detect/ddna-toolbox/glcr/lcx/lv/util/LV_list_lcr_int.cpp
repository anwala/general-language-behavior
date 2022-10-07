#include "LV_list_lcr_int.hpp"
#include <cassert>
LV_list_lcr_int::LV_list_lcr_int(int num_words, int x_repeats, Result_saver* rs, int max_lcp) :
	LV_list_lcr(num_words, x_repeats, rs)

{
	this->pqls = NULL;
	this->last_lcp = NULL;
	this->max_lcp = max_lcp;
	
	this->pqls = (Priority_QLS**)malloc(num_words*sizeof(Priority_QLS*));
	for (int i=0; i<num_words; i++)  {
		pqls[i] = new Priority_QLS(x_repeats);
		pqls[i]->add_value(0);
	}
	this->last_lcp = (LV_list_item**)calloc(max_lcp+1, sizeof(LV_list_item*));
	last_lcp[0] = &back;
	
	LV_list_item *begin = front.prev->prev;
	LV_list_item *end = back.next;
	begin->interval_end = end;
	end->interval_begin = begin;
	if (x_repeats>1) {
		end->interval_size = num_words;
	} else {
		end->interval_size = num_words-1;
	}
	
	front.prev->interval_end = back.next;
	back.next->interval_begin = front.prev;
	back.next->interval_size = num_words;
	last_lcp[0] = back.next;

}

LV_list_lcr_int::~LV_list_lcr_int()
{
	if (pqls!=NULL) {
		for (int i=0; i<num_words; i++)  {
			delete pqls[i];
		}
		free(pqls);
	}
	if (last_lcp!=NULL) {
		free(last_lcp);
	}
}


inline static void create_interval(LV_list_item* end, LV_list_item* begin, int lcp, int size) {
	end->interval_end = end;
	end->interval_begin = begin;
	
	begin->interval_end = end;
	begin->interval_begin = begin;
	
	end->interval_size = size;
	end->lcp = lcp;
	
}

void LV_list_lcr_int::list_update(int text, int lcp, int textlcp, int index) {
	LV_list_item *text_item = items[text][last_index[text]];
	last_index[text] = (last_index[text]+1) % x_repeats;
	
	pqls[text]->add_value(textlcp);
	int former_textlcp = pqls[text]->get_min();
	pqls[text]->remove_value();
	textlcp = pqls[text]->get_min();
	
	last_lcp[textlcp]->interval_size++;
	
	if (last_lcp[former_textlcp]!=text_item || text_item->interval_begin!=text_item) {
		
		// decrease interval size
		last_lcp[former_textlcp]->interval_size--;
		
		// if text_item is the end of an interval
		if (text_item==last_lcp[former_textlcp]) {
			create_interval(text_item->next, text_item->interval_begin, text_item->lcp, text_item->interval_size);
			
			if (last_lcp[text_item->lcp]==text_item) {
				last_lcp[text_item->lcp] = text_item->next;
			}
		}
		
		// if text_item is the beginning of an interval
		else if (text_item==last_lcp[former_textlcp]->interval_begin) {
			create_interval(text_item->interval_end, text_item->prev, text_item->interval_end->lcp, text_item->interval_end->interval_size);
		}
		
		// reset interval pointers
		text_item->interval_end  = text_item;
		text_item->interval_begin  = text_item;
	} else {
		last_lcp[text_item->lcp] = NULL;
	}
		
	if (x_repeats==1) {
		text_item->interval_size = 1;
	} else {
		text_item->interval_size = 0;
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

void LV_list_lcr_int::lcp_update(int lcp, int index) {
	LV_list_item *current = front.prev;
	LV_list_item *last_updated = current;
	
	current = current->prev;
	int list_pos = 0;
	
	while (lcp <= current->interval_end->lcp) {
		current = current->interval_end;
		last_updated = current;
		
		list_pos += current->interval_size;
		assert(list_pos<=num_words);
		
		rs->save_result(current->lcp, list_pos, current->index, index-1);
		
		if (last_lcp[last_updated->lcp]==last_updated) {
			last_lcp[last_updated->lcp] = NULL;
		}
		current = current->prev;
	}
	
	front.prev->interval_end = last_updated;
	last_updated->interval_begin = front.prev;
	
	last_updated->interval_size = list_pos;
	if (last_lcp[last_updated->lcp]==last_updated) {
		last_lcp[last_updated->lcp] = NULL;
	}
	last_updated->lcp = lcp;
	
	last_lcp[lcp] = last_updated;

}
