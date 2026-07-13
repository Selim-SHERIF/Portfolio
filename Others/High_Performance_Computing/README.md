# MPI/CUDA Parallelization of Iterative Solvers

### Context:
Two course projects for **MATH-454: Parallel and High-Performance Computing** at **EPFL**, Department of Mathematics.

---

## Key Takeaways:
1. **Profile Before Parallelizing**: In both projects, `perf`-based profiling identified a single dominant routine (`Mat_vec` for CG, `Compute_kernel` for SWE) as the clear target for acceleration.
2. **Strong Scaling Follows Amdahl's Law**: Measured speedups track Amdahl's Law closely given the profiled parallel fraction (`P ≈ 0.87` for CG, `P ≈ 0.96` for SWE).
3. **Weak Scaling Exposes Communication Costs**: Both solvers show weak scaling efficiency degrading with core count, driven by `MPI_Allreduce` and halo-exchange overhead rather than compute.
4. **GPU Acceleration Adds Further Speedup**: The CUDA version of the SWE solver plateaus in performance once thread blocks are large enough (TPB > 16) to fully occupy the GPU's SMs.

---

## Tools Used:
- **Profiling**: `perf`
- **Parallelization**: MPI (both projects), CUDA (SWE solver)
- **Report**: LaTeX

---

## Projects

### 1. MPI Parallelization of the Conjugate Gradient Algorithm
Parallelizes the CG method for solving large sparse linear systems. The matrix-vector product (`Mat_vec`) is distributed across ranks with `MPI_Allreduce` combining partial sums. Strong scaling matches Amdahl's Law (`P = 0.8692`); weak scaling reveals poor efficiency at higher core counts due to `MPI_Allreduce` and the low communication-to-computation ratio of the tridiagonal Laplace matrix.

### 2. MPI and CUDA Parallelization of a Shallow Water Equation (SWE) Solver
Extends a CPU-based SWE solver (MPI, row-wise domain decomposition, halo exchange, CFL enforcement via `MPI_Allreduce`) to a GPU-accelerated CUDA version (one thread per grid cell). Strong scaling is excellent across grid sizes (`P ≈ 0.96`); weak scaling follows a communication-limited `1/√ν` trend. CUDA performance plateaus beyond 16 threads per block.

---

## Repository Structure
```
MATH454_Parallel_HPC_Projects/
├── README.md
├── MPI_Conjugate_Gradient_Report.pdf
└── MPI_CUDA_SWE_Solver_Report.pdf
```