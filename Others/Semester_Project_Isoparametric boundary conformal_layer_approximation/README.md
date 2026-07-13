# Isoparametric Boundary Conformal Layers for Trimmed Surfaces

### Context:
CSE Master Semester Project at **EPFL**, Chair of Numerical Modelling and Simulation.

---

## Key Takeaways:
1. **Composite Spline Maps Can Be Approximated by a Single Spline**: A standard NURBS approximation of the composed boundary-layer mapping closely matches theoretical convergence rates, without sacrificing much accuracy.
2. **Convergence is Governed by the Weaker of the Two Maps**: Approximation error scales with the minimum regularity of the base and auxiliary spline degrees, as predicted by isogeometric theory.
3. **Boundary Errors Behave Less Predictably**: Unlike the smooth global convergence trends, errors along the trimmed boundary curves show irregular, case-dependent patterns tied to two recurring spatial error "modes."
4. **The Approximation Barely Affects Real Simulations**: A static structural analysis shows the projected geometry produces displacement fields nearly indistinguishable from the exact composed geometry, especially under realistic mesh resolutions.
5. **Practical Payoff**: Replacing expensive composite mappings with simple splines offers a computationally efficient, accurate-enough alternative for CAD, FEM, and isogeometric simulation workflows.

---

## Tools Used:
- **Geometry & Analysis**: Spline/NURBS-based isogeometric methods, L2-projection, h-p convergence studies
- **Simulation**: Linear static shell analysis (Kirchhoff-Love / isogeometric)
- **Report**: LaTeX

---

## Overview
The project investigates whether the composite mapping used in the Immersed Boundary Conformal Method (IBCM) to build boundary-conformal layers on trimmed surfaces can be replaced by a single, standard spline. It covers:
- The domain/mapping setup (auxiliary, parametric, and physical spaces).
- L2-projection of the composite map onto a spline space.
- An h-p convergence study on a saddle-shaped benchmark surface, comparing empirical error rates to theoretical predictions.
- A static structural analysis comparing simulation results between the exact and approximated geometries.
- A supplementary study of recurring spatial error patterns ("modes") in the pointwise projection error.

---

## Repository Structure
```
Isoparametric_Boundary_Conformal_Layers/
├── README.md
└── Isoparametric_Boundary_Conformal_Layers_Report.pdf
```