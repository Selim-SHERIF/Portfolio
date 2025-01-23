#include <gtest/gtest.h>
#include <fstream>
#include "../src/input.hpp"
#include "../src/solver.hpp"

/**
 * @file test_solver.cpp
 * @brief Unit tests for the `Input` and `Solver` classes using Google Test.
 *
 * This file contains tests to validate matrix parsers (`Input`) and solvers
 * (`Solver`) such as Power Method, Inverse Power Method, and QR decomposition.
 * It includes both real and complex matrix cases with edge case handling.
 */

// ============================== Helper Functions ==============================

/**
 * @brief Creates and writes content to a temporary file.
 *
 * @param fileName Name of the file to create.
 * @param content Content to write to the file.
 * @throws std::runtime_error If the file cannot be created.
 */
void WriteToTempFile(const std::string& fileName, const std::string& content) {
    std::ofstream file(fileName);
    if (!file) {
        throw std::runtime_error("Failed to create temporary file: " + fileName);
    }
    file << content;
    file.close();
}

/**
 * @brief Deletes a temporary file.
 *
 * @param fileName Name of the file to delete.
 */
void CleanUpTempFile(const std::string& fileName) {
    std::remove(fileName.c_str());
}

// ============================== Input Class Tests ==============================

/**
 * @class InputTest
 * @brief Google Test fixture for testing the `Input` class.
 *
 * Provides helper methods for reading test files and cleaning up temporary data.
 */
class InputTest : public ::testing::Test {
protected:
    Input input; ///< Instance of `Input` for testing.

    /**
     * @brief Helper function to read and parse a temporary test file.
     *
     * @param fileName Name of the file to read.
     * @param content Content to write to the file.
     */
    void ReadTestFile(const std::string& fileName, const std::string& content) {
        WriteToTempFile(fileName, content);
        input.ReadFile(fileName);
        CleanUpTempFile(fileName);
    }
};

/**
 * @test InputTest::ParsesValidRealMatrix
 * @brief Validates parsing a real matrix from input.
 */
TEST_F(InputTest, ParsesValidRealMatrix) {
    const std::string fileName = "valid_real_matrix.txt";
    const std::string content = R"(
        METHOD power
        TOLERANCE 1e-8
        MAX_ITER 500
        COMPLEX 0
        MATRIX_DATA
        3 3
        1 0 0
        0 2 0
        0 0 3
    )";

    ASSERT_NO_THROW(ReadTestFile(fileName, content));
    EXPECT_EQ(input.GetMethod(), "power");
    EXPECT_EQ(input.GetTolerance(), 1e-8);
    EXPECT_EQ(input.GetMaxIter(), 500);
    EXPECT_FALSE(input.GetIsComplex());

    Eigen::MatrixXd matrix = input.GetRealMatrix();
    ASSERT_EQ(matrix.rows(), 3);
    ASSERT_EQ(matrix.cols(), 3);
    EXPECT_EQ(matrix(0, 0), 1.0);
    EXPECT_EQ(matrix(2, 2), 3.0);
}

/**
 * @test InputTest::ParsesValidComplexMatrix
 * @brief Validates parsing a complex matrix from input.
 */
TEST_F(InputTest, ParsesValidComplexMatrix) {
    const std::string fileName = "valid_complex_matrix.txt";
    const std::string content = R"(
        METHOD qr
        TOLERANCE 1e-8
        MAX_ITER 500
        COMPLEX 1
        MATRIX_DATA
        2 2
        1 1 0 1
        0 -1 1 0
    )";

    ASSERT_NO_THROW(ReadTestFile(fileName, content));
    EXPECT_EQ(input.GetMethod(), "qr");
    EXPECT_EQ(input.GetTolerance(), 1e-8);
    EXPECT_EQ(input.GetMaxIter(), 500);
    EXPECT_TRUE(input.GetIsComplex());

    Eigen::MatrixXcd matrix = input.GetComplexMatrix();
    ASSERT_EQ(matrix.rows(), 2);
    ASSERT_EQ(matrix.cols(), 2);
    EXPECT_EQ(matrix(0, 0), std::complex<double>(1, 1));
    EXPECT_EQ(matrix(1, 0), std::complex<double>(0, -1));
}

/**
 * @test InputTest::ThrowsForInvalidMatrixDimensions
 * @brief Validates exception is thrown for invalid matrix dimensions.
 */
TEST_F(InputTest, ThrowsForInvalidMatrixDimensions) {
    const std::string fileName = "invalid_matrix_dimensions.txt";
    const std::string content = R"(
        METHOD power
        TOLERANCE 1e-8
        MAX_ITER 500
        COMPLEX 0
        MATRIX_DATA
        2 3
        1 2 3
        4 5
    )";

    EXPECT_THROW(ReadTestFile(fileName, content), std::runtime_error);
}

/**
 * @test InputTest::ThrowsForInvalidMethod
 * @brief Validates exception is thrown for invalid METHOD parameter.
 */
TEST_F(InputTest, ThrowsForInvalidMethod) {
    const std::string fileName = "invalid_method.txt";
    const std::string content = R"(
        METHOD invalid_method
        TOLERANCE 1e-8
        MAX_ITER 500
        COMPLEX 0
        MATRIX_DATA
        2 2
        1 0
        0 1
    )";

    EXPECT_THROW(ReadTestFile(fileName, content), std::runtime_error);
}

/**
 * @test InputTest::ParsesSingularMatrix
 * @brief Validates parsing a singular matrix from input.
 */
TEST_F(InputTest, ParsesSingularMatrix) {
    const std::string fileName = "singular_matrix.txt";
    const std::string content = R"(
        METHOD power
        TOLERANCE 1e-8
        MAX_ITER 500
        COMPLEX 0
        MATRIX_DATA
        2 2
        1 0
        0 0
    )";

    ASSERT_NO_THROW(ReadTestFile(fileName, content));
    auto matrix = input.GetRealMatrix();
    ASSERT_EQ(matrix.rows(), 2);
    ASSERT_EQ(matrix.cols(), 2);
    EXPECT_EQ(matrix(1, 1), 0.0);
}

/**
 * @test InputTest::ThrowsForMissingMatrixData
 * @brief Validates exception is thrown when MATRIX_DATA is missing.
 */
TEST_F(InputTest, ThrowsForMissingMatrixData) {
    const std::string fileName = "missing_matrix_data.txt";
    const std::string content = R"(
        METHOD power
        TOLERANCE 1e-8
        MAX_ITER 500
        COMPLEX 0
    )";

    EXPECT_THROW(ReadTestFile(fileName, content), std::runtime_error);
}

// ============================== Solver Class Tests ==============================

/**
 * @class SolverTest
 * @brief Google Test fixture for testing various solver classes.
 */
class SolverTest : public ::testing::Test {
protected:
    Input input; ///< Instance of `Input` for testing solvers.

    /**
     * @brief Helper function to read and parse a temporary test file.
     *
     * @param fileName Name of the file to read.
     * @param content Content to write to the file.
     */
    void ReadTestFile(const std::string& fileName, const std::string& content) {
        WriteToTempFile(fileName, content);
        input.ReadFile(fileName);
        CleanUpTempFile(fileName);
    }
};

/**
 * @test SolverTest::PowerMethodSolverRealMatrix
 * @brief Validates the Power Method solver with a real matrix.
 *
 * Tests that the solver correctly computes the largest eigenvalue.
 */
TEST_F(SolverTest, PowerMethodSolverRealMatrix) {
    const std::string fileName = "power_solver_real_input.txt";
    const std::string content = R"(
        METHOD power
        MAX_ITER 500
        TOLERANCE 1e-8
        COMPLEX 0
        MATRIX_DATA
        3 3
        4 1 0
        0 3 2
        0 0 2
    )";

    ReadTestFile(fileName, content);

    PowerMethodSolver<Eigen::MatrixXd, double> solver(input);
    auto result = solver.solve();

    EXPECT_NEAR(result, 4.0, 1e-8); ///< Largest eigenvalue
}

/**
 * @test SolverTest::InversePowerMethodSolverRealMatrix
 * @brief Validates the Inverse Power Method solver with a real matrix.
 *
 * Tests that the solver computes the eigenvalue closest to a given shift.
 */
TEST_F(SolverTest, InversePowerMethodSolverRealMatrix) {
    const std::string fileName = "shift_solver_real_input.txt";
    const std::string content = R"(
        METHOD shift
        MAX_ITER 500
        TOLERANCE 1e-9
        SHIFT 0
        COMPLEX 0
        MATRIX_DATA
        3 3
        4 1 0
        0 3 2
        0 0 2
    )";

    ReadTestFile(fileName, content);

    InversePowerMethodSolver<Eigen::MatrixXd, double> solver(input);
    auto result = solver.solve();

    EXPECT_NEAR(result, 2.0, 1e-8); ///< Eigenvalue closest to shift
}

/**
 * @test SolverTest::QRMethodSolverRealMatrix
 * @brief Validates the QR Method solver with a real matrix.
 *
 * Ensures the solver computes all eigenvalues accurately.
 */
TEST_F(SolverTest, QRMethodSolverRealMatrix) {
    const std::string fileName = "qr_solver_real_input.txt";
    const std::string content = R"(
        METHOD qr
        MAX_ITER 500
        TOLERANCE 1e-8
        COMPLEX 0
        MATRIX_DATA
        3 3
        4 1 0
        0 3 2
        0 0 2
    )";

    ReadTestFile(fileName, content);

    QRMethodSolver<Eigen::MatrixXd, Eigen::VectorXd> solver(input);
    auto result = solver.solve();

    ASSERT_EQ(result.size(), 3); ///< Ensure correct result size.
    EXPECT_NEAR(result(0), 4.0, 1e-8); ///< Largest eigenvalue.
    EXPECT_NEAR(result(1), 3.0, 1e-8); ///< Middle eigenvalue.
    EXPECT_NEAR(result(2), 2.0, 1e-8); ///< Smallest eigenvalue.
}

/**
 * @test SolverTest::PowerMethodSolverComplexMatrix
 * @brief Validates the Power Method solver with a complex matrix.
 *
 * Ensures the solver correctly computes the largest eigenvalue with both real
 * and imaginary parts.
 */
TEST_F(SolverTest, PowerMethodSolverComplexMatrix) {
    const std::string fileName = "power_solver_complex_input.txt";
    const std::string content = R"(
        METHOD power
        MAX_ITER 500
        TOLERANCE 1e-8
        COMPLEX 1
        MATRIX_DATA
        2 2
        0 1 -1 0
        1 0 0 1
    )";

    ReadTestFile(fileName, content);

    PowerMethodSolver<Eigen::MatrixXcd, std::complex<double>> solver(input);
    auto result = solver.solve();

    EXPECT_NEAR(result.real(), 0.0, 1e-8); ///< Real part of the largest eigenvalue.
    EXPECT_NEAR(result.imag(), 2.0, 1e-8); ///< Imaginary part of the largest eigenvalue.
}

/**
 * @test SolverTest::QRMethodSolverComplexMatrix
 * @brief Validates the QR Method solver with a complex matrix.
 *
 * Ensures the solver computes all eigenvalues accurately.
 */
TEST_F(SolverTest, QRMethodSolverComplexMatrix) {
    const std::string fileName = "qr_solver_complex_input.txt";
    const std::string content = R"(
        METHOD qr
        MAX_ITER 500
        TOLERANCE 1e-8
        COMPLEX 1
        MATRIX_DATA
        3 3
        0 1 -1 0 0 0
        1 0 0 1 0 0
        0 0 1 0 0 -1
    )";

    ReadTestFile(fileName, content);

    QRMethodSolver<Eigen::MatrixXcd, Eigen::VectorXcd> solver(input);
    auto result = solver.solve();

    ASSERT_EQ(result.size(), 3); ///< Ensure correct result size.

    // Validate eigenvalues
    EXPECT_NEAR(result(0).real(), 0.0, 1e-8);
    EXPECT_NEAR(result(0).imag(), 2.0, 1e-8);

    EXPECT_NEAR(result(1).real(), 0.0, 1e-8);
    EXPECT_NEAR(result(1).imag(), -1.0, 1e-8);

    EXPECT_NEAR(result(2).real(), 0.0, 1e-8);
    EXPECT_NEAR(result(2).imag(), 0.0, 1e-8);
}

/**
 * @brief Executes the Inverse Power Method Solver and propagates exceptions.
 *
 * This function is designed to test scenarios where the solver is expected
 * to fail (or not)due to invalid input (e.g., singular matrices). It is used to test
 * the difference between singular matrices and the case where the file doesn't converge .
 *
 * @param input An instance of the `Input` class containing solver configuration.
 * @throws std::runtime_error If the solver encounters an issue during execution.
 */
void RunSolverAndThrow(Input& input) {
    InversePowerMethodSolver<Eigen::MatrixXd, double> solver(input);
    solver.solve(); // This will throw an exception if the matrix is singular or invalid.
}
/**
 * @test SolverTest::InversePowerMethodSolverSingularRealMatrixThrows
 * @brief Validates exception handling for singular real matrices in the Inverse Power Method solver.
 *
 * Tests that the solver throws a runtime error when solving a singular matrix with a shift of 0.
 */
TEST_F(SolverTest, InversePowerMethodSolverSingularRealMatrixThrows) {
    const std::string fileName = "inverse_power_solver_singular_real_input.txt";
    const std::string content = R"(
        METHOD shift
        MAX_ITER 500
        TOLERANCE 1e-8
        SHIFT 0.0
        COMPLEX 0
        MATRIX_DATA
        3 3
        1 0 0
        0 0 0
        0 0 1
    )";

    // Write the input data to a temporary file and read it.
    ReadTestFile(fileName, content);

    // Use the RunSolverAndThrow helper function to execute the solver.
    // Expect a runtime error due to the singular matrix.
    EXPECT_THROW(
        RunSolverAndThrow(input),
        std::runtime_error
    );
}

/**
 * @test SolverTest::InversePowerMethodSolverSingularRealMatrixThrowsWithShift
 * @brief Validates exception handling for singular real matrices in the Inverse Power Method solver with a non-zero shift.
 *
 * Ensures the solver throws a runtime error even when a shift (e.g., 2.0) is applied.
 */
TEST_F(SolverTest, InversePowerMethodSolverSingularRealMatrixThrowsWithShift) {
    const std::string fileName = "inverse_power_solver_singular_real_input.txt";
    const std::string content = R"(
        METHOD shift
        MAX_ITER 500
        TOLERANCE 1e-8
        SHIFT 2.0
        COMPLEX 0
        MATRIX_DATA
        3 3
        1 0 0
        0 2 0
        0 0 3
    )";

    // Write the input data to a temporary file and read it.
    ReadTestFile(fileName, content);

    // Use the RunSolverAndThrow helper function to execute the solver.
    // Expect a runtime error due to the singular matrix.
    EXPECT_THROW(
        RunSolverAndThrow(input),
        std::runtime_error
    );
}

/**
 * @test SolverTest::QRConvergenceTest
 * @brief Validates the QR Method solver's convergence for a simple real matrix.
 *
 * Ensures the solver runs without throwing any errors when handling a non-singular matrix.
 */
TEST_F(SolverTest, QRConvergenceTest) {
    const std::string fileName = "QRConvergenceTest.txt";
    const std::string content = R"(
        METHOD qr
        MAX_ITER 500
        TOLERANCE 1e-8
        COMPLEX 0
        MATRIX_DATA
        2 2
        1 -1
        1 1
    )";

    // Write the input data to a temporary file and read it.
    ReadTestFile(fileName, content);

    // Use the RunSolverAndThrow helper function to execute the solver.
    // Expect the solver to run without throwing exceptions.
    ASSERT_NO_THROW(
        RunSolverAndThrow(input)
    );
}