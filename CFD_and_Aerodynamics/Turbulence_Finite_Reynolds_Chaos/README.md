# Turbulence at Finite Reynolds Number and The Skeleton of Chaos

### Context:
Course Project for **ME-467: Turbulence**, taught by **Tobias Schneider** at **EPFL**, Department of Mechanical Engineering.

---

## Key Takeaways:
1. **Taylor's Frozen Flow Hypothesis Holds**: Valid for all three datasets since turbulence intensity `I ≪ 1`, allowing time series to be treated as spatial profiles.
2. **K41 Theory Works in the Inertial Range**: The `-5/3` energy spectrum slope, structure function scaling (`S2 ∝ ℓ^(2/3)`, `S3` 4/5-law), and dissipation rate estimates all agree closely across independent methods.
3. **Intermittency Breaks Self-Similarity**: Velocity increment PDFs get fatter tails at small scales, and flatness decays through the inertial range instead of staying constant.
4. **KSE as a Minimal Chaos Model**: The 1D Kuramoto-Sivashinsky equation reproduces sensitive dependence on initial conditions and a positive leading Lyapunov exponent.
5. **Equilibria + UPOs = Skeleton of Chaos**: Invariant equilibria and unstable periodic orbits, computed via Newton/recurrence methods, together organize the chaotic attractor.

---

## Tools Used:
- **Data**: Hot-wire anemometer velocity data, Warhaft Wind and Turbulence Tunnel, Cornell University.
- **Analysis**: MATLAB (spectral analysis, autocorrelation, structure functions, PDFs, Lyapunov exponents, Newton solvers for KSE equilibria/UPOs).
- **Report**: LaTeX.

---

## Overview
Two-part report:

**Part I — Finite Reynolds Number Effects in Turbulence**
Analyzes three grid-turbulence datasets under Taylor's hypothesis: mean velocity, correlation/integral length scales, energy spectrum vs. K41, Taylor microscale and Reynolds numbers, velocity increments, PDF statistics, structure functions, and flatness/intermittency.

**Part II — Chaos, its Skeleton, and Quantitative Characterization**
Uses the 1D KSE as a minimal chaos model: sensitivity to initial conditions, Lyapunov spectrum, equilibrium solutions, unstable periodic orbits, and their combined role as the attractor's invariant skeleton.

---

## Repository Structure
```
Turbulence_Finite_Reynolds_and_Skeleton_of_Chaos/
├── README.md
├── Turbulence_Project_Report.pdf   # Full report
├── EPFL_ME467_K42.zip              # Part I: finite-Reynolds-number turbulence analysis code
└── EPFL_ME467_Chaos_Theory.zip     # Part II: KSE chaos / equilibria / UPO analysis code
```
- **EPFL_ME467_K42.zip**: MATLAB functions and scripts, data, for Part I — autocorrelation, energy spectrum, structure functions, PDFs, and flatness analysis.
- **EPFL_ME467_Chaos_Theory.zip**: MATLAB functions and scripts for Part II — KSE integration, Lyapunov exponents, equilibrium and UPO solvers.

---

## References
1. Yoon, K., & Warhaft, Z. (1990). *The evolution of grid-generated turbulence under conditions of stable thermal stratification*. J. Fluid Mechanics.
2. Cvitanović, P., Davidchack, R. L., & Siminos, E. (2005). *On the state space geometry of the Kuramoto-Sivashinsky flow in a periodic domain*. J. Physics: Conf. Series, 23(1), 33-47.
3. Frisch, U. (1995). *Turbulence: The Legacy of A.N. Kolmogorov*. Cambridge University Press.
4. Pope, S. B. (2000). *Turbulent Flows*. Cambridge University Press.
5. Higgins, C., Froidevaux, M., & Simeonov, V. (2012). *The effect of scale on the applicability of Taylor's frozen turbulence hypothesis in the atmospheric boundary layer*. Boundary-Layer Meteorology.
6. Tong, C. (1996). *Taylor's hypothesis and two-point coherence measurements*. Boundary-Layer Meteorology.
7. CFD-Wiki Contributors. *Turbulence dissipation rate*. [Link](https://www.cfd-online.com/Wiki/Turbulence_dissipation_rate)
