#ifndef OUTPUT_IMPL_HPP
#define OUTPUT_IMPL_HPP

/**
 * @file output_imp.hpp
 * @brief Implementation of the Output class methods for managing formatted output.
 *
 * This file provides the implementation of the `Output` class declared in `output.hpp`.
 * It includes methods for styled console output, saving results to a file,
 * and formatting real and complex eigenvalues.
 */

#include <iomanip>
#include <thread>

/**
 * @brief Utility function to center-align text.
 * @param text The text to center.
 * @param totalWidth Total width of the field.
 * @return A string with the text centered.
 */
inline std::string centerText(const std::string& text, int totalWidth) {
    if (text.size() >= totalWidth) {
        return text.substr(0, totalWidth); // Truncate if text is too wide
    }
    int paddingLeft = (totalWidth - text.size()) / 2;
    int paddingRight = totalWidth - text.size() - paddingLeft; // Remaining padding goes to the right
    return std::string(paddingLeft, ' ') + text + std::string(paddingRight, ' ');
}

/**
 * @brief Utility function to convert a complex number to a formatted string.
 * @tparam T The numeric type of the complex number.
 * @param c The complex number to convert.
 * @return A string representation of the complex number.
 */
template <typename T>
std::string complexToString(const std::complex<T>& c) {
    std::ostringstream oss;
    oss << c.real() << (c.imag() >= 0 ? "+" : "") << c.imag() << "i";
    return oss.str();
}

/**
 * @brief Displays a styled header with a title.
 * @param title The title to display.
 */
inline void Output::PrintHeader(const std::string& title) {
    const int SEPARATOR_WIDTH = 50;
    const std::string header = R"(
   _____                 ____     __
  / __(_)__ ____ ___    / __/__  / /  _____ ____
 / _// / _ `/ -_) _ \  _\ \/ _ \/ / |/ / -_) __/
/___/_/\_, /\__/_//_/ /___/\___/_/|___/\__/_/
      /___/
    )";

    const std::string separator(SEPARATOR_WIDTH, '=');

    // Print header
    std::cout << header << "\n" << BOLD << MAGENTA << centerText(title, SEPARATOR_WIDTH) << "\n" << RESET << std::endl;
    outputBuffer << header << "\n" << title << "\n\n";
}

/**
 * @brief Writes eigenvalue(s) to both the terminal and the output file.
 *
 * @tparam T The type of eigenvalue (scalar, complex, or vector).
 * @param eigenvalue The computed eigenvalue(s).
 * @param method The name of the method used to compute the eigenvalue(s).
 */
template <typename T>
void Output::WriteEigenvalue(const T& eigenvalue, const std::string& method) {

    const int SEPARATOR_WIDTH = 50;

    // Terminal Output
    std::ostringstream consoleOutput;
    consoleOutput << CYAN << std::string(SEPARATOR_WIDTH, '=') << "\n";
    consoleOutput << centerText(method, SEPARATOR_WIDTH) << "\n";
    consoleOutput << std::string(SEPARATOR_WIDTH, '=') << "\n" << RESET;

    if constexpr (std::is_scalar<T>::value) {
        // Scalar eigenvalue
        consoleOutput << centerText("Eigenvalue: " + std::to_string(eigenvalue), SEPARATOR_WIDTH) << "\n";
    } else if constexpr (std::is_same<T, std::complex<double>>::value) {
        // Complex eigenvalue
        consoleOutput << centerText("Eigenvalue: " + complexToString(eigenvalue), SEPARATOR_WIDTH) << "\n";
    } else if constexpr (Eigen::MatrixBase<T>::ColsAtCompileTime == 1 || Eigen::MatrixBase<T>::RowsAtCompileTime == 1) {
        // Vector eigenvalues
        consoleOutput << centerText("Index          Eigenvalue", SEPARATOR_WIDTH) << "\n";
        consoleOutput << centerText("-----------------------------------------------", SEPARATOR_WIDTH) << "\n";

        for (int i = 0; i < eigenvalue.size(); ++i) {
            std::ostringstream lineStream;
            if constexpr (std::is_same<typename T::Scalar, std::complex<double>>::value) {
                lineStream << std::setw(10) << i + 1 << std::setw(20) << complexToString(eigenvalue[i]);
            } else {
                lineStream << std::setw(10) << i + 1 << std::setw(20) << eigenvalue[i];
            }
            consoleOutput << centerText(lineStream.str(), SEPARATOR_WIDTH) << "\n";
        }
    }

    consoleOutput << CYAN << std::string(SEPARATOR_WIDTH, '=') << RESET << "\n";
    std::cout << consoleOutput.str();

    // File Output
    std::ostringstream fileOutput;
    fileOutput << std::string(SEPARATOR_WIDTH, '=') << "\n";
    fileOutput << method << "\n";
    fileOutput << std::string(SEPARATOR_WIDTH, '=') << "\n";

    if constexpr (std::is_scalar<T>::value) {
        fileOutput << "Eigenvalue: " << eigenvalue << "\n";
    } else if constexpr (std::is_same<T, std::complex<double>>::value) {
        fileOutput << "Eigenvalue: " << complexToString(eigenvalue) << "\n";
    } else if constexpr (Eigen::MatrixBase<T>::ColsAtCompileTime == 1 || Eigen::MatrixBase<T>::RowsAtCompileTime == 1) {
        fileOutput << "Index          Eigenvalue\n";
        fileOutput << "-----------------------------------------------\n";
        for (int i = 0; i < eigenvalue.size(); ++i) {
            if constexpr (std::is_same<typename T::Scalar, std::complex<double>>::value) {
                fileOutput << std::setw(10) << i + 1 << std::setw(20) << complexToString(eigenvalue[i]) << "\n";
            } else {
                fileOutput << std::setw(10) << i + 1 << std::setw(20) << eigenvalue[i] << "\n";
            }
        }
    }

    fileOutput << std::string(SEPARATOR_WIDTH, '=') << "\n";
    outputBuffer << fileOutput.str();  // Add the formatted message to the buffer
}

/**
 * @brief Writes a summary of input parameters to the output.
 */
inline void Output::WriteSummary(const Input& inputFile) {

    const int SEPARATOR_WIDTH = 50;
    const std::string separator(SEPARATOR_WIDTH, '=');

    // Console Output
    std::ostringstream consoleOutput;
    consoleOutput << MAGENTA << separator << "\n";
    consoleOutput << centerText("Input Summary", SEPARATOR_WIDTH) << "\n";
    consoleOutput << separator << "\n" << RESET;

    // Matrix type
    consoleOutput << "Matrix Type: " << (inputFile.GetIsComplex() ? "Complex" : "Real") << "\n";

    // Matrix dimension
    consoleOutput << "Dimension: " << inputFile.GetDimension() << "x" << inputFile.GetDimension() << "\n";

    // Parameters
    consoleOutput << "Tolerance: " << inputFile.GetTolerance() << "\n";
    consoleOutput << "Max Iterations: " << inputFile.GetMaxIter() << "\n";

    if (inputFile.GetMethod() == "shift") {
        consoleOutput << "Shift: " << inputFile.GetShift() << "\n";
    }

    // Print the matrix elegantly
    consoleOutput << "\nMatrix:\n";
    if (inputFile.GetIsComplex()) {
        const auto& matrix = inputFile.GetComplexMatrix();
        for (int i = 0; i < matrix.rows(); ++i) {
            for (int j = 0; j < matrix.cols(); ++j) {
                std::ostringstream cell;
                cell << std::fixed << std::setprecision(2)
                     << matrix(i, j).real() << (matrix(i, j).imag() >= 0 ? "+" : "")
                     << matrix(i, j).imag() << "i";
                consoleOutput << std::setw(15) << cell.str() << " ";
            }
            consoleOutput << "\n";
        }
    } else {
        const auto& matrix = inputFile.GetRealMatrix();
        for (int i = 0; i < matrix.rows(); ++i) {
            for (int j = 0; j < matrix.cols(); ++j) {
                consoleOutput << std::setw(15) << std::fixed << std::setprecision(2)
                              << matrix(i, j) << " ";
            }
            consoleOutput << "\n";
        }
    }

    // Display in terminal
    std::cout << consoleOutput.str();

    // File Output (plain, not centered)
    std::ostringstream fileOutput;
    fileOutput << separator << "\n";
    fileOutput << "Input Summary\n";
    fileOutput << separator << "\n";

    fileOutput << "Matrix Type: " << (inputFile.GetIsComplex() ? "Complex" : "Real") << "\n";
    fileOutput << "Dimension: " << inputFile.GetDimension() << "x" << inputFile.GetDimension() << "\n";
    fileOutput << "Tolerance: " << inputFile.GetTolerance() << "\n";
    fileOutput << "Max Iterations: " << inputFile.GetMaxIter() << "\n";

    if (inputFile.GetMethod() == "shift") {
        fileOutput << "Shift: " << inputFile.GetShift() << "\n";
    }

    fileOutput << "\nMatrix:\n";
    if (inputFile.GetIsComplex()) {
        const auto& matrix = inputFile.GetComplexMatrix();
        for (int i = 0; i < matrix.rows(); ++i) {
            for (int j = 0; j < matrix.cols(); ++j) {
                fileOutput << std::setw(15) << std::fixed << std::setprecision(2)
                           << matrix(i, j).real() << (matrix(i, j).imag() >= 0 ? "+" : "")
                           << matrix(i, j).imag() << "i" << " ";
            }
            fileOutput << "\n";
        }
    } else {
        const auto& matrix = inputFile.GetRealMatrix();
        for (int i = 0; i < matrix.rows(); ++i) {
            for (int j = 0; j < matrix.cols(); ++j) {
                fileOutput << std::setw(15) << std::fixed << std::setprecision(2)
                           << matrix(i, j) << " ";
            }
            fileOutput << "\n";
        }
    }

    fileOutput << separator << "\n";
    outputBuffer << fileOutput.str();
}


/**
 * @brief Displays an error message in a styled format on the console and logs it to the output file.
 *
 * @param message The error message to display in the terminal and log in the output file.
 */
inline void Output::DisplayError(const std::string& message) {
    const int SEPARATOR_WIDTH = 50;

    // Styled console output
    std::ostringstream consoleOutput;
    consoleOutput << BOLD << RED << std::string(SEPARATOR_WIDTH, '=') << "\n";
    consoleOutput << centerText("ERROR/WARNING", SEPARATOR_WIDTH) << "\n";
    consoleOutput << std::string(SEPARATOR_WIDTH, '=') << "\n";
    consoleOutput << RESET << message << "\n";
    consoleOutput << BOLD << RED << std::string(SEPARATOR_WIDTH, '=') << RESET << "\n";

    // Display error in the terminal
    std::cout << consoleOutput.str();

    // Log the error message to the output file
    std::ostringstream fileOutput;
    fileOutput << std::string(SEPARATOR_WIDTH, '=') << "\n";
    fileOutput << "ERROR/WARNING\n";
    fileOutput << std::string(SEPARATOR_WIDTH, '=') << "\n";

    // Append the formatted error message to the output buffer
    outputBuffer << fileOutput.str();
}

/**
 * @brief Logs a message to the output file, including eigenvalues or error details.
 *
 * @param message The message to log in the output file.
 */
inline void Output::WriteToFile(const std::string& message) {
    const int SEPARATOR_WIDTH = 50;

    // Append to the output buffer for saving to the file
    std::ostringstream fileOutput;
    fileOutput << std::string(SEPARATOR_WIDTH, '=') << "\n";
    fileOutput << message << "\n";
    fileOutput << std::string(SEPARATOR_WIDTH, '=') << "\n";

    outputBuffer << fileOutput.str();  // Add the formatted message to the buffer
}

/**
 * @brief Writes eigenvalue(s) to both the terminal and the output file.
 *
 * @tparam T The type of eigenvalue (scalar, complex, or vector).

/**
 * @brief Saves the collected output to the specified file.
 */
inline void Output::SaveToFile() const {
    std::ofstream outFile(outputFileName);
    if (outFile.is_open()) {
        outFile << outputBuffer.str();
        outFile.close();
    }
}

/**
 * @brief Clears the output buffer.
 */
inline void Output::Clear() {
    outputBuffer.str("");
    outputBuffer.clear();
}

/**
 * @brief Opens the output file.
 */
inline void Output::OpenFile() const {
#ifdef _WIN32
    system(("start " + outputFileName).c_str());
#elif __APPLE__
    system(("open " + outputFileName).c_str());
#else
    system(("xdg-open " + outputFileName).c_str());
#endif
}

#endif // OUTPUT_IMPL_HPP
