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
	int start_cmds = 0; // bool to prevent using multiple # operators
	int lineLen = 0; // tracks when it should cut off for next
	int maxLineLen = 0;
	int numLines = 1;
	int i, j;
	char temp;

	// Make sure file is valid
	FILE* fp = fopen(filename, "r");
	if (fp == NULL) {
		return INVALID_FILE;
	}

	// First, get size of file
	temp = fgetc(fp);
	lineLen++;

	while (temp != EOF) {
		if (temp == '\n') {
			if (lineLen > maxLineLen) { // see if this line is bigger than others encountered
				maxLineLen = lineLen;
			}
			lineLen = 0;
			numLines++;
		} else if (temp == CMD_START) {
			CURRENT_LINE = numLines - 1;
			CURRENT_COLUMN = lineLen;
			start_cmds++;
		}

		temp = fgetc(fp);
		lineLen++;
	}
	if (lineLen > maxLineLen) { // check length of last line
		maxLineLen = lineLen;
	}

	fclose(fp);
	
	// Error checking
	if (start_cmds == 0) {
		return NO_START_CMD;
	} else if (start_cmds > 1) {
		return MULTIPLE_START_CMDS;
	}
	if (numLines == 0) {
		return INVALID_FILE;
	}
	if (maxLineLen == 1) {
		return INVALID_FILE;
	}
	
	// Set sizes of global array
	if (maxLineLen % 3 == 0) {
		PROGRAM_LINELEN = maxLineLen;
	} else {
		PROGRAM_LINELEN = maxLineLen + 3 - (maxLineLen % 3); // round up to nearest 3
	}
	PROGRAM_NUMLINES = numLines;

	// Create 2D array of sufficient size
	PROGRAM_ARRAY = malloc(sizeof(char*)*PROGRAM_NUMLINES);
	for (i = 0; i < PROGRAM_NUMLINES; i++) {
		PROGRAM_ARRAY[i] = malloc(sizeof(char)*PROGRAM_LINELEN);
		for (j = 0; j < PROGRAM_LINELEN; j++) {
			PROGRAM_ARRAY[i][j] = ' ';
		}
	}

	// Read in file
	fp = fopen(filename, "r");
	i = 0;
	j = 0;

	temp = fgetc(fp);

	while (temp != EOF) {
		if (temp == '\n') { // next line
			j = 0;
			i++;
		} else { // normal character
			PROGRAM_ARRAY[i][j] = temp;
			j++;
		}
		temp = fgetc(fp);
	}

	fclose(fp);

	return NO_ERROR;
}