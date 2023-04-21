/////////////////////
// main.c
// Noah Ansel
// 2015-11-19
// -----------------
// Program shell.
/////////////////////

#include "main.h"
#include "loader.h"
#include "interpreter.h"
#include "debug.h"

void initGlobals() {
	// initialize all variables to 0
	memset(VAR_SPACE, 0, sizeof(char)*VARSPACE_SIZE*VARSPACE_SIZE);
	
	// loaded variable initialized to first item of VAR_SPACE
	LOADED_VAR = &VAR_SPACE[0][0];
	
	// initialize other globals
	PROGRAM_FLOW = UP;
	PROGRAM_ARRAY = NULL;
	PROGRAM_NUMLINES = 0;
	PROGRAM_LINELEN = 0;
	CURRENT_LINE = 0;
	CURRENT_COLUMN = 0;
	PROGRAM_COMPLETE = 0;
}

void handleError(ErrCode error) {
	switch (error) {
	case NO_ERROR: {
		break;
	}
	// parsing errors
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
	case NO_START_DIRECTION: {
		printf("PARSING ERROR: No start direction specified.\n");
		break;
	}
	// runtime errors
	case LEAK_ERROR: {
		printf("RUNTIME ERROR: Program flow left file at line %d column %d.\n", CURRENT_LINE, CURRENT_COLUMN);
		break;
	}
	case INVALID_EXPRESSION: {
		printf("RUNTIME ERROR: Invalid expression at line %d column %d.\n", CURRENT_LINE, CURRENT_COLUMN);
		break;
	}
	case INVALID_VARIABLENAME: {
		printf("RUNTIME ERROR: Invalid variable name at line %d column %d.\n", CURRENT_LINE, CURRENT_COLUMN);
		break;
	}
	case INVALID_OPERATOR: {
		printf("RUNTIME ERROR: Invalid operator at line %d column %d.\n", CURRENT_LINE, CURRENT_COLUMN);
		break;
	}
	case BOUNDS_VIOLATION: {
		printf("RUNTIME ERROR: Attempted to access invalid memory location at line %d column %d. Current location: %p. Bounds: %p ~ %p.\n", CURRENT_LINE, CURRENT_COLUMN, LOADED_VAR, VAR_SPACE, &VAR_SPACE[VARSPACE_SIZE-1][VARSPACE_SIZE-1]);
		break;
	}
	// miscellaneous errors
	case INVALID_DEBUG_FILE: {
		printf("DEBUG ERROR: Could not open debug file.\n");
		break;
	}
	default: {
		printf("ERROR: Unspecified error %d\n", error);
		break;
	}
	}
}


int main(void) {
	int i = 0;
	char filename[512];
	initGlobals();

	printf("[Flow] Enter the file to be executed: ");
	filename[0] = getchar();
	while (filename[i] != '\n') {
		i++;
		filename[i] = getchar();
	}
	filename[i] = '\0';

	ERROR = loadFile(filename);
	if (ERROR != NO_ERROR) {
		handleError(ERROR);
		return 0;
	} else {
		printf("[Flow] Beginning execution . . .\n");
	}

	while (PROGRAM_COMPLETE == 0) {
		ERROR = tick();
		if (ERROR != NO_ERROR) {
			handleError(ERROR);
			break;
		}
	}
	if (ERROR == NO_ERROR) {
		printf("[Flow] Program exited successfully.\n");
	}
	dump_VAR_SPACE(0);
	printf("\n[Flow] Press Enter to close this window . . . ");
	getchar();

	return 0;
}