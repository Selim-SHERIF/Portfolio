#ifndef INPUT_HPP
#define INPUT_HPP

/**
 * @file input.hpp
 * @brief Declaration of the Input class for managing numerical parameters and matrices from a file.
 *
 * This header file defines the `Input` class, which provides methods to read and store configuration
 * parameters and matrix data for numerical computations. It supports both real and complex matrices.
 *
 * Key Features:
 * - Reads numerical parameters like tolerance, maximum iterations, shift, and method.
 * - Parses square matrices from an input file in a defined format.
 * - Supports validation of parameters and matrix data.
 */

# include <string>
# include <Eigen/Dense>

/**
 * @class Input
 * @brief Class to handle numerical input parameters and matrices from a file.
 *
 * The Input class provides methods to read configuration data and matrices
 * from a file and store them for numerical computations. It supports both
 * real and complex matrices.
 *
 * @note The matrix must be square, and numerical parameters such as tolerance
 * and maximum iterations have specific constraints.
 */

class Input {

private:

    Eigen::MatrixXd mReal_A;        ///< Stores the real matrix read from the input file
    Eigen::MatrixXcd mComplex_A;    ///< Stores the complex matrix read from the input file
    int mDimension;                 ///< The dimension of the square matrix
    std::string mMethod;            ///< The numerical method to be used ("qr", "power", or "shift")
    bool mIsComplex;                ///< Flag indicating whether the matrix is complex or real
    int mMaxIter;                   ///< Maximum number of iterations
    double mTolerance;              ///< Convergence tolerance for iterative methods
    double mShift;                  ///< Shift value for the inverse power method

public:

    // Default constructor
    Input() : mMethod("qr"), mIsComplex(false), mMaxIter(500), mTolerance(1e-10), mShift(0.0) {}

    // Access to private members
    Eigen::MatrixXd GetRealMatrix() const;
    Eigen::MatrixXcd GetComplexMatrix() const;
    int GetDimension() const;
    std::string GetMethod() const;
    bool GetIsComplex() const;
    int GetMaxIter() const;
    double GetTolerance() const;
    double GetShift() const;

    // Input methods
    void ReadFile(const std::string& fileName);
    void ReadMatrixData(std::ifstream &file, int rows, int cols);
};

#endif //INPUT_HPP