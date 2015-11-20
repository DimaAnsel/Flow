/////////////////////
// main.c
// Noah Ansel
// 2015-11-19
// -----------------
// Program shell.
/////////////////////

#include "main.h"
#include "loader.h"
#include "debug.h"

void initGlobals() {
	// initialize all variables to 0
	memset(VAR_SPACE, 0, sizeof(char)*VARSPACE_SIZE*VARSPACE_SIZE);
	
	// loaded variable initialized to first item of VAR_SPACE
	LOADED_VAR = &VAR_SPACE[0][0];
	
	// initialize other globals
	PROGRAM_FLOW = UP;
	PROGRAM_ORIGIN = NULL;
	PROGRAM_PTR = NULL;
	PROGRAM_NUMLINES = 0;
}


int main(void) {
	initGlobals();

	loadFile("echo.fl");

	return 0;
}