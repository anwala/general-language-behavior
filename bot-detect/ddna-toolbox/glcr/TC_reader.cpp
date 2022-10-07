#include "TC_reader.hpp"
#include <ctime>
using namespace std;

TC_reader::TC_reader() {
	wordbegin = (int*)malloc(10*sizeof(int));
	wordbegin_size = 10;
	testcase_counter = 0;
}

TC_reader::~TC_reader() {
	free(wordbegin);
}

GSA* TC_reader::read_testcase(char* filename) {
	FILE *file;
	file = fopen(filename, "r");
	if(!file){
		cerr << "\nERROR: Cannot open the file!" << filename << endl;
		throw "Cannot open the file!";
	}

	int alphabet_size = 0;
	int num_words;
	fscanf(file,"%d\n",&num_words); //	First row of the input file, contains the number of sequences (rows) to read
	cout << "File correctly read, num_words is " << num_words << endl;
	if (num_words > wordbegin_size) {
		wordbegin = (int*)realloc(wordbegin, (num_words+1)*sizeof(int));
		wordbegin_size = num_words;
	}
	int len=0;
	//	Read file by row
	for(int i=1; i<=num_words; i++)	{
		wordbegin[i-1]=len;
		fgets(buf+len, MAXLEN-len, file);
		int l = strlen(buf+len);				// Length of current sequence
		if (buf[len+l-1]<32) {
			l--;
			buf[len+l] = 0;
		}
		//	For each letter in sequence evaluate the alphabet size (e.g. for A=[a] is 1, for A=[a,...z] is 25)
		for(int j=0; j<l; j++) {
			text[len]=buf[len]-31+num_words;
			if (text[len]>alphabet_size) {
				alphabet_size = text[len];
			}
			len++;
		}
		buf[len]=0;
		text[len]=i;
		len++;
	}
	text[len]=text[len+1]=text[len+2]=0;
	buf[len]=0;
	wordbegin[num_words]=len;
	alphabet_size++;
	cerr << "Computing Enhanced Generalized Suffix Array..." << endl;
	GSA* gsa = new GSA(text, len, alphabet_size, wordbegin, num_words);
	//	gsa->pprint();
	cerr << "done." << endl;
	return gsa;

}

/**
 * Computes the Generalized Suffix Array given a set of sequences specified as parameter.
 *
 * @param sequences	the reference to the set of sequences
 * @return the Generalized Suffix Array as reference to GSA object.
 */
GSA* TC_reader::read_testcase(char** sequences, int num_words){
	int alphabet_size = 0;
	if (num_words > wordbegin_size) {
		wordbegin = (int*)realloc(wordbegin, (num_words+1)*sizeof(int));
		wordbegin_size = num_words;
	}
	int len=0;
	//	Read file by row, compute suffixes and store in buf
	for(int i=1; i<=num_words; i++)	{
		wordbegin[i-1]=len;
		strncpy(buf+len,sequences[i-1],MAXLEN-len);
		int l = strlen(buf+len);				// Length of current suffix
		if (buf[len+l-1]<32) {
			l--;
			buf[len+l] = 0;
		}
		//	For each letter in sequence evaluate the alphabet size (e.g. for A=[a] is 1, for A=[a,...z] is 25)
		for(int j=0; j<l; j++) {
			text[len]=buf[len]-31+num_words;
			if (text[len]>alphabet_size) {
				alphabet_size = text[len];
			}
			len++;
		}
		buf[len]=0;
		text[len]=i;
		len++;
	}
	text[len]=text[len+1]=text[len+2]=0;
	buf[len]=0;
	wordbegin[num_words]=len;
	alphabet_size++;
	cerr << "Computing Enhanced Generalized Suffix Array..." << endl;
	GSA* gsa = new GSA(text, len, alphabet_size, wordbegin, num_words);
	cerr << "done." << endl;
	return gsa;
}

