#ifndef LCX_HPP_
#define LCX_HPP_

#include <cstdlib>
#include "Result_saver.hpp"
#include "../esa/GSA.hpp"

/**
 * Abstract base class for all problems (LCS, LCR, GLCR)
 */
class LCX
{
protected:
	Result_saver* rs;
	GSA *gsa;
public:
	LCX(Result_saver* rs);
	virtual ~LCX();
	virtual void get_lcs() {};
	virtual void get_lcr(int x_repeats) {};
};

#endif /*LCX_HPP_*/
