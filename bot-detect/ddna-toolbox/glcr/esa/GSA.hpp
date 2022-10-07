#ifndef GSA_HPP_
#define GSA_HPP_

#include "../esa/typedefs.h"

class GSA
{
	public:
		int len;
		int* wordbegin;
		int num_words;
		
		int* sa;
		int* inv_sa;
		int* lcp;
		int* wordindex;
		
		int* otext;
		int* lcps;
	
	public:
		GSA(int* text, int len, int alphabet_size, int* wordbegin, int num_words);
		GSA(char* filename);
		virtual ~GSA();
		
		int text(int i);
		void init_lcps();
		int get_max_lcp();
		void print(char* buf);
		void write(char* filename, char* buf);
		void write_tiny(char* filename, char* buf);
		void read();
		bool equals(GSA *gsa);
	private:
		void init_wordindex();
		void inv_suffixArray(int* sa, int len);
		
};

#endif /*GSA_HPP_*/
