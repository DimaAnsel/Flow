/////////////////////
// main.h
// Noah Ansel
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

#define CMD_LOAD	'@' // sets LOADED_VAR pointer
#define CMD_SET		':' // sets loaded var to this
#define CMD_ADD		'+' // adds this to loaded var
#define CMD_SUB		'-' // subtracts this from loaded var
#define CMD_MUL		'*' // multiplies this and loaded var
#define CMD_DIV		'/' // divides loaded var by this
#define CMD_MOD		'%' // modulos loaded var by this
#define CMD_COMP	'?' // compares this to loaded var
#define CMD_OUT		'"' // prints out ASCII of loaded var
#define CMD_IN		'~' // gets single char input in loaded var; if succeeds, sets this to FF, else 00

#define CMD_UP		'^' // turns program flow up
#define CMD_DOWN	'v' // turns program flow down
#define CMD_LEFT	'<' // turns program flow left
#define CMD_RIGHT	'>' // turns program flow right

#define VARSPACE_SIZE	16	// number of unique characters

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
	MISSING_FILE,
	NO_START_CMD,
	MULTIPLE_START_PATHS,

	// runtime errors
	LEAK_ERROR,
	SYNTAX_ERROR,

	// debug errors
	INVALID_DEBUG_FILE
} ErrCode;

// Structs

typedef struct FileLine_struct FileLine;
typedef struct FileLine_struct* pFileLine;
struct FileLine_struct {
	int num_cols; // number of 3-character strings in this line
	char** strings; // array of 3-character strings
	pFileLine prev_line; // pointer to the previous line
	pFileLine next_line; // pointer to the next line
};



// Global variables

pFileLine PROGRAM_ORIGIN;
int PROGRAM_NUMLINES;

char VAR_SPACE[VARSPACE_SIZE][VARSPACE_SIZE];
char* LOADED_VAR;
char** PROGRAM_PTR;
FlowDir PROGRAM_FLOW;

// function signatures

void initGlobals();