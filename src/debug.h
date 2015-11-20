/////////////////////
// debug.h
// Noah Ansel
// 2015-11-19
// -----------------
// Helpful functions for debugging programs
// or the interpreter.
/////////////////////

#pragma once

ErrCode dumpVarSpace() {
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
