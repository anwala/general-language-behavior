#include "QLS_item.hpp"

QLS_item::QLS_item() {
	enabled = false;
	greater = this;
	lesser = this;
}

QLS_item::~QLS_item() {
}

int QLS_item::get_value() {
	return value;
}

void QLS_item::set_value(int value)  {
	this->value = value;
}

void QLS_item::set_value(int value, QLS_item* max_item) {
	this->enabled = true;
	this->value = value;
	while(max_item->value >= value) {
		max_item->disable();
		max_item = max_item->lesser;
	}
	max_item->greater = this;
	this->lesser = max_item;
	this->greater = this;
}

void QLS_item::remove() {
	if (enabled) {
		lesser->greater = greater;
		greater->lesser = lesser;
	}
} 

QLS_item* QLS_item::get_greater() {
	return greater;
}

void QLS_item::disable() {
	this->enabled = false;
}
