#ifndef LCR_HPP_
#define LCR_HPP_

#include "LCX.hpp"
#include "Result_saver.hpp"

class LCR : public LCX
{
public:
	LCR(Result_saver *rs);
	virtual ~LCR();
	void get_lcs();
	virtual void get_lcr(int x_repeats) {};
};

#endif /*LCR_HPP_*/
