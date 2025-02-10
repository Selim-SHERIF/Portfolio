# Numerical Flow Simulation of Ground Effect on an Airfoil ✈️

### Context
This project was completed as part of the **EPFL ME-474: Numerical Flow Simulation** course. The study explores the aerodynamic performance of a NACA 4417 airfoil in proximity to the ground, focusing on the effects of ground distance on lift and drag coefficients.

---

## Tools Used 🛠️
- **Software:** ANSYS Fluent, SpaceClaim, ANSYS Workbench
- **Post-Processing:** ANSYS Fluent visualization tools
- **Report Documentation:** LaTeX

---

## The 3 Key Takeaways 📊
- **Automated Simulation Workflows:** Automating simulation processes can be highly beneficial, streamlining tasks and reducing manual errors.
- **FLUENT as a Black Box:** While Ansys produces reliable outputs, it operates as a “black box,” meaning the underlying processes and computations remain hidden.
- **Ground Effect on Lift:** The lift increase due to ground effect is minimal for typical aircraft wings; noticeable differences only occur when the aircraft is extremely close to the ground.

## Table of Contents 📑

1. [Project Objectives](#project-objectives)
2. [Approach and Methodology](#approach-and-methodology)
3. [Results and Insights](#results-and-insights)
4. [Conclusion](#conclusion)
5. [Future Work](#future-work)
6. [References](#references)

---

## Project Objectives

1. Analyze how ground proximity influences aerodynamic characteristics such as lift and drag.
2. Evaluate the effects of different height-to-chord ratios ($h/c$) and angles of attack ($\alpha = 4^\circ$ and $\alpha = 6^\circ$).
3. Validate numerical results against experimental and theoretical data.

---

## Approach and Methodology

1. **Geometry and Computational Domain:**
    - Modeled the NACA 4417 airfoil with a chord length of 1 meter.
    - Investigated height-to-chord ratios ($h/c$) ranging from 0.1 to 1.0.

2. **Physical and Numerical Modeling:**
    - Assumed incompressible, isothermal, and Newtonian fluid behavior.
    - Applied the $k-\omega$ turbulence model for resolving near-wall effects.
    - Simulations conducted using steady-state conditions in ANSYS Fluent.

3. **Mesh Design and Convergence Study:**
    - Hybrid meshing approach: structured grids for uniform flow regions and unstructured grids near the airfoil for resolving gradients.
    - Convergence study with six progressively refined meshes to ensure accuracy.

---

## Results and Insights

1. **Aerodynamic Characteristics:**
    - Lift coefficient ($C_L$) increased as $h/c$ decreased, emphasizing stronger ground effects at lower heights.
    - Drag coefficient ($C_D$) decreased near the ground, reflecting improved aerodynamic efficiency.

2. **Flow Field Analysis:**
    - Pressure contours revealed significant pressure differentials between the airfoil surfaces.
    - Velocity contours highlighted accelerated flow over the upper surface and wake structures downstream.

3. **Validation:**
    - The results aligned with experimental studies on similar airfoils, confirming the reliability of the numerical simulations.

---

## Conclusion

This study effectively demonstrated the impact of ground proximity on airfoil performance, offering insights for the design of low-altitude aircraft and ground-effect vehicles. The systematic mesh refinement ensured accurate results, highlighting the critical role of numerical validation in aerodynamic simulations.

---


## References

1. Visser, M. "I-DPCN at Work." Published under CC BY-SA 2.0 terms. Available: [commons.wikimedia.org](https://commons.wikimedia.org)
2. Lednicer, D. "The Incomplete Guide to Airfoil Usage." University of Illinois at Urbana-Champaign. Available: [m-selig.ae.illinois.edu](https://m-selig.ae.illinois.edu)
3. Win, S.Y., & Thianwiboon, M. "Parametric Optimization of NACA 4412 Airfoil in Ground Effect." _Engineering Journal_, 25(12), 2021.
4. Fluid Mechanics 101. "Inflation Layer Calculator." Available: [fluidmechanics101.com](https://www.fluidmechanics101.com)
5. Ahmed, M.R., Takasaki, T., & Kohama, Y. "Aerodynamics of a NACA 4412 Airfoil in Ground Effect." _AIAA Journal_, 45(1), 2007.

---

## Authors 👨‍🔬
- **Teo HALEVI**
- **Selim SHERIF**
- **Roy TURK**
- **Jan ZGRAGGEN**

For further details or inquiries, feel free to [contact me](../../README.md#contact)
