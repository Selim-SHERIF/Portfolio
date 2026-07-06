#ifndef SOLVER_IMP_HPP
#define SOLVER_IMP_HPP

/**
 * @file solver_imp.hpp
 * @brief Implementation of the Solver classes and their respective eigenvalue computation methods.
 *
 * This file provides the implementation of the methods declared in `solver.hpp`, including
 * the Power Method, Inverse Power Method with Shift, and the QR Algorithm.
 */

#include "solver.hpp"

template <typename MatrixType, typename T>
MatrixType Solver<MatrixType, T>::GetMatrix() const {

    if (mInputFile.GetIsComplex()) {
        if constexpr (std::is_same<MatrixType, Eigen::MatrixXcd>::value) {
            return mInputFile.GetComplexMatrix();
        } else {
            throw std::runtime_error("Matrix type mismatch: Expected a real matrix, but input is complex.");
        }
    } else {
        if constexpr (std::is_same<MatrixType, Eigen::MatrixXd>::value) {
            return mInputFile.GetRealMatrix();
        } else {
            throw std::runtime_error("Matrix type mismatch: Expected a complex matrix, but input is real.");
        }
    }
}

/**
 * @brief Create a vector of the appropriate type, initialized to ones.
 *
 * The vector type is determined using the `VectorType` trait based on the matrix type.
 *
 * @return A vector of type `VectorType<MatrixType>::type`, initialized with ones.
 */
template <typename MatrixType, typename T>
typename VectorType<MatrixType>::type Solver<MatrixType, T>::CreateVector() const {
    typename VectorType<MatrixType>::type vec(mInputFile.GetDimension());
    vec.setOnes();
    return vec;
}

/**
 * @brief Compute the dominant eigenvalue using the Power Method.
 *
 * This iterative method estimates the largest eigenvalue of the matrix by repeatedly
 * multiplying a vector with the matrix. The eigenvalue is computed using the Rayleigh quotient.
 *
 * @return The dominant eigenvalue of type T (double or std::complex<double>).
 */
template <typename MatrixType, typename T>
T PowerMethodSolver<MatrixType, T>::solve() const {

    typename VectorType<MatrixType>::type x = this->CreateVector();
    typename VectorType<MatrixType>::type x_new = x;

    const double Tolerance = this->mInputFile.GetTolerance();
    const int MaxIter = this->mInputFile.GetMaxIter();
    int iter = 0;
    T Eigenvalue = 0.0;

    for (iter = 0; iter < MaxIter; ++iter) {
        x_new = this->GetMatrix() * x;
        x_new.normalize();
        Eigenvalue = x.dot(this->GetMatrix() * x);

        if ((this->GetMatrix() * x - Eigenvalue * x).norm() < Tolerance) {
            break;
        }

        x = x_new;
    }

    if (iter == MaxIter) {
        const_cast<PowerMethodSolver*>(this)->success = false;
        const_cast<PowerMethodSolver*>(this)->errorMessage =
            "Warning: Power Method did not converge within maximum number of iterations. "
            "Try increasing MAX_ITER or eigenvalue might be complex.";
    }

    return Eigenvalue;
}

/**
 * @brief Compute any eigenvalue using the Inverse Power Method with a specified shift.
 *
 * This method applies a shift to the matrix and solves a linear system iteratively to find
 * an eigenvalue near the specified shift.
 *
 * @return An eigenvalue of type T (double or std::complex<double>).
 * @throws std::runtime_error If the shifted matrix is singular or the method fails to converge.
 */
template <typename MatrixType, typename T>
T InversePowerMethodSolver<MatrixType, T>::solve() const {

    const int N = this->mInputFile.GetDimension();
    MatrixType ShiftedMatrix = this->GetMatrix() - this->mInputFile.GetShift() * MatrixType::Identity(N, N);

    if (std::abs(ShiftedMatrix.determinant()) < 1e-8) {
        throw std::runtime_error("Matrix with shift is singular, cannot proceed with the Inverse Power Method.");
    }

    typename VectorType<MatrixType>::type x = this->CreateVector();
    typename VectorType<MatrixType>::type x_new = x;

    const double Tolerance = this->mInputFile.GetTolerance();
    const int MaxIter = this->mInputFile.GetMaxIter();
    int iter = 0;
    T Eigenvalue = 0.0;

    for (int i = 0; i < MaxIter; i++) {
        x_new = ShiftedMatrix.householderQr().solve(x);
        x_new.normalize();
        Eigenvalue = x_new.dot(this->GetMatrix() * x_new);

        if ((this->GetMatrix() * x_new - Eigenvalue * x_new).norm() < Tolerance) {
            break;
        }

        x = x_new;
        iter++;
    }

    if (iter == MaxIter) {
        const_cast<InversePowerMethodSolver*>(this)->success = false;
        const_cast<InversePowerMethodSolver*>(this)->errorMessage =
            "Warning: Inverse Power Method did not converge within maximum number of iterations. "
            "Try increasing MAX_ITER or eigenvalue might be complex.";
    }

    return Eigenvalue;
}

/**
 * @brief Compute all eigenvalues using the QR Algorithm.
 *
 * This iterative algorithm uses QR decomposition to transform the matrix into an upper
 * triangular form. The eigenvalues are then extracted from the diagonal of the resulting matrix.
 *
 * @return A vector containing all eigenvalues of type T (double or std::complex<double>).
 */
template <typename MatrixType, typename T>
T QRMethodSolver<MatrixType, T>::solve() const {

    MatrixType K = this->GetMatrix();
    const int MaxIter = this->mInputFile.GetMaxIter();
    int iter = 0;

    while (iter < MaxIter) {
        iter++;
        Eigen::HouseholderQR<MatrixType> qr(K);
        MatrixType Q = qr.householderQ();
        MatrixType R = qr.matrixQR().template triangularView<Eigen::Upper>();
        K = R * Q;

        bool is_triangular = true;
        for (int i = 0; i < this->mInputFile.GetDimension(); i++) {
            for (int j = 0; j < i; j++) {
                if (std::abs(K(i, j)) > 1e-8) {
                    is_triangular = false;
                    break;
                }
            }
            if (!is_triangular) break;
        }
        if (is_triangular) break;
    }

    if (iter == MaxIter) {
        const_cast<QRMethodSolver*>(this)->success = false;
        const_cast<QRMethodSolver*>(this)->errorMessage =
            "Warning: QR Algorithm did not converge within the maximum number of iterations. "
            "Try increasing MAX_ITER or eigenvalues might be complex.";
    }

    return K.diagonal();
}

#endif // SOLVER_IMP_HPP
