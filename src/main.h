/////////////////////
// main.h
// Dima Ansel
// 2015-11-19
// -----------------
// Common include for all files.
// Anything used in multiple places
// can go here.
/////////////////////

#ifndef _CRT_SECURE_NO_WARNINGS // make Visual Studio shut up about using C functions
#define _CRT_SECURE_NO_WARNINGS
#endif // _CRT_SECURE_NO_WARNINGS
#ifndef _CRT_NONSTDC_NO_WARNINGS
#define _CRT_NONSTDC_NO_WARNINGS
#endif // _CRT_NONSTDC_NO_WARNINGS

#pragma once

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define CMD_START	'#' // start & end of program
#define CMD_IGNORE	' ' // spaces are ignored

#define CMD_LOAD	'@' // sets LOADED_VAR pointer
#define CMD_NEXT	'\'' // loads a variable forward in memory
#define CMD_PREV	',' // loads a variable backwards in memory
#define CMD_CACHE	';' // caches LOADED_VAR offset to this
#define CMD_SET		':' // sets loaded var to this
#define CMD_COPY	')' // copies LOADED_VAR to this var
#define CMD_ADD		'+' // adds this to loaded var
#define CMD_SUB		'-' // subtracts this from loaded var
#define CMD_MUL		'*' // multiplies this and loaded var
#define CMD_DIV		'/' // divides loaded var by this
#define CMD_MOD		'%' // modulos loaded var by this
#define CMD_COMP	'?' // compares this to loaded var (unsigned)
#define CMD_SCOMP	'!' // compares this to loaded var (signed)
#define CMD_OUT		'"' // prints out ASCII of loaded var
#define CMD_IN		'~' // gets single char input in loaded var; if succeeds, sets this to FF, else 00

#define CMD_UP		'^' // turns program flow up
#define CMD_DOWN	'v' // turns program flow down
#define CMD_LEFT	'<' // turns program flow left
#define CMD_RIGHT	'>' // turns program flow right

#define VARSPACE_SIZE	16	// number of unique characters
#define VARSPACE_START	'g' // start character for variable space
#define VARSPACE_END	VARSPACE_START + (char)VARSPACE_SIZE - (char)1 // end character for variable space

#define OP_LENGTH 3
#define OPS_PER_SECTOR 8

#define DEBUG_FILENAME "debug.txt"

typedef enum FlowDir_enum {
	UP,
	LEFT,
	RIGHT,
	DOWN
} FlowDir;

typedef enum ErrCode_enum {
	NO_ERROR,

	// parsing errors
	INVALID_FILE,
	NO_START_CMD,
	MULTIPLE_START_CMDS,
	NO_START_DIRECTION,

	// runtime errors
	LEAK_ERROR,
	INVALID_EXPRESSION,
	INVALID_VARIABLENAME,
	INVALID_OPERATOR,
	BOUNDS_VIOLATION,

	// debug errors
	INVALID_DEBUG_FILE
} ErrCode;


// Global variables

char** PROGRAM_ARRAY;
int PROGRAM_LINELEN;
int PROGRAM_NUMLINES;
int CURRENT_LINE;
int CURRENT_COLUMN;
FlowDir PROGRAM_FLOW;
char PROGRAM_COMPLETE;
char DEBUG_MODE;

char VAR_SPACE[VARSPACE_SIZE][VARSPACE_SIZE]; // variable space
char* LOADED_VAR;

ErrCode ERROR;

// function signatures

void init_globals();
void handle_error(ErrCode error);