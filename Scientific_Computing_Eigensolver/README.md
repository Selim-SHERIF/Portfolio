# Scientific Computing & Coding 💻
## What is the Difference Between Regular Coding and Scientific Computing?
Scientific computing extends beyond functional programming to focus on **optimization**, **efficiency**, **scalability**, and **polymorphism**. It prioritizes extracting the best performance from code while maintaining clarity, flexibility, and reusability.

Key aspects that distinguish scientific computing:
- **Efficiency**: Reducing computational overhead for faster performance.
- **Scalability**: Ensuring the code performs consistently as problem size grows.
- **Polymorphism**: Designing code that adapts seamlessly to different scenarios.
- **Factorization**: Structuring code to minimize redundancy and improve maintainability.

As a specialist in **Computational Science and Engineering**, mastering these principles is essential. This directory features a project (**Eigenvalue Solver**) that emphasizes these aspects, showcasing the importance of writing high-performance scientific code. While the mathematical challenge is simple, the focus is on implementation quality—making it efficient, scalable, and robust.

---

# Eigenvalue Solver 🧮

### Context
This project was undertaken as part of the **MATH-458: EPFL Programming Concepts in Scientific Computing** course.




## Tools Used 🛠️
- **Programming Language**: C++
- **Build System**: CMake
- **IDE**: CLion
- **Version Control**: Git
- **Documentation**: Doxygen
- **Software Testing**: Googletest

## The 3 Key Takeaways 📊: 
- Planning the project structure and class design is essential for scalability and organization.
- Polymorphism plays a vital role in flexible and effective scientific computing.
- Writing modular and factorized code ensures reusability and long-term maintainability.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Installation](#installation)
    - [Cloning the repository](#cloning-the-repository)
    - [Building the executable](#building-the-executables)
4. [Usage](#usage)
    - [Input File Format](#input-file-format)
    - [Running the Program](#running-the-program)
5. [Code Structure](#code-structure)
6. [Methods Implemented](#methods-implemented)
    - [Power Method](#power-method)
    - [Inverse Power Method with Shift](#inverse-power-method-with-shift)
    - [QR Method](#qr-method)
7. [Documentation](#documentation)
8. [Limitations](#limitations)
9. [Contributing](#contributing)
10. [Acknowledgments](#acknowledgments)
11. [Support](#support)

---

## Project Overview
![image](https://github.com/user-attachments/assets/448a17ea-40f4-496c-9256-ddefe1ab4d88)


This repository implements three different methods to compute the eigenvalues of a matrix:
1. **Power Method**
2. **Inverse Power Method with Shift**
3. **QR Method**

The program reads matrix and parameter data from a user-defined control file, solves the eigenvalue problem,
and outputs the results to a file and the console.

---

## Features

- Supports **real** and **complex** matrices.
- Implements multiple numerical methods for eigenvalue computation.
- Provides flexible input format for specifying matrix and solver parameters.
- Modular design with clear separation of concerns across input, solver, and output functionalities.

---

## Installation

### Cloning the repository

Start by cloning the repository
```
git clone git@gitlab.epfl.ch:roy_selim/pcsc-project.git
```
Load Eigen and Google Test submodules
```
git submodule update --init --recursive
```

### Building the executables

Ensure CMake and a compatible C++ compiler are installed. Then

1. Create a build directory:
    ```
    mkdir build
    cd build
    ```
2. Generate the build files and build the project
    ```
    cmake ..
    make
    ```

This will create an executable named `pcsc_project` along with `pcsc_project_tests` for various tests.

---

## Usage

### Input File Format

The input file should define the following parameters

| **Parameter**  | **Description**                                   | **Choices/Format**                  | **Default**        |
|-----------------|---------------------------------------------------|--------------------------------------|--------------------|
| `MAX_ITER`     | Maximum number of iterations for the solver       | Positive integer                     | 500                |
| `TOLERANCE`    | Convergence tolerance                             | Floating-point number (0, 1]         | 1e-10             |
| `SHIFT`        | Shift value for the inverse power method          | Floating-point number                | 0.0                |
| `COMPLEX`      | Flag to indicate if the matrix is complex         | `0` (real), `1` (complex)            | 0                  |
| `METHOD`       | Numerical method to compute eigenvalues           | `qr`, `power`, `shift`               | `qr`               |
| `MATRIX_DATA`  | Matrix dimensions and values                      | Matrix must be square                | N/A                |

Below is an example of the input file when the matrix is **real**:

$$
A = \begin{pmatrix} 
1 & 2 & 3 \\
4 & 5 & 6 \\
7 & 8 & 9
\end{pmatrix}
$$

```
MAX_ITER 500
TOLERANCE 1e-10
SHIFT 0.5
COMPLEX 0 
METHOD shift
MATRIX_DATA
3 3
1.0 2.0 3.0
4.0 5.0 6.0
7.0 8.0 9.0
```

and when the matrix is **complex**:

$$
A = \begin{pmatrix} 
1+2i & -3+4i \\
i & -2+i
\end{pmatrix}
$$

```
MAX_ITER 500
TOLERANCE 1e-10
COMPLEX 1 
METHOD qr
MATRIX_DATA
2 2
1 2 -3 4
0 1 -2 1
```

### Running the Program

To use the program, start by modifying the `input.txt` file located outside the `build` directory to suit your requirements.
Then, execute the following command indicating the **correct** path for the input file
```
./pcsc_project ../input.txt
```
If you don't provide an argument, the program will ask you to specify the path to the input file.

Upon successful execution, the program will generate a `solver_output.txt` file in the `build` directory containing the solver's results.

---

## Code Structure

The project is organized into modular components:

- **`main.cpp`**: Entry point for the program. Handles argument parsing, input/output management, and solver execution.
- **`input.hpp` / `input.cpp`**: Defines the `Input` class for reading, validating, and managing input parameters and matrices.
- **`solver.hpp` / `solver_imp.hpp`**: Implements numerical methods for eigenvalue computation, including:
    - **Power Method**
    - **Inverse Power Method with Shift**
    - **QR Method**
- **`output.hpp` / `output_imp.hpp`**: Defines the `Output` class for output formatting, including:
    - Displaying the results in the console.
    - Saving results to a file.

---

## Methods Implemented

### Power Method

**Purpose**: Computes the dominant eigenvalue of a matrix $A$.

**How it works**:
- Starts with an initial guess vector of ones $x_{0}$.
- Repeatedly applies the matrix $A$ to the vector $x$, normalizing at each step
  $$x_{k+1} = \frac{A x_{k}}{\|A x_{k}\|}$$
- Estimates the eigenvalue at each iteration
  $$\lambda = x_{k}^{T}Ax_{k}$$
- Convergence is checked using
  $$\|Ax_{k} - \lambda x_{k}\| < \varepsilon$$

**Inputs**:
- Matrix $A$: Real or complex square matrix.
- Tolerance: Convergence threshold.
- Max iterations: Maximum allowed iterations.

**Output**:
- Dominant eigenvalue $\lambda$.

**Notes**:
- May struggle if the matrix does not have a unique dominant eigenvalue.

### Inverse Power Method with Shift

**Purpose**: Computes an eigenvalue close to a user-specified shift.

**How it works**:
- Starts with an initial guess vector of ones $x_{0}$.
- Modifies the matrix $A$ by applying a shift $\sigma$
  $$B = A - \sigma I$$
  where $I$ is the identity matrix.
- Solves the linear system iteratively
  $$Bx_{k+1} = x_{k}$$
- Estimates the eigenvalue at each iteration
  $$\lambda = x_{k}^{T}Ax_{k}$$
- Convergence is checked using
  $$\|Ax_{k} - \lambda x_{k}\| < \varepsilon$$

**Inputs**:
- Matrix $A$: Real or complex square matrix.
- Shift $\sigma$: Scalar value to target a specific eigenvalue.
- Tolerance: Convergence threshold.
- Max iterations: Maximum allowed iterations.

**Output**:
- Eigenvalue $\lambda$ near the shift $\sigma$

**Notes*:*
- Requires $A - \sigma I$ to be non-singular.
- Suitable for computing small eigenvalues or those near $\sigma$.

### QR Method

**Purpose**: Computes all eigenvalues of a matrix.

**How it works**:
- Starts with a matrix $A$ and iteratively performs QR decomposition
  $$A_{k} = Q_{k}R_{k}$$
  where $Q_{k}$ is an orthogonal matrix and $R_{k}$ is an upper triangular matrix.
- Updates the matrix
  $$A_{k+1} = R_{k}Q_{k}$$
- The process continues until $A_{k}$ becomes upper triangular, and the eigenvalues are the diagonal entries of $A_{k}$.

**Inputs**:
- Matrix $A$: Real or complex square matrix.
- Max iterations: Maximum allowed iterations.

**Output**:
- All eigenvalues as the diagonal elements of the triangular matrix.

**Notes**:
- Convergence depends on the matrix being reducible to triangular form.

---

## Documentation

The code is documented using Doxygen. You can access the generated documentation in either PDF or HTML format.

- **PDF documentation**: Navigate to ``docs/latex`` and open ``refman.pdf`` with your preferred PDF viewer. For example:

```
cd docs/latex
evince refman.pdf
```

- **HTML documentation**: Navigate to ``docs/html`` and open the ``index.html`` file in your web browser. For example:

```
cd docs/html
xdg-open index.html
```

---

## Limitations

The project has the following limitations:

1. Lack of control over the initial guess
    - In the Power Method and Inverse Power Method with Shift, the user does not have control over the initial guess vector $x_{0}$.
      The vector is internally generated, which might affect convergence rate for certain matrices.
2. Matrix and eigenvalue types
    - The code is designed to handle the following scenarios
        - Real matrices with real eigenvalues: fully supported.
        - Complex matrices: supports computation of eigenvalues of any type (real or complex).
          The implementation does **not** support real matrices with complex eigenvalues. This limitation exists because the methods assume
          that eigenvalues will be of the same type as the input matrix. For example, consider the rotation matrix
          $$
          A = \begin{pmatrix}1 & -1 \\ 1 & 1\end{pmatrix}
          $$. This matrix has eigenvalues $\lambda=1\pm i$. However, do to our aforementioned limitation,
          the current implementation cannot compute these eigenvalues.
3. Input format
    - The input file format is strict and must follow a specific structure. The matrix and the problem parameters are both
      implemented in a single control file.

---

## Contributing

Contributions are welcome! Please fork the repository, create a branch for your feature, and submit a pull request.

---

## Acknowledgments

We would like to express our gratitude to
- The **Eigen Library** community for simplifying life with the linear algebra framework.
- **ChatGPT-4o** for debugging purposes when necessary.

---

# Support

If you have any questions, feedback, or issues with the project, feel free to contact the authors!
- **Selim Sherif**: [selim.sherif@epfl.ch](mailto:selim.sherif@epfl.ch)
- **Roy Turk**: [roy.turk@epfl.ch](mailto:roy.turk@epfl.ch)

---

