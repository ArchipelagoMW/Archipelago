/* A specialized unordered_set implementation for literals, where bucket_count
 * is defined at initialization rather than increased automatically.
 */
#include <stddef.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#ifndef INTSET_NAME
#error "Please #define INTSET_NAME ... before including intset.h"
#endif

#ifndef INTSET_TYPE
#error "Please #define INTSET_TYPE ... before including intset.h"
#endif

/* macros to generate unique names from INTSET_NAME */
#ifndef INTSET_CONCAT
#define INTSET_CONCAT_(a, b) a ## b
#define INTSET_CONCAT(a, b) INTSET_CONCAT_(a, b)
#define INTSET_FUNC_(a, b) INTSET_CONCAT(a, _ ## b)
#endif

#define INTSET_FUNC(name) INTSET_FUNC_(INTSET_NAME, name)
#define INTSET_BUCKET INTSET_CONCAT(INTSET_NAME, Bucket)

typedef struct {
    size_t count;
    union {
        INTSET_TYPE val;
        INTSET_TYPE *data;
    };
} INTSET_BUCKET;

typedef struct {
    size_t bucket_count;
    INTSET_BUCKET buckets[];
} INTSET_NAME;

static INTSET_NAME *INTSET_FUNC(new)(size_t buckets)
{
    if (buckets < 1)
        buckets = 1;
    size_t size = sizeof(INTSET_NAME) + buckets * sizeof(INTSET_BUCKET);
    INTSET_NAME *set = (INTSET_NAME*)malloc(size);
    if (!set)
        return NULL;
    memset(set, 0, size);
    set->bucket_count = buckets;
    return set;
}

static void INTSET_FUNC(free)(INTSET_NAME *set)
{
    size_t i;
    for (i = 0; i < set->bucket_count; i++) {
        if (set->buckets[i].count > 1)
            free(set->buckets[i].data);
    }
    free(set);
}

static bool INTSET_FUNC(contains)(INTSET_NAME *set, INTSET_TYPE val)
{
    size_t i;
    INTSET_BUCKET* bucket = set->buckets + ((size_t)val % set->bucket_count);
    if (bucket->count == 1)
        return bucket->val == val;
    for (i = 0; i < bucket->count; ++i) {
        if (bucket->data[i] == val)
            return true;
    }
    return false;
}

static bool INTSET_FUNC(add)(INTSET_NAME *set, INTSET_TYPE val)
{
    INTSET_BUCKET* bucket;

    if (INTSET_FUNC(contains)(set, val))
        return true; /* ok */

    bucket = set->buckets + ((size_t)val % set->bucket_count);
    if (bucket->count == 0) {
        bucket->val = val;
        bucket->count = 1;
    } else if (bucket->count == 1) {
        INTSET_TYPE old = bucket->val;
        bucket->data = (INTSET_TYPE*)malloc(2 * sizeof(INTSET_TYPE));
        if (!bucket->data) {
            bucket->val = old;
            return false; /* error */
        }
        bucket->data[0] = old;
        bucket->data[1] = val;
        bucket->count = 2;
    } else {
        size_t new_bucket_size;
        INTSET_TYPE* new_bucket_data;

        new_bucket_size = (bucket->count + 1) * sizeof(INTSET_TYPE);
        new_bucket_data = (INTSET_TYPE*)realloc(bucket->data, new_bucket_size);
        if (!new_bucket_data)
            return false; /* error */
        bucket->data = new_bucket_data;
        bucket->data[bucket->count++] = val;
    }
    return true; /* success */
}

#undef INTSET_FUNC
#undef INTSET_BUCKET
