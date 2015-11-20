/////////////////////
// loader.c
// Noah Ansel
// 2015-11-19
// -----------------
// See loader.h for info.
/////////////////////

#include "loader.h"
#include "main.h"

ErrCode loadFile(char filename[]) {
	char found_start = 0; // bool to prevent using multiple # operators
	int idx = 0; // tracks when it should cut off for next
	char storage[3];
	
	FILE* fp = fopen(filename, "r");
	if (fp == NULL) {
		printf("MISSING_FILE\n");
		return MISSING_FILE;
	}
	
	PROGRAM_ORIGIN = malloc(sizeof(FileLine));
	PROGRAM_ORIGIN->num_cols = 0;
	PROGRAM_ORIGIN->strings = NULL;
	PROGRAM_ORIGIN->next_line = NULL;
	PROGRAM_ORIGIN->prev_line = NULL;

	storage[idx] = fgetc(fp);
	
	while (storage[idx] != '\n' && storage[idx] != EOF) {
	
		idx = (idx + 1) % 3;
		storage[idx] = fgetc(fp);
		if (idx == 2) {
			printf("|%c%c%c|\n", storage[0], storage[1], storage[2]);
		}
	}
	while (idx < 3) {
		storage[idx] = ' ';
		idx++;
	}
	printf("|%c%c%c|\n", storage[0], storage[1], storage[2]);

	fclose(fp);

	return NO_ERROR;
}