import math
import csv
from multiprocessing import Pool, cpu_count
import glob
from multiple_animate import animate_multiple_pendulums

g = 9.81
L1, L2 = 1.0, 1.0
m1, m2 = 1.0, 1.0
dt = 0.01
steps = 100000

def derivatives(theta1, theta2, omega1, omega2):
    num1 = -g*(2*m1+m2)*math.sin(theta1)
    num2 = -m2*g*math.sin(theta1-2*theta2)
    num3 = -2*math.sin(theta1-theta2)*m2*(omega2**2*L2 + omega1**2*L1*math.cos(theta1-theta2))
    den = L1*(2*m1+m2 - m2*math.cos(2*theta1-2*theta2))
    a1 = (num1+num2+num3)/den

    num1 = 2*math.sin(theta1-theta2)
    num2 = (omega1**2*L1*(m1+m2) + g*(m1+m2)*math.cos(theta1) + omega2**2*L2*m2*math.cos(theta1-theta2))
    den = L2*(2*m1+m2 - m2*math.cos(2*theta1-2*theta2))
    a2 = num1*num2/den
    
    return omega1, omega2, a1, a2

def run_simulation(params):
    """Run a single simulation with given initial conditions"""
    sim_id, theta1_init, theta2_init, omega1_init, omega2_init = params
    
    theta1, theta2 = theta1_init, theta2_init
    omega1, omega2 = omega1_init, omega2_init
    
    results = []
    t = 0
    
    for _ in range(steps):
        # RK4 integration
        k1_theta1, k1_theta2, k1_omega1, k1_omega2 = derivatives(theta1, theta2, omega1, omega2)
        
        k2_theta1, k2_theta2, k2_omega1, k2_omega2 = derivatives(
            theta1 + 0.5*dt*k1_theta1,
            theta2 + 0.5*dt*k1_theta2,
            omega1 + 0.5*dt*k1_omega1,
            omega2 + 0.5*dt*k1_omega2
        )
        
        k3_theta1, k3_theta2, k3_omega1, k3_omega2 = derivatives(
            theta1 + 0.5*dt*k2_theta1,
            theta2 + 0.5*dt*k2_theta2,
            omega1 + 0.5*dt*k2_omega1,
            omega2 + 0.5*dt*k2_omega2
        )
        
        k4_theta1, k4_theta2, k4_omega1, k4_omega2 = derivatives(
            theta1 + dt*k3_theta1,
            theta2 + dt*k3_theta2,
            omega1 + dt*k3_omega1,
            omega2 + dt*k3_omega2
        )
        
        # Update state variables
        theta1 += (dt/6)*(k1_theta1 + 2*k2_theta1 + 2*k3_theta1 + k4_theta1)
        theta2 += (dt/6)*(k1_theta2 + 2*k2_theta2 + 2*k3_theta2 + k4_theta2)
        omega1 += (dt/6)*(k1_omega1 + 2*k2_omega1 + 2*k3_omega1 + k4_omega1)
        omega2 += (dt/6)*(k1_omega2 + 2*k2_omega2 + 2*k3_omega2 + k4_omega2)

        x1, y1 = L1*math.sin(theta1), -L1*math.cos(theta1)
        x2, y2 = x1 + L2*math.sin(theta2), y1 - L2*math.cos(theta2)

        results.append([t, theta1, theta2, omega1, omega2, x1, y1, x2, y2])
        t += dt
    
    return sim_id, results

if __name__ == '__main__':
    initial_conditions = [
        (0, math.pi/2, math.pi/2, 0.0, 0.0),      # Original
        (1, math.pi/2 + 0.01, math.pi/2, 0.0, 0.0),  # Small perturbation
        (2, math.pi/3, math.pi/3, 0.0, 0.0),      # Different angles
        (3, math.pi/4, math.pi/2, 0.0, 0.0),      # Different angles
        (4, math.pi/2, math.pi/2, 0.1, 0.0),      # With initial velocity
    ]
    
    # Use all available CPU cores
    num_processes = cpu_count()
    print(f"Running {len(initial_conditions)} simulations on {num_processes} cores...")
    
    # Run simulations in parallel
    with Pool(processes=num_processes) as pool:
        all_results = pool.map(run_simulation, initial_conditions)
    
    # Write results to separate CSV files
    for sim_id, results in all_results:
        filename = f'double_pendulum_sim_{sim_id}.csv'
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['time', 'theta1', 'theta2', 'omega1', 'omega2', 'x1', 'y1', 'x2', 'y2'])
            writer.writerows(results)
        print(f"Completed simulation {sim_id} -> {filename}")
    
    print("All simulations complete!")


    files = sorted(glob.glob("double_pendulum_sim_*.csv"))
    print(f"Found {len(files)} simulation files: {files}")

    # Animate them all
    animate_multiple_pendulums(
        files,
        colors=None,          
        show_trail=True,
        trail_length=300,
        interval=1,
        save_as=None,         
        block=True
    )