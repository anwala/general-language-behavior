#ifndef TC_READER_HPP_
#define TC_READER_HPP_

#include "esa/GSA.hpp"
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <iostream>

#define MAXLEN 50000000

class TC_reader
{
private:
	int* wordbegin;
	int wordbegin_size;
	int testcase_counter;
public:
	int text[MAXLEN];
	char buf[MAXLEN];
	
	GSA* read_testcase(char* filename);
	GSA* read_testcase(char** sequences, int num_words);
	
	TC_reader();
	virtual ~TC_reader();
};

#endif /*TC_READER_HPP_*/
