# Flow Language Documentation

## Contents
* Overview
* Variables
* Program Flow
* Operators and Syntax

## Overview

Flow is a very simple language designed from the concept of the non-linear nature of programming. Whereas other languages use for loops or if statements to denote branches in code, loops in Flow look like loops, and if-else blocks look like branches.

To achieve this, the interpreter tracks programs' current location and direction, beginning from a starting pointer. Commands can alter direction of the program, and the compare operator allows for branches.

## Variables

Flow has a finite number of variables, all of the character type, identified by two-character names consisting of the lowercase characters _g_ through _v_. The interpreter stores these characters as a 2D array. Variables are modified by "loading" a variable, which causes the interpreter to point to a specific variable, and then performing an operation.

## Program Flow

Every Flow program must begin and end on the program terminate operator. The terminate operator also specifies the program's initial direction. The interpreter follows this path, executing any commands it crosses, until it reaches a flow-altering operator. If the program flows outside of the file.

## Operators and Syntax

Each operation in a Flow program has three characters. The first is the operator, followed by a two-character hexadecimal value or variable name. The exceptions to this are the terminate operator, which is followed by a direction operator instead of a variable, and the direction operators, which are followed by spaces instead of values or variables. Arithmetic and comparison operations are performed in-place on the currently loaded variable. The complete list of operators is as follows:

| operator | name | description |
| :------- |:----:| :---------- |
| # | terminate | Marks the start and end of a program. Only one terminate operator is allowed per program. |
| < | left | Sets the flow direction to left. |
| > | right | Sets the flow direction to right. |
| v | down | Sets the flow direction to down. |
| ^ | up | Sets the flow direction to up. |
| @ | load | Loads a variable by pointing the interpreter to that variable. |
| : | set | Sets the loaded variable to the value of this expression. |
| + | add | Adds the value of this operation to the currently loaded variable. |
| - | subtract | Subtracts the value of this expression from the currently loaded variable. |
| * | multiply | Multiplies the loaded variable by this expression.
| / | divide | Divides the loaded variable by this expression.
| % | modulo | Modulos the loaded variable by this expression.
| ? | compare | Compares the loaded variable to this expression. If the loaded variable is less than this expression, the flow direction turns counter-clockwise. If the loaded variable is equal to this expression, the flow direction is unchanged. If greater than this expression, the flow direction turns clockwise. |
