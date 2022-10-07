#ifndef GLCR_HPP_
#define GLCR_HPP_

#include "LCR.hpp"

class GLCR : public LCR
{
public:
	GLCR(Result_saver* rs);
	virtual ~GLCR();
};

#endif /*GLCR_HPP_*/
