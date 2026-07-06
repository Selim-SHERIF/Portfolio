#ifndef OUTPUT_HPP
#define OUTPUT_HPP

/**
 * @file output.hpp
 * @brief Declaration of the Output class for handling formatted output of eigenvalue solver results.
 *
 * This header file defines the `Output` class, which provides methods for:
 * - Printing styled headers and results to the console.
 * - Saving results to an external file.
 * - Managing output formatting for both real and complex eigenvalues.
 * - Displaying input summaries and error messages.
 *
 * The class leverages ANSI escape codes for styled terminal output and supports
 * detailed formatting for matrices and vectors.
 */

#include <fstream>
#include <sstream>
#include <string>
#include <utility>
#include "input.hpp"

// ANSI escape codes for styled console output
#define RESET   "\033[0m"
#define GREEN   "\033[32m"
#define CYAN    "\033[36m"
#define MAGENTA "\033[35m"
#define BOLD    "\033[1m"
#define RED     "\033[31m"

/**
 * @class Output
 * @brief Handles formatted output of eigenvalue solver results.
 *
 * The `Output` class provides functionality to display and save results of eigenvalue solvers.
 * It includes methods for:
 * - Displaying headers and results in a styled format on the console.
 * - Writing results and errors to a file.
 * - Managing formatted output for real and complex eigenvalues.
 *
 * @note ANSI escape codes are used for terminal styling, which may not be supported in all environments.
 */

class Output {

private:

    std::string outputFileName;         ///< Name of the output file
    std::ostringstream outputBuffer;    ///< Buffer for collecting formatted output

public:

    // Constructor
    explicit Output(std::string  fileName = "output.txt")
        : outputFileName(std::move(fileName)) {}    ///< Constructor

    // Output methods
    void PrintHeader(const std::string& title); ///< Displays a styled header
    template <typename T>
    void WriteEigenvalue(const T& eigenvalue, const std::string& method);   ///< Writes eigenvalues
    void WriteSummary(const Input& inputFile);  ///< Writes a summary of the input parameters
    void DisplayError(const std::string& message); ///< Displays error messages
    void WriteToFile(const std::string& message); ///< Appends messages to the output file
    void SaveToFile() const;    ///< Saves the output to the specified file
    void Clear();   ///< Clears the output buffer
    void OpenFile() const;  ///< Opens the output file with the system's default application.
};

#include "output_imp.hpp"

#endif // OUTPUT_HPP
