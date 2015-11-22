/////////////////////
// interpreter.c
// Noah Ansel
// 2015-11-21
// -----------------
// Functions for interpreting
// a loaded file.
/////////////////////

#include "main.h"
#include "interpreter.h"

ErrCode tick() {
	// move
	switch (PROGRAM_FLOW) {
	case UP: {
		CURRENT_LINE--;
		break;
	}
	case DOWN: {
		CURRENT_LINE++;
		break;
	}
	case LEFT: {
		CURRENT_COLUMN -= 3;
		break;
	}
	case RIGHT: {
		CURRENT_COLUMN += 3;
		break;
	}
	}

	if (CURRENT_LINE < 0 ||
		CURRENT_LINE >= PROGRAM_NUMLINES ||
		CURRENT_COLUMN < 0 ||
		CURRENT_COLUMN >= PROGRAM_LINELEN) {
		return LEAK_ERROR; // program flowed out of file
	}

	char* expression = &(PROGRAM_ARRAY[CURRENT_LINE][CURRENT_COLUMN + 1]);
	// then execute
	switch (PROGRAM_ARRAY[CURRENT_LINE][CURRENT_COLUMN]) {
	case CMD_START: {
		PROGRAM_COMPLETE = 1;
		return NO_ERROR;
	}
	case CMD_LOAD: {
		return cmd_load(expression);
	}
	case CMD_SET: {
		return cmd_set(expression);
	}
	case CMD_ADD: {
		return cmd_add(expression);
	}
	case CMD_SUB: {
		return cmd_sub(expression);
	}
	case CMD_MUL: {
		return cmd_mul(expression);
	}
	case CMD_DIV: {
		return cmd_div(expression);
	}
	case CMD_MOD: {
		return cmd_mod(expression);
	}
	case CMD_COMP: {
		return cmd_comp(expression);
	}
	// I/O
	case CMD_IN: {
		return cmd_in(expression);
	}
	case CMD_OUT: {
		return cmd_out(expression);
	}
	// direction change
	case CMD_UP: {
		PROGRAM_FLOW = UP;
		return NO_ERROR;
	}
	case CMD_DOWN: {
		PROGRAM_FLOW = DOWN;
		return NO_ERROR;
	}
	case CMD_LEFT: {
		PROGRAM_FLOW = LEFT;
		return NO_ERROR;
	}
	case CMD_RIGHT: {
		PROGRAM_FLOW = RIGHT;
		return NO_ERROR;
	}
	case CMD_IGNORE: {
		return NO_ERROR;
	}
	default: {
		return INVALID_OPERATOR;
	}
	}
}

ErrCode cmd_load(char expression[]) {
	ErrCode error;
	char* var = NULL;
	error = getVariable(expression, &var);
	if (error == NO_ERROR) {
		LOADED_VAR = var;
	}
	return error;
}

ErrCode cmd_set(char expression[]) {
	ErrCode error;
	char temp;
	error = evaluate(expression, &temp);
	if (error == NO_ERROR) {
		(*LOADED_VAR) = temp;
	}
	return error;
}

ErrCode cmd_add(char expression[]) {
	ErrCode error;
	char temp;
	error = evaluate(expression, &temp);
	if (error == NO_ERROR) {
		(*LOADED_VAR) += temp;
	}
	return error;
}

ErrCode cmd_sub(char expression[]) {
	ErrCode error;
	char temp;
	error = evaluate(expression, &temp);
	if (error == NO_ERROR) {
		(*LOADED_VAR) -= temp;
	}
	return error;
}

ErrCode cmd_mul(char expression[]) {
	ErrCode error;
	char temp;
	error = evaluate(expression, &temp);
	if (error == NO_ERROR) {
		(*LOADED_VAR) = (*LOADED_VAR) * temp;
	}
	return error;
}

ErrCode cmd_div(char expression[]) {
	ErrCode error;
	char temp;
	error = evaluate(expression, &temp);
	if (error == NO_ERROR) {
		(*LOADED_VAR) = (*LOADED_VAR) / temp;
	}
	return error;
}

ErrCode cmd_mod(char expression[]) {
	ErrCode error;
	char temp;
	error = evaluate(expression, &temp);
	if (error == NO_ERROR) {
		(*LOADED_VAR) = (*LOADED_VAR) % temp;
	}
	return error;
}

//////////////
// cmd_comp
//	Rotates flow direction depending on comparison
//	between loaded variable and expression.
ErrCode cmd_comp(char expression[]) {
	ErrCode error;
	char temp, curr;
	error = evaluate(expression, &temp);
	if (error == NO_ERROR) {
		curr = (*LOADED_VAR);
		if (curr < temp) {
			rotate_ccw();
		} else if (curr > temp) {
			rotate_cw();
		}
	}
	return error;
}

//////////////
// cmd_in
//	Gets a character of input and places it
//	in the specified variable.
ErrCode cmd_in(char expression[]) {
	ErrCode error;
	char* var = NULL;
	error = getVariable(expression, &var);
	if (error == NO_ERROR) {
		(*var) = getchar();
	}

	return error;
}

/////////////
// cmd_out
//	Prints out ASCII representation of an expression.
ErrCode cmd_out(char expression[]) {
	ErrCode error;
	char temp;
	error = evaluate(expression, &temp);
	if (error == NO_ERROR) {
		printf("%c", temp);
	}
	
	return error;
}

/////////////
// rotate_ccw
//	Rotates flow direction counter-clockwise.
void rotate_ccw() {
	switch (PROGRAM_FLOW) {
	case UP: {
		PROGRAM_FLOW = LEFT;
		break;
	}
	case DOWN: {
		PROGRAM_FLOW = RIGHT;
		break;
	}
	case LEFT: {
		PROGRAM_FLOW = DOWN;
		break;
	}
	case RIGHT: {
		PROGRAM_FLOW = UP;
		break;
	}
	}
}

/////////////
// rotate_cw
//	Rotates flow direction counter-clockwise.
void rotate_cw() {
	switch (PROGRAM_FLOW) {
	case UP: {
		PROGRAM_FLOW = RIGHT;
		break;
	}
	case DOWN: {
		PROGRAM_FLOW = LEFT;
		break;
	}
	case LEFT: {
		PROGRAM_FLOW = UP;
		break;
	}
	case RIGHT: {
		PROGRAM_FLOW = DOWN;
		break;
	}
	}
}

////////////////
// evaluate
//	Evaluates an expression if that expression is valid,
//	putting return value in ret.
//	If invalid, raises INVALID_EXPRESSION error.
ErrCode evaluate(char expression[], char* ret) {
	ErrCode error;
	char* ptr = NULL;
	error = getVariable(expression, &ptr);
	if (error == NO_ERROR) {
		(*ret) = *ptr;
	} else {
		error = translateHex(expression, ret);
	}
	
	return error;
}

////////////////
// translateHex
//	Translates an expression from hex if valid,
//	putting return value in ret.
//	Otherwise, raises INVALID_EXPRESSION error.
ErrCode translateHex(char expression[], char* ret) {
	char a = 0;
	char b = 0;

	// first character of expression
	if (expression[0] >= '0' && expression[0] <= '9') {
		a = expression[0] - '0';
	} else if (expression[0] >= 'A' && expression[0] <= 'F') {
		a = 10 + (expression[0] - 'A');
	} else {
		return INVALID_EXPRESSION;
	}
	// second character of expression
	if (expression[1] >= '0' && expression[1] <= '9') {
		b = expression[1] - '0';
	} else if (expression[1] >= 'A' && expression[1] <= 'F') {
		b = 10 + (expression[1] - 'A');
	} else {
		return INVALID_EXPRESSION;
	}

	// combine the two
	(*ret) = (a << 4) + b;
	return NO_ERROR;
}

////////////////
// getVariable
//	Returns the address of a variable, if expression is a valid variable.
//	Otherwise, raises INVALID_VARIABLENAME error.
ErrCode getVariable(char expression[], char** ret) {
	if (expression[0] < 'g' ||
		expression[0] > 'v' ||
		expression[1] < 'g' ||
		expression[1] > 'v') {
		return INVALID_VARIABLENAME;
	}

	int i = (int)(expression[0] - 'g');
	int j = (int)(expression[1] - 'g');

	(*ret) = &(VAR_SPACE[i][j]);
	
	return NO_ERROR;
}