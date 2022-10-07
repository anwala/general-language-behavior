#include "LCR.hpp"

LCR::LCR(Result_saver *rs) : LCX(rs) 
{
}

LCR::~LCR()
{
}

void LCR::get_lcs() {
	return get_lcr(1);
}

