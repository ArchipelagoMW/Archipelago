#include <limits>
#include <cstdint>
#include <gtest/gtest.h>

// uint32Set
#define INTSET_NAME uint32Set
#define INTSET_TYPE uint32_t
#include "../../../intset.h"
#undef INTSET_NAME
#undef INTSET_TYPE

// int64Set
#define INTSET_NAME int64Set
#define INTSET_TYPE int64_t
#include "../../../intset.h"


TEST(IntsetTest, ZeroBuckets)
{
    // trying to allocate with zero buckets has to either fail or be functioning
    uint32Set *set = uint32Set_new(0);
    if (!set)
        return; // failed -> OK

    EXPECT_FALSE(uint32Set_contains(set, 1));
    EXPECT_TRUE(uint32Set_add(set, 1));
    EXPECT_TRUE(uint32Set_contains(set, 1));
    uint32Set_free(set);
}

TEST(IntsetTest, Duplicate)
{
    // adding the same number again can't fail
    uint32Set *set = uint32Set_new(2);
    ASSERT_TRUE(set);
    EXPECT_TRUE(uint32Set_add(set, 0));
    EXPECT_TRUE(uint32Set_add(set, 0));
    EXPECT_TRUE(uint32Set_contains(set, 0));
    uint32Set_free(set);
}

TEST(IntsetTest, SetAllocFailure)
{
    // try to allocate 100TB of RAM, should fail and return NULL
    if (sizeof(size_t) < 8)
        GTEST_SKIP() << "Alloc error not testable on 32bit";
    int64Set *set = int64Set_new(6250000000000ULL);
    EXPECT_FALSE(set);
    int64Set_free(set);
}

TEST(IntsetTest, SetAllocOverflow)
{
    // try to overflow argument passed to malloc
    int64Set *set = int64Set_new(std::numeric_limits<size_t>::max());
    EXPECT_FALSE(set);
    int64Set_free(set);
}

TEST(IntsetTest, NullFree)
{
    // free(NULL) should not try to free buckets
    uint32Set_free(NULL);
    int64Set_free(NULL);
}

TEST(IntsetTest, BucketRealloc)
{
    // add a couple of values to the same bucket to test growing the bucket
    uint32Set* set = uint32Set_new(1);
    ASSERT_TRUE(set);
    EXPECT_FALSE(uint32Set_contains(set, 0));
    EXPECT_TRUE(uint32Set_add(set, 0));
    EXPECT_TRUE(uint32Set_contains(set, 0));
    for (uint32_t i = 1; i < 32; ++i) {
        EXPECT_TRUE(uint32Set_add(set, i));
        EXPECT_TRUE(uint32Set_contains(set, i - 1));
        EXPECT_TRUE(uint32Set_contains(set, i));
        EXPECT_FALSE(uint32Set_contains(set, i + 1));
    }
    uint32Set_free(set);
}

TEST(IntSet, Max)
{
    constexpr auto n = std::numeric_limits<uint32_t>::max();
    uint32Set *set = uint32Set_new(1);
    ASSERT_TRUE(set);
    EXPECT_FALSE(uint32Set_contains(set, n));
    EXPECT_TRUE(uint32Set_add(set, n));
    EXPECT_TRUE(uint32Set_contains(set, n));
    uint32Set_free(set);
}

TEST(InsetTest, Negative)
{
    constexpr auto n = std::numeric_limits<int64_t>::min();
    static_assert(n < 0, "n not negative");
    int64Set *set = int64Set_new(3);
    ASSERT_TRUE(set);
    EXPECT_FALSE(int64Set_contains(set, n));
    EXPECT_TRUE(int64Set_add(set, n));
    EXPECT_TRUE(int64Set_contains(set, n));
    int64Set_free(set);
}
