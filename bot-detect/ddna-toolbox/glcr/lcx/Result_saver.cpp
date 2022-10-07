#include "Result_saver.hpp"
#include <iostream>

#include "stdlib.h"
#include "stdio.h"
#include "string.h"


//------------------------ Start Utility to check memory usage----------------------
int parseLine(char* line){
    // This assumes that a digit will be found and the line ends in " Kb".
    int i = strlen(line);
    const char* p = line;
    while (*p <'0' || *p > '9') p++;
    line[i-3] = '\0';
    i = atoi(p);
    return i;
}

int getValue(){ //Note: this value is in KB!
    FILE* file = fopen("/proc/self/status", "r");
    int result = -1;
    char line[128];

    while (fgets(line, 128, file) != NULL){
        if (strncmp(line, "VmSize:", 7) == 0){
            result = parseLine(line);
            break;
        }
    }
    fclose(file);
    return result;
}
//------------------------ End Utility to check memory usage----------------------



Result_saver::Result_saver(GSA* gsa, bool detailed_output, char* all_sequences)
{
	this->gsa = gsa;
	this->all_sequences = all_sequences;
	this->detailed_output = detailed_output;
	result_lengths = new int[gsa->num_words+1];
	memset(result_lengths,0,(gsa->num_words+1)*sizeof(int));
	
	results = new std::vector<Result*>[gsa->num_words+1];
	preresults = new std::vector<Result*>();
	import_numpy();
}

Result_saver::~Result_saver()
{
	flush(0);
//	cout << "Used memory is " << getValue() <<endl;
//	sleep(5);
	for (int w=0; w<gsa->num_words; w++) {
		for (unsigned int i=0; i<results[w].size(); i++) {
			delete (results[w].at(i));
		}
	}
//	cout << "Used memory is " << getValue() <<endl;
	delete[] result_lengths;
//	cout << "Used memory is " << getValue() <<endl;
	delete[] results;
//	cout << "Used memory is " << getValue() <<endl;
	delete preresults;
//	cout << "Used memory is " << getValue() <<endl;
}

int Result_saver::import_numpy(){
	import_array();
    return 0;
}

void Result_saver::save_result(Result* res) {
	if (result_lengths[res->num_texts] <= res->length) {
		if (result_lengths[res->num_texts] < res->length) {
			for (unsigned int i=0; i<results[res->num_texts].size(); i++) {
				delete results[res->num_texts].at(i);
			}
			results[res->num_texts].clear();
			result_lengths[res->num_texts] = res->length;
		}
		results[res->num_texts].push_back(res);
	} else {
		delete res;
	}
	
}

void Result_saver::save_result(int length, int num_texts, int begin, int end) {
	if (detailed_output) {
		if (result_lengths[num_texts] <= length) {
			Result* res = new Result(length, num_texts, begin, end);
			if (result_lengths[res->num_texts] < res->length) {
				for (unsigned int i=0; i<results[res->num_texts].size(); i++) {
					delete results[res->num_texts].at(i);
				}
				results[res->num_texts].clear();
				result_lengths[res->num_texts] = res->length;
			}
			results[res->num_texts].push_back(res);
		}
	} else {
		if (result_lengths[num_texts] <= length) {
			result_lengths[num_texts] = length;
		}
		
	}
}


void Result_saver::save_preresult(int length, int num_texts, int begin, int end) {
//	if (result_lengths[num_texts]<=length) {
//		Result* res = new Result(length, num_texts, begin, end);
//		preresults->push_back(res);
//	}
}

void Result_saver::flush(int length) {
	for (unsigned int i=0; i<preresults->size(); i++) {
		Result* res = preresults->at(i);
		if (res->length > length) {
			save_result(res);
		} else {
			delete res;
		}
	}
	preresults->clear();
}

int* Result_saver::get_results() {
	int* result = (int*)calloc(gsa->num_words+1, sizeof(int));
	int last_value = 0;
	for (int i=gsa->num_words; i>=1; i--) {
		if (result_lengths[i] < last_value) {
			result[i] = last_value;
		} else {
			result[i] = result_lengths[i];
		}
		last_value = result[i];
	}
	
	return result;
}

void Result_saver::print_results() {
	for (int w=1; w<=gsa->num_words; w++) {
		for (unsigned int i=0; i<results[w].size(); i++) {
			Result* res = results[w].at(i);
			res->print();
		}
	}
}

void Result_saver::write_results(char *filename, short verbosity) {
	ofstream fout;
	fout.open(filename, ofstream::out | ofstream::app);
	fout << "num_texts,length,begin,end";
	if(verbosity == 3)	fout << ",subsequence";
	fout << "\n";
	for (int w=1; w<=gsa->num_words; w++) {
		for (unsigned int i=0; i<results[w].size(); i++) {
			Result* res = results[w].at(i);
			res->write(&fout, gsa, all_sequences, verbosity);
		}
	}
	fout.close();
}

void Result_saver::pyprint(PyObject *o){
	PyObject* repr = PyObject_Repr(o);
	PyObject* str = PyUnicode_AsEncodedString(repr, "utf-8", "~E~");
	const char *bytes = PyBytes_AS_STRING(str);
	printf("\n\nREPR: %s\n", bytes);
	Py_XDECREF(repr);
	Py_XDECREF(str);
}

void *Result_saver::write_results_to_memory(int num_words) {

	int n_rows = 0;
	for (int w=1; w<=gsa->num_words; w++)
		n_rows += results[w].size();
	const short n_dims = 2;
	npy_intp dims[n_dims] = { (npy_intp)n_rows, (npy_intp)1 };
	PyObject *op, *array;
	PyArray_Descr *descr;
	op = Py_BuildValue("[(s, s),(s, s)]", "num_texts", "int", "length", "int");
	PyArray_DescrConverter(op, &descr);
	Py_DECREF(op);
	array = PyArray_SimpleNewFromDescr(n_dims, dims, descr);
	int k = 0;
	for (int w=1; w<=gsa->num_words; w++) {
		for (unsigned int i=0; i<results[w].size(); i++) {
			Result* res = results[w].at(i);
			void *p = PyArray_GETPTR1(array, (npy_intp) k);
			PyObject *row = Py_BuildValue("(ii)", res->num_texts, res->length);
			PyArray_SETITEM(array, p, row);
			Py_DecRef(row);
			delete res;
			k++;
			}
		}
	return array;
}
//void *Result_saver::write_results_to_memory() {
////	Not Efficient implementation, use with caution
//
//	cout << "PyList_New\n";
//	sleep(2);
//	PyObject *list = PyList_New(0);
//	sleep(2);
//	PyObject *row = NULL;
//
//
//	cout << "Appending...\n";
//	sleep(2);
//	for (int w=1; w<=gsa->num_words; w++) {
//		for (unsigned int i=0; i<results[w].size(); i++) {
//			Result* res = results[w].at(i);
//			row = Py_BuildValue("(iiii)",
//					res->num_texts,
//					res->length,
//					res->begin,
//					res->end);
//			PyList_Append(list, row);
//			Py_DecRef(row);
//		}
//	}
//	sleep(2);
//	cout << "Appended\n";
//
//	PyObject *op;
//	PyArray_Descr *descr;
//	op = Py_BuildValue("[(s, s),(s, s),(s, s),(s, s)]", "num_texts", "int",	"length", "int", "begin", "int", "end", "int");
//	PyArray_DescrConverter(op, &descr);
//	cout << "Converting...\n";
//	sleep(2);
//	PyObject *array =  PyArray_FromAny(list, descr, 0, 0, 0, NULL);
//	sleep(2);
//	cout << "Converted\n";
//	Py_DecRef(op);
//	Py_DecRef(list);
//	return array;
//}

