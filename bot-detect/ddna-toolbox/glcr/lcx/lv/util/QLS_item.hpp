#ifndef QLS_ITEM_HPP_
#define QLS_ITEM_HPP_

class QLS_item
{
	private:
		int value;
		bool enabled;
		
		QLS_item* lesser;
		QLS_item* greater;
		
	public:
		QLS_item();
		virtual ~QLS_item();
		int get_value();
		void set_value(int value);
		void set_value(int value, QLS_item* max_item);
		void remove();
		void disable();
		QLS_item* get_greater();
};

#endif /*QLS_ITEM_HPP_*/
