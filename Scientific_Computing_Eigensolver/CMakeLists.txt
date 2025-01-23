cmake_minimum_required(VERSION 3.22)
project(pcsc_project)

# Set C++ standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add Eigen submodule
add_subdirectory(external/eigen)
include_directories(external/eigen)

# Add the executable target for the main application
add_executable(pcsc_project
        src/main.cpp
        src/solver.hpp
        src/solver_imp.hpp
        src/input.hpp
        src/input.cpp
        src/output.hpp
        src/output_imp.hpp
)

# Include GoogleTest as a submodule
add_subdirectory(googletest)

# Add a new executable target for testing
add_executable(pcsc_project_tests
        test/test.cpp
        src/solver.hpp
        src/solver_imp.hpp
        src/input.hpp
        src/input.cpp
        src/output.hpp
        src/output_imp.hpp
)

# Link the test target with GoogleTest and pthread
target_link_libraries(pcsc_project_tests PRIVATE gtest gtest_main pthread)

# Enable testing and add the test executable as a test case
enable_testing()
add_test(NAME pcsc_tests COMMAND pcsc_project_tests)
