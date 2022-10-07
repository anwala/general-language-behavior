#include "Priority_QLS.hpp"
#include <cstdlib>

Priority_QLS::Priority_QLS(int n) {
	this->n = n;
	this->index = 0;
	
	qls_items = new QLS_item[n];
	min_item = new QLS_item();
	min_item->set_value(-1);
	max_item = min_item;
}

Priority_QLS::~Priority_QLS() {
	delete[] qls_items;
	delete min_item;
}

int Priority_QLS::get_min() {
	return min_item->get_greater()->get_value();
}

void Priority_QLS::add_value(int value) {
	index++;
	if (index>=n) {
		index = 0;
	}
//	qls_items[index].remove();
	qls_items[index].set_value(value, max_item);
	max_item=&qls_items[index];
}

void Priority_QLS::remove_value() {
	qls_items[(index+1)%n].remove();
}

