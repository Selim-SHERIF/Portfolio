/**
* @file input.cpp
 * @brief Implementation of the Input class for managing numerical parameters and matrices.
 *
 * This source file provides the implementation of the `Input` class declared in `input.hpp`.
 * It includes methods for reading and validating numerical parameters and matrix data from
 * a file, as well as parsing real and complex matrices.
 *
 * Key Implementation Details:
 * - Uses the Eigen library to store and manipulate matrices.
 * - Performs input validation for numerical parameters and matrix data.
 * - Supports flexible file formats with comments and whitespace handling.
 *
 * Example Input File Format:
 * @code
 * MAX_ITER 500
 * TOLERANCE 1e-10
 * SHIFT 0.5
 * COMPLEX 0
 * METHOD qr
 * MATRIX_DATA
 * 3 3
 * 1.0 2.0 3.0
 * 4.0 5.0 6.0
 * 7.0 8.0 9.0
 * @endcode
 */

# include <iostream>
# include <fstream>
# include <sstream>
# include "input.hpp"

/**
 * @brief Get the real matrix.
 * @return A copy of the real matrix as an Eigen::MatrixXd.
 */
Eigen::MatrixXd Input::GetRealMatrix() const {
    return mReal_A;
}

/**
 * @brief Get the complex matrix.
 * @return A copy of the complex matrix as an Eigen::MatrixXcd.
 */
Eigen::MatrixXcd Input::GetComplexMatrix() const {
    return mComplex_A;
}

/**
 * @brief Get the dimension of the square matrix.
 * @return The dimension as an integer.
 */
int Input::GetDimension() const {
    return mDimension;
}

/**
 * @brief Get the numerical method to be used.
 * @return A string representing the numerical method.
 */
std::string Input::GetMethod() const {
    return mMethod;
}

/**
 * @brief Check whether the matrix is complex or real.
 * @return True if the matrix is complex, false otherwise.
 */
bool Input::GetIsComplex() const {
    return mIsComplex;
}

/**
 * @brief Get the maximum number of iterations.
 * @return The maximum number of iterations as an integer.
 */
int Input::GetMaxIter() const{
    return mMaxIter;
}

/**
 * @brief Get the convergence tolerance.
 * @return The tolerance value as a double.
 */
double Input::GetTolerance() const {
    return mTolerance;
}

/**
 * @brief Get the shift value for the inverse power method.
 * @return The shift value as a double.
 */
double Input::GetShift() const {
    return mShift;
}

/**
 * @brief Read numerical parameters and matrix data from a file.
 *
 * Parses the input file to initialize the numerical parameters and read the
 * matrix data. The file must adhere to a specific format with clearly defined
 * sections for parameters and the matrix.
 *
 * @param fileName The name of the input file to read.
 * @throw std::runtime_error If the file cannot be opened, contains invalid
 * parameters, or is missing the required MATRIX_DATA section.
 */
void Input::ReadFile(const std::string &fileName) {

    // Initialize local variables for reading parameters
    int MaxIter;
    double Shift;
    double Tolerance;
    int isComplex;
    std::string Method;
    int rows = 0, cols = 0;

    bool isMatrixSection = false; // Flag to identify if MATRIX_DATA section is found

    // Open the input file
    std::ifstream file(fileName);
    if (!file.is_open()) {
        throw std::runtime_error("Error opening input file: " + fileName);
    }

    std::string line;
    while (std::getline(file, line)) {
        // Skip empty lines and comments
        if (line.empty() || (line[0] == '/' && line[1] == '/')) {
            continue;
        }

        std::istringstream lineStream(line);

        if (!isMatrixSection) {
            // Parse key-value pairs for parameters
            std::string key;
            lineStream >> key;
            if (key == "MAX_ITER") {
                lineStream >> MaxIter;
                if (MaxIter <= 0) {
                    throw std::runtime_error("Invalid MAX_ITER: must be greater than 0.");
                }
                mMaxIter = MaxIter;
            } else if (key == "TOLERANCE") {
                lineStream >> Tolerance;
                if (Tolerance <= 0.0 || Tolerance > 1.0) {
                    throw std::runtime_error("Invalid TOLERANCE: must be in the range (0, 1].");
                }
                mTolerance = Tolerance;
            } else if (key == "SHIFT") {
                lineStream >> Shift;
                mShift = Shift;
            } else if (key == "COMPLEX") {
                lineStream >> isComplex;
                if (isComplex != 0 && isComplex != 1) {
                    throw std::runtime_error("Invalid COMPLEX flag: must be 0 (false) or 1 (true).");
                }
                mIsComplex = isComplex;
            } else if (key == "METHOD") {
                lineStream >> Method;
                if (Method != "qr" && Method != "power" && Method != "shift") {
                    throw std::runtime_error("Invalid METHOD: must be 'qr', 'power', or 'shift'.");
                }
                mMethod = Method;
            } else if (key == "MATRIX_DATA") {
                isMatrixSection = true; // MATRIX_DATA section starts
            }
        } else {
            // Parse matrix dimensions
            lineStream >> rows >> cols;
            if (rows <= 0 || cols <= 0) {
                throw std::runtime_error("Invalid matrix size: dimensions must be positive.");
            }
            if (rows != cols) {
                throw std::runtime_error("Matrix must be square.");
            }
            mDimension = rows;

            // Allocate matrix space
            if (mIsComplex) {
                mComplex_A.resize(rows, cols);
            } else {
                mReal_A.resize(rows, cols);
            }

            // Read the matrix elements
            ReadMatrixData(file, rows, cols);

            break; // Exit after reading the matrix
        }
    }

    // Ensure MATRIX_DATA section was found
    if (!isMatrixSection) {
        throw std::runtime_error("Missing MATRIX_DATA section in the input file.");
    }

    file.close();
}

/**
 * @brief Read matrix elements from the input file.
 *
 * Parses matrix data from the file after reading its dimensions. The function
 * supports both real and complex matrices based on the `mIsComplex` flag.
 *
 * @param file Reference to the input file stream.
 * @param rows Number of rows in the matrix.
 * @param cols Number of columns in the matrix.
 * @throw std::runtime_error If the data is incomplete, mismatched with
 * dimensions, or contains invalid entries.
 */
void Input::ReadMatrixData(std::ifstream &file, int rows, int cols) {

    std::string line;
    for (int i = 0; i < rows; ++i) {
        if (!std::getline(file, line)) {
            throw std::runtime_error("Incomplete matrix data: missing rows.");
        }

        std::istringstream matrixLine(line);
        for (int j = 0; j < cols; ++j) {
            if (mIsComplex) {
                // Parse complex matrix elements
                double realPart, imagPart;
                if (!(matrixLine >> realPart >> imagPart)) {
                    throw std::runtime_error("Incomplete matrix data: missing elements.");
                }
                mComplex_A(i, j) = std::complex<double>(realPart, imagPart);
            } else {
                // Parse real matrix elements
                double value;
                if (!(matrixLine >> value)) {
                    throw std::runtime_error("Incomplete matrix data: missing elements.");
                }
                mReal_A(i, j) = value;
            }
        }

        // Check for extra elements in the row
        std::string extra;
        if (matrixLine >> extra) {
            throw std::runtime_error("Matrix size mismatch: extra elements in row data.");
        }
    }
}
