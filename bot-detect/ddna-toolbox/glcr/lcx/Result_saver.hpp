#ifndef RESULT_SAVER_HPP_
#define RESULT_SAVER_HPP_

#include <vector>
#include "../esa/GSA.hpp"
#include "Result.hpp"
#include <string.h>
#include <stdlib.h>
using namespace std;

class Result_saver
{
private:
	GSA* gsa;
	bool detailed_output;
	char* all_sequences;
	void save_result(Result* res);
public:
	std::vector<Result*> *results;
	std::vector<Result*> *preresults;
	int* result_lengths;
	Result_saver(GSA* gsa, bool detailed_output, char* all_sequences);
	virtual ~Result_saver();
	void save_preresult(int length, int num_texts, int begin, int end);
	void save_result(int length, int num_texts, int begin, int end);
	int* get_results();
	void print_results();
	void write_results(char *filename, short verbosity);
	void *write_results_to_memory(int num_words);
	void flush(int length);
	int import_numpy();
	void pyprint(PyObject *o);
};

#endif /*RESULT_SAVER_HPP_*/
