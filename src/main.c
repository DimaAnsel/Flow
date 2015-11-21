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
	PROGRAM_ARRAY = NULL;
	PROGRAM_PTR = NULL;
	PROGRAM_NUMLINES = 0;
	PROGRAM_LINELEN = 0;
	CURRENT_LINE = 0;
	CURRENT_COLUMN = 0;
}

void handleError(ErrCode error) {
	switch (error) {
	case NO_ERROR: {
		break;
	}
	case INVALID_FILE: {
		printf("PARSING ERROR: Invalid file.\n");
		break;
	}
	case NO_START_CMD: {
		printf("PARSING ERROR: No start command in file.\n");
		break;
	}
	case MULTIPLE_START_CMDS: {
		printf("PARSING ERROR: Multiple start commands in file.\n");
		break;
	}
	case LEAK_ERROR: {
		printf("RUNTIME ERROR: Program flow left file at line %d column %d.\n", CURRENT_LINE, CURRENT_COLUMN);
		break;
	}
	case SYNTAX_ERROR: {
		printf("SYNTAX ERROR: Syntax error at line %d column %d.\n", CURRENT_LINE, CURRENT_COLUMN);
		break;
	}
	case INVALID_DEBUG_FILE: {
		printf("DEBUG ERROR: Could not open debug file.\n");
		break;
	}
	}
}


int main(void) {
	initGlobals();

	ERROR = loadFile("echo.fl");
	handleError(ERROR);

	return 0;
}