#include "Result.hpp"
using namespace std;

Result::Result(int length, int num_texts, int begin, int end)
{
	this->length = length;
	this->num_texts = num_texts;
	this->begin = begin;
	this->end = end;
}

Result::~Result()
{
}

void Result::print() {
	cerr << "matches in different texts: " << num_texts;
	cerr << " length: " << length;
	cerr << " begin: " << begin;
	cerr << " end: " << end;
//	cerr << " subseq: " << subseq;
	cerr << endl;
}

void Result::write(ofstream *fout, GSA *gsa, char* all_sequences, short verbosity) {
	(*fout) << num_texts << "," << length << "," << begin << "," << end ;
	if(verbosity == 3){
		(*fout) << "," << string(all_sequences+(gsa->sa[begin]), length);
	}
	(*fout) << "\n";
}

void *Result::write_to_memory(GSA *gsa) {
	int nvecs  = 2;
	    double k[2] = {1., 2.};


	    npy_intp dims[1] = {nvecs};

	    PyObject *ret = PyArray_SimpleNew(1, dims, NPY_DOUBLE);
	    memcpy(PyArray_DATA(ret), k, nvecs*sizeof(double));
	    free(k);
	    pyprint(ret);
	return NULL;
}

void Result::pyprint(PyObject *o){
	PyObject* repr = PyObject_Repr(o);
	PyObject* str = PyUnicode_AsEncodedString(repr, "utf-8", "~E~");
	const char *bytes = PyBytes_AS_STRING(str);
	printf("\n\nREPR: %s\n", bytes);
	Py_XDECREF(repr);
	Py_XDECREF(str);
}
