/////////////////////
// debug.c
// Dima Ansel
// 2023-04-22
// -----------------
// Helpful functions for debugging programs
// or the interpreter.
/////////////////////

#include "debug.h"

ErrCode dump_VAR_SPACE(char hex) {
    FILE* fp = fopen(DEBUG_FILENAME, "a");
    if (fp == NULL) {
        return INVALID_DEBUG_FILE;
    }

    fprintf(fp, " .VAR_SPACE dump--");
    printf(" .VAR_SPACE dump--");
    if (hex) {
        fprintf(fp, "----------------");
        printf("----------------");
    }
    fprintf(fp, ".\n");
    printf(".\n");

    for (int i = 0; i < VARSPACE_SIZE; i++) {
        // row label
        fprintf(fp,"%c|", VARSPACE_START + (char)i);
        printf("%c|", VARSPACE_START + (char)i);

        // data
        for (int j = 0; j < VARSPACE_SIZE; j++) {
            if (hex) {
                if (VAR_SPACE[i][j] == '\0') {
                    fprintf(fp,"  ");
                    printf("  ");
                } else {
                    fprintf(fp, "%2x", VAR_SPACE[i][j]);
                    printf("%2x", VAR_SPACE[i][j]);
                }
            } else {
                if (VAR_SPACE[i][j] == '\t' ||
                    VAR_SPACE[i][j] == '\0' ||
                    VAR_SPACE[i][j] == '\n') {
                    fprintf(fp," ");
                    printf(" ");
                } else {
                    fprintf(fp, "%c", VAR_SPACE[i][j]);
                    printf("%c", VAR_SPACE[i][j]);
                }
            }
        }
        fprintf(fp, "|\n");
        printf("|\n");
    }

    fprintf(fp, " '----------------");
    printf(" '----------------");
    if (hex) {
        fprintf(fp, "----------------");
        printf("----------------");
    }
    fprintf(fp, "'\n");
    printf("'\n");

    fprintf(fp, ".VAR_SPACE RANGE %p ~ %p\n", *VAR_SPACE, &VAR_SPACE[VARSPACE_SIZE-1][VARSPACE_SIZE-1]);
    printf(".VAR_SPACE RANGE %p ~ %p\n", *VAR_SPACE, &VAR_SPACE[VARSPACE_SIZE-1][VARSPACE_SIZE-1]);
    fprintf(fp, ".LOADED_VAR      %p\n", LOADED_VAR);
    printf(".LOADED_VAR      %p\n", LOADED_VAR);

    fclose(fp);
    return NO_ERROR;
}

void print_PROGRAM_ARRAY() {
    int i, j;
    printf("   .--PROGRAM_ARRAY");
    for (i = 15; i < PROGRAM_LINELEN; i++) {
        printf("-");
    }
    printf(".\n");
    for (i = 0; i < PROGRAM_NUMLINES; i++) {
        printf("%3d|",i);
        for (j = 0; j < PROGRAM_LINELEN; j++) {
            printf("%c", PROGRAM_ARRAY[i][j]);
        }
        printf("|\n");
    }
    printf("   '");
    for (j = 0; j < PROGRAM_LINELEN; j++) {
        printf("-");
    }
    printf("'\n");
}