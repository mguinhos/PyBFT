
#include <stdio.h>

#define S 1024

char T[S] = { 0 };
size_t P = 0;

// write a char in stdout
static inline
void O()
{
    putchar(T[P % S] & 0xFF);
}

// get a char from stdin
static inline
void I()
{
    T[P % S] = getchar() & 0xFF;
}

// refresh the stdout
static inline
void F()
{
    fflush(stdout);
}

// refresh the tape values
static inline
void U()
{
    P %= S;
    T[P] &= 0xFF;
    
}