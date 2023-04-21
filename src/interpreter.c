/////////////////////
// interpreter.c
// Dima Ansel
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
		// end of program
		case CMD_START: {
			PROGRAM_COMPLETE = 1;
			return NO_ERROR;
		}
		// pointer magic
		case CMD_LOAD: {
			return cmd_load(expression);
		}
		case CMD_NEXT: {
			return cmd_next(expression);
		}
		case CMD_PREV: {
			return cmd_prev(expression);
		}
		case CMD_CACHE: {
			return cmd_cache(expression);
		}
		// arithmetic
		case CMD_SET: {
			return cmd_set(expression);
		}
		case CMD_ADD: {
			return cmd_add(expression);
		}
		case CMD_SUB: {
			return cmd_subtract(expression);
		}
		case CMD_MUL: {
			return cmd_multiply(expression);
		}
		case CMD_DIV: {
			return cmd_divide(expression);
		}
		case CMD_MOD: {
			return cmd_modulus(expression);
		}
		// logic
		case CMD_COMP: {
			return cmd_compare(expression);
		}
		case CMD_SCOMP: {
			return cmd_compare_signed(expression);
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

//////////////
// cmd_load
//	Sets the loaded variable to the value
//	of the expression.
ErrCode cmd_load(char expression[]) {
	ErrCode error;
	char* var = NULL;
	error = get_variable(expression, &var);
	if (error == NO_ERROR) {
		LOADED_VAR = var;
	}
	return error;
}

//////////////
// cmd_next
//	Moves the loaded variable forward
//	by the value of the expression.
ErrCode cmd_next(char expression[]) {
	ErrCode error;
	char* var = NULL;
	error = move_variable(expression, &var, 0);
	if (error == NO_ERROR) {
		LOADED_VAR = var;
	}
	return error;
}

//////////////
// cmd_prev
//	Moves the loaded variable backward
//	by the value of the expression.
ErrCode cmd_prev(char expression[]) {
	ErrCode error;
	char* var = NULL;
	error = move_variable(expression, &var, 1);
	if (error == NO_ERROR) {
		LOADED_VAR = var;
	}
	return error;
}

//////////////
// cmd_prev
//	Sets the target variable to the absolute
//	offset between itself and the loaded variable.
ErrCode cmd_cache(char expression[]) {
	ErrCode error;
	char* var = NULL;
	error = get_variable(expression, &var);
	if (error == NO_ERROR) {
		if (var > LOADED_VAR) {
			(*var) = (char)(((long)((long)var - (long)LOADED_VAR))%0x100);
		} else {
			(*var) = (char)(((long)((long)LOADED_VAR - (long)var))%0x100);
		}
	}
	return error;
}

//////////////
// cmd_next
//	Sets the loaded variable to the value
//	of the expression.
ErrCode cmd_set(char expression[]) {
	ErrCode error;
	char temp;
	error = evaluate(expression, &temp);
	if (error == NO_ERROR) {
		(*LOADED_VAR) = temp;
	}
	return error;
}

//////////////
// cmd_add
//	Adds the value of the expression
//	to the loaded variable.
ErrCode cmd_add(char expression[]) {
	ErrCode error;
	char temp;
	error = evaluate(expression, &temp);
	if (error == NO_ERROR) {
		(*LOADED_VAR) += temp;
	}
	return error;
}

//////////////
// cmd_subtract
//	Subtracts the value of the expression
//	from the loaded variable.
ErrCode cmd_subtract(char expression[]) {
	ErrCode error;
	char temp;
	error = evaluate(expression, &temp);
	if (error == NO_ERROR) {
		(*LOADED_VAR) -= temp;
	}
	return error;
}

//////////////
// cmd_multiply
//	Multiplies the loaded variable
//	by the value of the expression.
ErrCode cmd_multiply(char expression[]) {
	ErrCode error;
	char temp;
	error = evaluate(expression, &temp);
	if (error == NO_ERROR) {
		(*LOADED_VAR) = (*LOADED_VAR) * temp;
	}
	return error;
}

//////////////
// cmd_multiply
//	Divides the loaded variable
//	by the value of the expression.
ErrCode cmd_divide(char expression[]) {
	ErrCode error;
	char temp;
	error = evaluate(expression, &temp);
	if (error == NO_ERROR) {
		(*LOADED_VAR) = (*LOADED_VAR) / temp;
	}
	return error;
}

//////////////
// cmd_multiply
//	Mods the loaded variable
//	by the value of the expression.
ErrCode cmd_modulus(char expression[]) {
	ErrCode error;
	char temp;
	error = evaluate(expression, &temp);
	if (error == NO_ERROR) {
		(*LOADED_VAR) = (*LOADED_VAR) % temp;
	}
	return error;
}

//////////////
// cmd_compare
//	Rotates flow direction depending on comparison
//	between loaded variable and expression (unsigned).
ErrCode cmd_compare(char expression[]) {
	ErrCode error;
	unsigned char temp, curr;
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
// cmd_compare
//	Rotates flow direction depending on comparison
//	between loaded variable and expression (signed).
ErrCode cmd_compare_signed(char expression[]) {
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
	error = get_variable(expression, &var);
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
	error = get_variable(expression, &ptr);
	if (error == NO_ERROR) {
		(*ret) = *ptr;
	} else {
		error = translate_hex(expression, ret);
	}
	
	return error;
}

////////////////
// translate_hex
//	Translates an expression from hex if valid,
//	putting return value in ret.
//	Otherwise, raises INVALID_EXPRESSION error.
ErrCode translate_hex(char expression[], char* ret) {
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
// get_variable
//	Returns the address of a variable, if expression is a valid variable.
//	Otherwise, raises INVALID_VARIABLENAME error.
ErrCode get_variable(char expression[], char** ret) {
	if (expression[0] == '@' && expression[1] == ' ') {
		(*ret) = LOADED_VAR;
		return NO_ERROR;
	}
	if (expression[0] < VARSPACE_START ||
		expression[0] > VARSPACE_END ||
		expression[1] < VARSPACE_START ||
		expression[1] > VARSPACE_END) {
		return INVALID_VARIABLENAME;
	}

	int i = (int)(expression[0] - VARSPACE_START);
	int j = (int)(expression[1] - VARSPACE_START);

	(*ret) = &(VAR_SPACE[i][j]);
	
	return NO_ERROR;
}

////////////////
// move_variable
//	Returns the new location of the variable pointer,
//	if expression evaluates to a valid pointer within variable space.
//	Otherwise, raises BOUNDS_VIOLATION error.
ErrCode move_variable(char expression[], char** ret, char decrement) {
	unsigned char temp;
	ErrCode error;
	error = evaluate(expression, &temp);
	if (error == NO_ERROR) {
		char* dest = LOADED_VAR + (decrement ? -temp : temp);
		if ((dest < &VAR_SPACE[0][0]) ||
			(dest > &VAR_SPACE[VARSPACE_SIZE-1][VARSPACE_SIZE-1])) {
			return BOUNDS_VIOLATION;
		}
		(*ret) = dest;
		return NO_ERROR;
	}
	return error;
}
