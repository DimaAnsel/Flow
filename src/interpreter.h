/////////////////////
// interpreter.h
// Noah Ansel
// 2015-11-21
// -----------------
// Function definitions for interpreting
// a loaded file.
/////////////////////

#pragma once

#include "main.h"


ErrCode tick();

// operators
ErrCode cmd_load(char expression[]);
ErrCode cmd_set(char expression[]);
ErrCode cmd_add(char expression[]);
ErrCode cmd_sub(char expression[]);
ErrCode cmd_mul(char expression[]);
ErrCode cmd_div(char expression[]);
ErrCode cmd_mod(char expression[]);
ErrCode cmd_comp(char expression[]);

// I/O
ErrCode cmd_out(char expression[]);
ErrCode cmd_in(char expression[]);

// direction modifiers
void rotate_ccw();
void rotate_cw();

// helper fcns
ErrCode evaluate(char expression[], char* ret);
ErrCode translateHex(char expression[], char* ret);
ErrCode getVariable(char expression[], char** ret);
