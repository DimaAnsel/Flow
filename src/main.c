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

void init_globals() {
	// initialize all variables to 0
	memset(VAR_SPACE, 0, sizeof(char)*VARSPACE_SIZE*VARSPACE_SIZE);
	
	// loaded variable initialized to first item of VAR_SPACE
	LOADED_VAR = &VAR_SPACE[0][0];
	
	// initialize other globals
	ERROR = INVALID_FILE;
	PROGRAM_FLOW = UP;
	PROGRAM_ARRAY = NULL;
	PROGRAM_NUMLINES = 0;
	PROGRAM_LINELEN = 0;
	CURRENT_LINE = 0;
	CURRENT_COLUMN = 0;
	PROGRAM_COMPLETE = 0;
}

void handle_error(ErrCode error) {
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


int main(int argc, char *argv[]) {
	int i;
	init_globals();

	// command line arguments
	for (int i = 1; i < argc; i++) {
		if ((strcmp(argv[i],"-h") == 0) || (strcmp(argv[i],"--help") == 0)) {
			printf("Usage: flow [options] [file]\n");
			printf("Options:\n");
			printf("\t-h\t--help\tDisplay this help menu.\n");
			printf("\t-d\t--debug\tPrint loaded program file and variable space.\n");
			printf("\t-vd\t--debug-verbose\tSame as --debug, but prints variable space in hex.\n");
			return 1;
		} else if ((strcmp(argv[i],"-d") == 0) || (strcmp(argv[i],"--debug") == 0)) {
			DEBUG_MODE = 1;
		} else if ((strcmp(argv[i], "-vd") == 0) || (strcmp(argv[i], "--debug-verbose") == 0)) {
			DEBUG_MODE = 2;
		} else if (ERROR == INVALID_FILE) {
			// haven't loaded file yet
			ERROR = load_file(argv[i]);
			if (ERROR != NO_ERROR) {
				handle_error(ERROR);
				return 0;
			}
		} else {
			printf("Unrecognized argument: %s\n", argv[i]);
			return 0;
		}
	}

	// if input file not provided, get it here
	if (ERROR == INVALID_FILE) {
		char filename[512];
		printf("[Flow] Enter the file to be executed: ");
		filename[0] = getchar();
		i = 0;
		while (filename[i] != '\n') {
			i++;
			filename[i] = getchar();
		}
		filename[i] = '\0';

		ERROR = load_file(filename);
		if (ERROR != NO_ERROR) {
			handle_error(ERROR);
			return 0;
		}
	}

	// go with the flow!
	printf("[Flow] Beginning execution . . .\n");
	while (PROGRAM_COMPLETE == 0) {
		ERROR = tick();
		if (ERROR != NO_ERROR) {
			handle_error(ERROR);
			break;
		}
	}
	if (ERROR == NO_ERROR) {
		printf("[Flow] Program exited successfully.\n");
	}
	if (DEBUG_MODE > 0) {
		dump_VAR_SPACE(DEBUG_MODE - 1);
	}
	printf("\n[Flow] Press Enter to close this window . . . ");
	getchar();

	return 0;
}