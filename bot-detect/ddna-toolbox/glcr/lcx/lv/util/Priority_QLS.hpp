#ifndef PRIORITY_QLS_HPP_
#define PRIORITY_QLS_HPP_

#include "QLS_item.hpp"

class Priority_QLS
{
	private:
		int n;
		int index;
		
		QLS_item* qls_items;
		QLS_item* min_item;
		QLS_item* max_item;
		
	public:
		Priority_QLS(int n);
		virtual ~Priority_QLS();
		
		int get_min();
		void add_value(int value);
		void remove_value();
};

#endif /*PRIORITY_QLS_HPP_*/
