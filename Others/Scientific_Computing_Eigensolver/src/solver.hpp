#ifndef SOLVER_HPP
#define SOLVER_HPP

/**
 * @file solver.hpp
 * @brief Declaration of eigenvalue solvers using Power Method, Inverse Power Method, and QR Algorithm.
 *
 * Defines the abstract base class `Solver` and its derived classes for computing eigenvalues
 * using various numerical techniques. Includes support for real and complex matrices.
 */

#include "input.hpp"
#include <Eigen/Dense>
#include <type_traits>

/**
 * @brief Type trait to deduce the vector type based on the matrix type.
 */
template <typename MatrixType>
struct VectorType {};

// Specialization for real-valued matrices
template <>
struct VectorType<Eigen::MatrixXd> {
    using type = Eigen::VectorXd;
};

// Specialization for complex-valued matrices
template <>
struct VectorType<Eigen::MatrixXcd> {
    using type = Eigen::VectorXcd;
};

/**
 * @class Solver
 * @brief Base class for eigenvalue solvers.
 *
 * Provides the interface and common functionality for eigenvalue solvers.
 *
 * @tparam MatrixType The type of the matrix (real or complex).
 * @tparam T The type of the eigenvalue (real or complex).
 */
template <typename MatrixType, typename T>
class Solver {

protected:

    Input& mInputFile;  ///< Reference to the Input object
    bool success = true; ///< Status of computation success
    std::string errorMessage; ///< Stores error messages

public:

    explicit Solver(Input& mInputFile) : mInputFile(mInputFile) {}  ///< Constructor taking an Input object reference
    virtual ~Solver() = default;    ///< Virtual destructor

    virtual T solve() const = 0; ///< Pure virtual method for solving the eigenvalue problem

    MatrixType GetMatrix() const;   ///< Retrieve the matrix from the input file
    bool GetStatus() const { return success; } ///< Returns the success flag
    std::string GetErrorMessage() const { return errorMessage; } ///< Returns the error message
    typename VectorType<MatrixType>::type CreateVector() const; ///< Create vector initialized to ones
};

/**
 * @class PowerMethodSolver
 * @brief Solver for computing the dominant eigenvalue using the Power Method.
 *
 * The Power Method iteratively computes the dominant eigenvalue (the eigenvalue with the largest absolute value)
 * and its corresponding eigenvector for a given square matrix. This solver is suitable for real and complex matrices
 * and relies on a tolerance threshold and a maximum number of iterations to determine convergence.
 *
 * @tparam MatrixType The type of the matrix (Eigen::MatrixXd for real or Eigen::MatrixXcd for complex).
 * @tparam T The type of the eigenvalue (double for real or std::complex<double> for complex).
 */
template <typename MatrixType, typename T>
class PowerMethodSolver : public Solver<MatrixType, T> {
public:
    explicit PowerMethodSolver(Input& mInputFile) : Solver<MatrixType, T>(mInputFile) {}    ///< Constructor
    T solve() const override;   ///< Solve the eigenvalue problem using the Power Method
};

/**
 * @class InversePowerMethodSolver
 * @brief Solver for computing an eigenvalue close to a given shift using the Inverse Power Method.
 *
 * The Inverse Power Method isolates and computes an eigenvalue near a user-defined shift value.
 * This solver is particularly useful for finding eigenvalues other than the dominant one.
 * Convergence is determined by a tolerance threshold and a maximum number of iterations.
 *
 * @tparam MatrixType The type of the matrix (Eigen::MatrixXd for real or Eigen::MatrixXcd for complex).
 * @tparam T The type of the eigenvalue (double for real or std::complex<double> for complex).
 *
 * @note If the shifted matrix is singular or nearly singular, the method may fail.
 */
template <typename MatrixType, typename T>
class InversePowerMethodSolver : public Solver<MatrixType, T> {
public:
    explicit InversePowerMethodSolver(Input& mInputFile) : Solver<MatrixType, T>(mInputFile) {} ///< Constructor
    T solve() const override;   ///< Solve the eigenvalue problem using the Inverse Power Method with Shift
};

/**
 * @class QRMethodSolver
 * @brief Solver for computing all eigenvalues using the QR Algorithm.
 *
 * The QR Algorithm decomposes a given square matrix into Q (orthogonal) and R (upper triangular) matrices
 * iteratively. It computes all eigenvalues of the matrix by transforming it into an upper triangular form,
 * where the diagonal entries represent the eigenvalues.
 *
 * @tparam MatrixType The type of the matrix (Eigen::MatrixXd for real or Eigen::MatrixXcd for complex).
 * @tparam T The type of the eigenvalues (Eigen::VectorXd for real or Eigen::VectorXcd for complex).
 */
template <typename MatrixType, typename T>
class QRMethodSolver : public Solver<MatrixType, T> {
public:
    explicit QRMethodSolver(Input& mInputFile) : Solver<MatrixType, T>(mInputFile) {}   ///< Constructor
    T solve() const override;   ///< Solve the eigenvalue problem using the QR algorithm
};

#include "solver_imp.hpp"

#endif // SOLVER_HPP