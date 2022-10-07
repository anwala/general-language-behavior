#include "LV_list_glcr_int.hpp"

LV_list_glcr_int::LV_list_glcr_int(int num_words, int* D, Result_saver *rs, int max_lcp)

{
	this->num_words = num_words;
	this->D = D;
	this->list_sizes = new int[num_words];
	
	for (int i=0; i<num_words; i++) {
		if (D[i]>0) {
			list_sizes[i] = D[i];
		} else {
			list_sizes[i] = 1;
		}
	}
	
	this->rs = rs;
	items = (LV_list_item***)malloc(num_words*sizeof(LV_list_item**));
	
	LV_list_item *last_item = &back;
	back.prev = NULL;
	for (int i=0; i<num_words; i++) {

		items[i] = (LV_list_item**)malloc(list_sizes[i]*sizeof(LV_list_item*));
		for (int j=0; j<list_sizes[i]; j++) {
			items[i][j] = new LV_list_item(i);
			items[i][j]->interval_size = 0;
			items[i][j]->prev = last_item;
			if (last_item!=NULL) {
				last_item->next = items[i][j];
			}
			last_item = items[i][j];
		}
		if (D[i]>0) items[i][0]->interval_size = 1;
	}
	last_item->next = &front;
	front.prev = last_item;
	front.next = NULL;
	
	
	front.lcp = -1;
	back.lcp = -2;
	
	this->last_index = (int*)calloc(num_words, sizeof(int));
	this->pqls = NULL;
	this->last_lcp = NULL;
	this->max_lcp = max_lcp;
	
	this->pqls = (Priority_QLS**)malloc(num_words*sizeof(Priority_QLS*));
	for (int i=0; i<num_words; i++)  {
		pqls[i] = new Priority_QLS(list_sizes[i]);
		pqls[i]->add_value(0);
	}
	this->last_lcp = (LV_list_item**)calloc(max_lcp+1, sizeof(LV_list_item*));
	last_lcp[0] = &back;
	
	LV_list_item *begin = front.prev->prev;
	LV_list_item *end = back.next;
	begin->interval_end = end;
	end->interval_begin = begin;
	if (D[front.prev->text]>1) {
		end->interval_size = num_words;
	} else {
		end->interval_size = num_words-1;
	}
	for (int i=0; i<num_words-1; i++) {
		if (D[i]==0) {
			end->interval_size = -1;
			end->clean = false;
		}
	}
	
	last_lcp[0] = end;

}

LV_list_glcr_int::~LV_list_glcr_int()
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
	
	for (int i=0; i<num_words; i++) {
		for (int j=0; j<list_sizes[i]; j++) {
			delete(items[i][j]);
		}
		free(items[i]);
	}
	delete[] list_sizes;
	free(items);
	free(last_index);
}


inline static void create_interval(LV_list_item* end, LV_list_item* begin, int lcp, int size, bool clean) {
	end->interval_end = end;
	end->interval_begin = begin;
	
	begin->interval_end = end;
	begin->interval_begin = begin;
	
	end->interval_size = size;
	end->lcp = lcp;
	end->clean = clean;
}

void LV_list_glcr_int::list_update(int index, int text, int lcp, int textlcp) {
	LV_list_item *text_item = items[text][last_index[text]];
	last_index[text] = (last_index[text]+1) % list_sizes[text];
	
	pqls[text]->add_value(textlcp);
	int former_textlcp = pqls[text]->get_min();
	pqls[text]->remove_value();
	textlcp = pqls[text]->get_min();
	
	if (D[text]>1 && last_lcp[textlcp]->interval_size>=0) {
		last_lcp[textlcp]->interval_size++;
	}
	
	if (last_lcp[former_textlcp]!=text_item || text_item->interval_begin!=text_item) {
		
		// decrease interval size
		if (D[text]!=0 && last_lcp[textlcp]->interval_size>=0) {
			last_lcp[former_textlcp]->interval_size--;
		}
		
		// if text_item is the end of an interval
		if (text_item==last_lcp[former_textlcp]) {
			create_interval(text_item->next, text_item->interval_begin, text_item->lcp, text_item->interval_size, text_item->clean);
			
			if (last_lcp[text_item->lcp]==text_item) {
				last_lcp[text_item->lcp] = text_item->next;
			}
		}
		
		// if text_item is the beginning of an interval
		else if (text_item==last_lcp[former_textlcp]->interval_begin) {
			create_interval(text_item->interval_end, text_item->prev, text_item->interval_end->lcp, text_item->interval_end->interval_size, text_item->interval_end->clean);
		}
		
		// reset interval pointers
		text_item->interval_end  = text_item;
		text_item->interval_begin  = text_item;
	}
	if (D[text]==1) {
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
	if (D[text]>0) {
		text_item->clean = true;
	}
	text_item->index = index;
}

void LV_list_glcr_int::lcp_update(int lcp, int text, bool clean) {
	LV_list_item *current = front.prev;
	LV_list_item *last_updated = current;
	
	clean &= current->clean;
	int list_pos = 0;
	if (D[current->text]==1) {
		list_pos = 1;
	}
		
	current = current->prev;
	
	while (lcp <= current->interval_end->lcp) {
		current = current->interval_end;
		clean &= current->clean;

		last_updated = current;
		
		
		list_pos += current->interval_size;
		if (clean) {
			rs->save_preresult(current->lcp, list_pos, current->index, front.prev->index);
		}
		current = current->prev;
	}
	
	LV_list_item* begin = front.prev;
	
	begin->interval_end = last_updated;
	last_updated->interval_begin = begin;
	last_updated->interval_size = list_pos;
	last_updated->clean = clean;
	last_updated->lcp = lcp;
	
	last_lcp[lcp] = last_updated;

}
