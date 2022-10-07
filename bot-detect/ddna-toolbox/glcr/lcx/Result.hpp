#include <fstream>
#include "../esa/GSA.hpp"
#include "numpy/arrayobject.h"
#include <Python.h>
#include <stdlib.h>
#include <iostream>
#include <string>

#ifndef RESULT_HPP_
#define RESULT_HPP_


class Result
{
public:
	int length;
	int num_texts;
	int begin;
	int end;
	Result(int length, int num_texts, int begin, int end);
	virtual ~Result();
	void print();
	void write(std::ofstream *fout, GSA *gsa, char *all_sequences, short verbosity);
	void *write_to_memory(GSA *gsa);
	void pyprint(PyObject *o);
};

#endif /*RESULT_HPP_*/
