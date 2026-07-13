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
└── Turbulence_Project_Report.pdf   # Full report
```

---