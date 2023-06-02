#ifndef __RAND_H__
#define __RAND_H__
#include "constants.h"

void initializeWithSeed(int seed);

// EFFECTS: randomly returns 0 or 1
int flipCoin();

enum RespChoice {
    REPEAT = 1,
    ADMIRE = 2,
    NONE = 0,
};

/*
 * Depending on repeat and admire constant, decides the response
 */
RespChoice randomResponse();

#endif /* __RAND_H__ */
