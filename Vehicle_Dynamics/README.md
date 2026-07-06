# Vehicle Dynamics & Simulation

Vehicle-level modelling and simulation work, centred on the development of a Formula Student Lap Time Simulator for the EPFL Racing Team.

---

## Formula Student Lap Time Simulator — EPFL Racing Team

**Role:** Vehicle Dynamics Engineer (2024–2025)

The Lap Time Simulator (LTS) is the team's primary tool for data-driven design decisions: it predicts lap performance from vehicle parameters, allowing proposed design changes to be evaluated virtually before committing resources to manufacturing.

### Architecture

The simulator is built in MATLAB/Simulink using a modular, connective system-modelling approach:

- **Suspension model** — dynamic response under load transfer and track inputs
- **Tire model** — tire-road contact patch interaction, the dominant force-generating mechanism and the most complex subsystem
- **Driver model** — trajectory and control input generation around the track
- **Vehicle dynamics core** — conservation laws applied at vehicle level (velocity-yaw formulation)

### Key engineering challenges

- Numerical stability of the coupled system near the limits of tire adhesion
- Balancing model fidelity against simulation runtime for rapid design iteration
- Validation against on-track telemetry data

### Applications

Design trade-off evaluation, rapid assessment of setup changes, and the foundation for a future driver-in-the-loop digital twin.

> **Note:** The simulator codebase is property of the EPFL Racing Team and is closed-source. This overview describes the architecture and my contributions; I am happy to discuss the technical details directly.

*Tools: MATLAB, Simulink, Simscape*
