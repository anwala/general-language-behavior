#ifndef LCR_LAST_VISITED_INT_HPP_
#define LCR_LAST_VISITED_INT_HPP_

#include "../LCR.hpp"

/**
 * O(n) implementation for LCR problem using last-visited list with intervals
 */
class LCR_last_visited_int : public LCR
{
		
public:
	LCR_last_visited_int(GSA *gsa, Result_saver* rs);
	virtual ~LCR_last_visited_int();
	void get_lcr(int x_repeats);
};

#endif /*LCR_LAST_VISITED_INT_HPP_*/
