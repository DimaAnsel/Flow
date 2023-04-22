/////////////////////
// interpreter.h
// Dima Ansel
// 2015-11-21
// -----------------
// Function definitions for interpreting
// a loaded file.
/////////////////////

#pragma once

#include "main.h"


ErrCode tick();

// pointer magic
ErrCode cmd_load(char expression[]);
ErrCode cmd_next(char expression[]);
ErrCode cmd_prev(char expression[]);
ErrCode cmd_cache(char expression[]);

// arithmetic operators
ErrCode cmd_set(char expression[]);
ErrCode cmd_copy(char expression[]);
ErrCode cmd_add(char expression[]);
ErrCode cmd_subtract(char expression[]);
ErrCode cmd_multiply(char expression[]);
ErrCode cmd_divide(char expression[]);
ErrCode cmd_modulus(char expression[]);
ErrCode cmd_compare(char expression[]);
ErrCode cmd_compare_signed(char expression[]);

// I/O
ErrCode cmd_out(char expression[]);
ErrCode cmd_in(char expression[]);

// direction modifiers
void rotate_ccw();
void rotate_cw();

// helper functions
ErrCode evaluate(char expression[], char* ret);
ErrCode translate_hex(char expression[], char* ret);
ErrCode get_variable(char expression[], char** ret);
ErrCode move_variable(char expression[], char** ret, char decrement);
