# Double Pendulum Simulation

## Project Information

**Course name:** Napredne Tehnike Programiranja  
**Target Grade:** 6  

### Grade 6 Requirements

- Implement a **sequential version** of the chosen problem in Python.  
- Implement a **parallelized version** using the `multiprocessing` library in Python.  

---

## Chosen Topic: Double Pendulum Simulation

The **double pendulum** is a classic physics problem consisting of two pendulums connected end-to-end. Despite its simple structure, the system exhibits **complex, chaotic motion**, making it ideal for studying both physics and computational methods.

The motion of a double pendulum is governed by **non-linear coupled differential equations** derived from Newtonian mechanics:

Let:  
- `θ1, θ2` be the angles of the first and second pendulum (measured from vertical)  
- `ω1, ω2` be the angular velocities  
- `L1, L2` the lengths of the rods  
- `m1, m2` the masses  
- `g` the acceleration due to gravity  

The **angular accelerations** `α1, α2` are:

```text
num1 = -g*(2*m1+m2)*math.sin(theta1)
num2 = -m2*g*math.sin(theta1-2*theta2)
num3 = -2*math.sin(theta1-theta2)*m2*(omega2**2*L2 + omega1**2*L1*math.cos(theta1-theta2))
den = L1*(2*m1+m2 - m2*math.cos(2*theta1-2*theta2))
a1 = (num1+num2+num3)/den

num1 = 2*math.sin(theta1-theta2)
num2 = (omega1**2*L1*(m1+m2) + g*(m1+m2)*math.cos(theta1) + omega2**2*L2*m2*math.cos(theta1-theta2))
den = L2*(2*m1+m2 - m2*math.cos(2*theta1-2*theta2))
a2 = num1*num2/den
```

These accelerations are then used to **update angular velocities and angles** over time using **numerical integration methods**:

- **Euler’s Method (Sequential Version)**:

```text
θ_i^{t+Δt} = θ_i^t + ω_i^t Δt
ω_i^{t+Δt} = ω_i^t + α_i^t Δt
```

- **Runge-Kutta 4th Order (RK4, Higher Accuracy)**:

```text
θ_i^{t+Δt} = θ_i^t + (Δt/6) * (k1 + 2*k2 + 2*k3 + k4)
ω_i^{t+Δt} = ω_i^t + (Δt/6) * (k1 + 2*k2 + 2*k3 + k4)
θ_i^{t+Δt} = θ_i^t + (Δt/6) * (k1 + 2*k2 + 2*k3 + k4)
ω_i^{t+Δt} = ω_i^t + (Δt/6) * (k1 + 2*k2 + 2*k3 + k4)
```

## Implementation Overview
### Sequential Version

- Initialize pendulum parameters (L1, L2, m1, m2, g) and starting conditions (θ1, θ2, ω1, ω2).
- Compute accelerations using the formulas above.
- Integrate using Euler’s method or RK4 over a fixed number of steps.
- Store results (angles, velocities, positions) in a CSV file.
- Animate the motion using matplotlib, optionally showing the trail of the second pendulum.

### Parallel Version

- Multiple simulations run simultaneously with slightly different initial conditions (demonstrating sensitivity to initial conditions).
- Each simulation uses RK4 internally.
- Use Python’s multiprocessing.Pool to distribute simulations across available CPU cores.
- Store each simulation’s results in a separate CSV file.
- Animate all simulations together to visually compare trajectories.

## Key Features

- CSV Output: Stores time, angles, angular velocities, and Cartesian coordinates.
- Animation Module: Can display pendulum motion in real-time with trails.
- Parallel Execution: Demonstrates leveraging multi-core processors for independent simulations.
- RK4 vs Euler Comparison: Illustrates the effect of numerical method choice on simulation accuracy.
