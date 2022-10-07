#ifndef LCS_LAST_VISITED_INT_HPP_
#define LCS_LAST_VISITED_INT_HPP_

#include "../LCS.hpp"

/**
 * O(n) implementation for LCS problem using last-visited list with intervals
 */
class LCS_last_visited_int : public LCS
{
public:
	LCS_last_visited_int(GSA *gsa, Result_saver* rs);
	virtual ~LCS_last_visited_int();
	void get_lcs();
};

#endif /*LCS_LAST_VISITED_INT_HPP_*/
