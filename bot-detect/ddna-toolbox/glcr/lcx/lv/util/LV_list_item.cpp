#include "LV_list_item.hpp"

LV_list_item::LV_list_item()
{
	this->lcp = 0;
	this->interval_end = this;
	this->interval_begin = this;
	this->interval_size = 1;
	clean = true;
}

LV_list_item::LV_list_item(int text) {
	this->text = text;
//	this->repeat_index = repeat_index;
	this->lcp = 0;
	this->interval_end = this;
	this->interval_begin = this;
	this->interval_size = 1;
	clean = true;
}
LV_list_item::~LV_list_item()
{
}
