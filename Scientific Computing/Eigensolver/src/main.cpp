#include <iostream>
#include <string>
#include <stdexcept>
#include "input.hpp"
#include "solver.hpp"
#include "output.hpp"

template <typename SolverType, typename T>
void SolveAndWrite(Input& inputFile, Output& outputManager, const std::string& methodName);

int main(int argc, char *argv[]) {

    Output OutputManager("solver_output.txt");

    try {

        std::string inputFileName;

        // Handle input file argument
        if (argc == 2) {
            inputFileName = argv[1];
        } else if (argc == 1) {
            std::cout << "Please enter the input file name: ";
            std::getline(std::cin, inputFileName);
            if (inputFileName.empty()) {
                throw std::invalid_argument("No file name provided.");
            }
        } else {
            throw std::invalid_argument("Too many arguments provided. Usage: ./solver <input_file>");
        }

        // Print Program Header
        OutputManager.PrintHeader("Eigenvalue Solver");

        Input inputFile;

        // Read input file
        inputFile.ReadFile(inputFileName);

        // Solve based on method and matrix type
        bool isComplex = inputFile.GetIsComplex();
        const std::string& method = inputFile.GetMethod();

        if (method == "power") {
            if (isComplex) {
                SolveAndWrite<PowerMethodSolver<Eigen::MatrixXcd, std::complex<double>>, std::complex<double>>(inputFile, OutputManager, "Power Method");
            } else {
                SolveAndWrite<PowerMethodSolver<Eigen::MatrixXd, double>, double>(inputFile, OutputManager, "Power Method");
            }
        } else if (method == "shift") {
            if (isComplex) {
                SolveAndWrite<InversePowerMethodSolver<Eigen::MatrixXcd, std::complex<double>>, std::complex<double>>(inputFile, OutputManager, "Inverse Power Method");
            } else {
                SolveAndWrite<InversePowerMethodSolver<Eigen::MatrixXd, double>, double>(inputFile, OutputManager, "Inverse Power Method");
            }
        } else if (method == "qr") {
            if (isComplex) {
                SolveAndWrite<QRMethodSolver<Eigen::MatrixXcd, Eigen::VectorXcd>, Eigen::VectorXcd>(inputFile, OutputManager, "QR Method");
            } else {
                SolveAndWrite<QRMethodSolver<Eigen::MatrixXd, Eigen::VectorXd>, Eigen::VectorXd>(inputFile, OutputManager, "QR Method");
            }
        }

        // Save results and summary
        OutputManager.WriteSummary(inputFile);
        OutputManager.SaveToFile();
        OutputManager.OpenFile();

    } catch (const std::exception& e) {
        // Log and save error message in case of failure
        std::string errorMessage = "Program error: " + std::string(e.what());
        OutputManager.DisplayError(errorMessage);  // Terminal output
        OutputManager.WriteToFile(errorMessage);   // File output
        OutputManager.SaveToFile();
        OutputManager.OpenFile();
        return 1;  // Exit with error code 1 to indicate failure
    }

    return 0;  // Exit with success code 0
}

/**
 * @brief Template function to execute a solver and handle results or errors.
 *
 * @tparam SolverType The solver class type.
 * @tparam T The type of the eigenvalue result (e.g., double, std::complex<double>, or Eigen vector).
 * @param inputFile The input object with the problem definition.
 * @param outputManager The output manager for logging and saving results.
 * @param methodName The name of the method (e.g., "Power Method").
 */
template <typename SolverType, typename T>
void SolveAndWrite(Input& inputFile, Output& outputManager, const std::string& methodName) {
    SolverType solver(inputFile);
    T result;

    try {
        result = solver.solve();

        if (!solver.GetStatus()) {
            std::string errorMessage = solver.GetErrorMessage() + " Writing current estimate.";
            outputManager.DisplayError(errorMessage);  // Terminal output
            outputManager.WriteToFile(errorMessage);   // File output
            outputManager.WriteEigenvalue(result, methodName + " (NON-CONVERGED)");
        } else {
            outputManager.WriteEigenvalue(result, methodName);
        }
    } catch (const std::exception& e) {
        throw;  // Re-throw exception for `main` to handle
    }
}
