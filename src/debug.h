/////////////////////
// debug.h
// Noah Ansel
// 2015-11-19
// -----------------
// Helpful functions for debugging programs
// or the interpreter.
/////////////////////

#pragma once

#include "main.h"


ErrCode dump_VAR_SPACE() {
	FILE* fp = fopen(DEBUG_FILENAME, "a");
	if (fp == NULL) {
		return INVALID_DEBUG_FILE;
	}
	fprintf(fp, ".VAR_SPACE dump--.\n");
	printf(".VAR_SPACE dump--.\n");
	for (int i = 0; i < VARSPACE_SIZE; i++) {
		fprintf(fp,"|");
		printf("|");
		for (int j = 0; j < VARSPACE_SIZE; j++) {
			if (VAR_SPACE[i][j] == '\t' ||
				VAR_SPACE[i][j] == '\0' ||
				VAR_SPACE[i][j] == '\n') {
				fprintf(fp," ");
				printf(" ");
			} else {
				fprintf(fp, "%c", VAR_SPACE[i][j]);
				printf("%c", VAR_SPACE[i][j]);
			}
		}
		fprintf(fp, "|\n");
		printf("|\n");
	}
	fprintf(fp, "'----------------'\n");
	printf("'----------------'\n");

	fclose(fp);
	return NO_ERROR;
}

void print_PROGRAM_ARRAY() {
	int i, j;
	printf(".--PROGRAM_ARRAY");
	for (i = 15; i < PROGRAM_LINELEN; i++) {
		printf("-");
	}
	printf(".\n");
	for (i = 0; i < PROGRAM_NUMLINES; i++) {
		printf("|");
		for (j = 0; j < PROGRAM_LINELEN; j++) {
			printf("%c", PROGRAM_ARRAY[i][j]);
		}
		printf("|\n");
	}
	printf("'");
	for (j = 0; j < PROGRAM_LINELEN; j++) {
		printf("-");
	}
	printf("'\n");
}