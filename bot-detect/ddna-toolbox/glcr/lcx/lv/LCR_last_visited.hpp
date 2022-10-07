#ifndef LCR_LAST_VISITED_HPP_
#define LCR_LAST_VISITED_HPP_

#include "../LCR.hpp"

/**
 * Implementation for LCS problem using last-visited list
 */
class LCR_last_visited : public LCR
{
		
public:
	LCR_last_visited(GSA *gsa, Result_saver* rs);
	virtual ~LCR_last_visited();
	void get_lcr(int x_repeats);
};

#endif /*LCR_LAST_VISITED_HPP_*/
