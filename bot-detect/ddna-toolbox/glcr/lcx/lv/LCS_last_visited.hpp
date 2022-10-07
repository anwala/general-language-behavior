#ifndef LCS_LAST_VISITED_HPP_
#define LCS_LAST_VISITED_HPP_

#include "../LCS.hpp"

/**
 * Implementation for LCS problem using last-visited list
 */
class LCS_last_visited : public LCS
{
public:
	LCS_last_visited(GSA *gsa, Result_saver* rs);
	virtual ~LCS_last_visited();
	void get_lcs();
};

#endif /*LCS_LAST_VISITED_HPP_*/
