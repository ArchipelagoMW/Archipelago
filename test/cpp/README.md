# C++ tests

Test framework for C and C++ code in AP.

## Adding a Test

### GoogleTest

Adding GoogleTests is as simple as creating a directory with
* one or more `test_*.cpp` files that define tests using
  [GoogleTest API](https://google.github.io/googletest/)
* a `CMakeLists.txt` that adds the .cpp files to `test_default` target using
  [target_sources](https://cmake.org/cmake/help/latest/command/target_sources.html)

### CTest

If either GoogleTest is not suitable for the test or the build flags / sources / libraries are incompatible,
you can add another CTest to the project using add_target and add_test, similar to how it's done for `test_default`.

## Running Tests

* Install [CMake](https://cmake.org/).
* Build and/or install GoogleTest and make sure
  [CMake can find it](https://cmake.org/cmake/help/latest/module/FindGTest.html), or
  [create a parent `CMakeLists.txt` that fetches GoogleTest](https://google.github.io/googletest/quickstart-cmake.html).
* Enter the directory with the top-most `CMakeLists.txt` and run
  ```sh
  mkdir build
  cmake -S . -B build/ -DCMAKE_BUILD_TYPE=Release
  cmake --build build/ --config Release && \
  ctest --test-dir build/ -C Release --output-on-failure
  ```
