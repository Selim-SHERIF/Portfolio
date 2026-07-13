# Others

A collection of engineering and scientific computing projects spanning coursework, research, and extracurricular team projects — reflecting the range of my work across my M.Sc. in Computational Science and Engineering and my involvement in EPFL's student engineering teams.

---

## Projects

```
Others/
├── Scientific_Computing_Eigensolver
├── Caroms_Billiard_Game
├── High_Performance_Computing
├── Investments_Strategic_International_Asset_Allocation
├── Semester_Project_Isoparametric_boundary_conformal_layer_approximation
├── Structural_Design_Rocket_Team
└── Vehicle_Dynamics_Racing_Team
```

| Project | Description | Tools |
|---|---|---|
| [Eigenvalue Solver](./Scientific_Computing_Eigensolver) | A C++ eigenvalue solver library built for EPFL MATH-458, designed around polymorphic solver classes (power method, inverse power, QR) with full unit testing and Doxygen documentation. Focus on software quality: modularity, extensibility, and test coverage. | C++, CMake, GoogleTest, Doxygen |
| [Carom Billiard Simulator](./Caroms_Billiard_Game) | Physics simulation of carom billiards: elastic collisions, friction models, and trajectory generation with automated score-sheet output. | Python |
| [High-Performance Computing](./High_Performance_Computing) | Two MATH-454 course projects on MPI/CUDA parallelization: a Conjugate Gradient solver profiled and scaled with MPI, and a Shallow Water Equation solver extended from MPI to GPU acceleration with CUDA. Includes strong/weak scaling analysis against Amdahl's and Gustafson's laws. | MPI, CUDA, C++, perf |
| [Investments: Strategic International Asset Allocation](./Investments_Strategic_International_Asset_Allocation) | FIN-405 course project studying international diversification, currency hedging, and predictive signals (momentum, reversal, carry, dollar) across seven markets, culminating in a mean-variance optimized fund benchmarked against Fama-French factors. | Python, OLS regression |
| [Isoparametric Boundary Conformal Layers](./Semester_Project_Isoparametric_boundary_conformal_layer_approximation) | Semester project approximating composite spline mappings for trimmed-surface boundary layers with a single NURBS spline, including an h-p convergence study and a static structural analysis of the approximation's impact on simulation accuracy. | Isogeometric Analysis, NURBS/Splines |
| [Anti-Buckling Ring — EPFL Rocket Team](./Structural_Design_Rocket_Team) | CAD design of a structural ring reinforcing the carbon fiber load-bearing rods of the EPFL Rocket Team's bi-liquid rocket, developed through topology optimization and refined for CNC manufacturing. | SolidWorks, 3DEXPERIENCE |
| [Lap Time Simulator — EPFL Racing Team](./Vehicle_Dynamics_Racing_Team) | Modular Formula Student lap time simulator built around suspension, tire, driver, and vehicle-dynamics blocks, used for design validation and rapid iteration on car setup. *(Closed-source — overview only.)* | Simulink, Simscape, MATLAB |