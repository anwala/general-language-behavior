#ifndef GLCR_LAST_VISITED_INT_HPP_
#define GLCR_LAST_VISITED_INT_HPP_

#include "../GLCR.hpp"
#include "../Result_saver.hpp"

/**
 * O(n) implementation for GLCR problem using last-visited list with intervals
 */
class GLCR_last_visited_int : public GLCR
{
public:
	GLCR_last_visited_int(GSA* gsa, Result_saver* rs);
	virtual ~GLCR_last_visited_int();
	void get_glcr(int* D);
};

#endif /*GLCR_LAST_VISITED_INT_HPP_*/
