#ifndef LCS_HPP_
#define LCS_HPP_

#include "LCX.hpp"

class LCS : public LCX
{
public:
	LCS(Result_saver *rs);
	virtual ~LCS();
	virtual void get_lcs() {};
};

#endif /*LCS_HPP_*/
