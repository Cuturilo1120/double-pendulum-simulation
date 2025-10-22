#Euler

import math, csv
from pendulum_animator import animate_pendulum
#consts
g = 9.81
L1, L2 = 1.0, 1.0
m1, m2 = 1.0, 1.0
dt = 0.01
steps = 100000

theta1, theta2 = math.pi/2, math.pi/2
omega1, omega2 = 0.0, 0.0

with open('double_pendulum.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['time', 'theta1', 'theta2', 'omega1', 'omega2', 'x1', 'y1', 'x2', 'y2'])
    t = 0
    for _ in range(steps):
        num1 = -g*(2*m1+m2)*math.sin(theta1)
        num2 = -m2*g*math.sin(theta1-2*theta2)
        num3 = -2*math.sin(theta1-theta2)*m2*(omega2**2*L2 + omega1**2*L1*math.cos(theta1-theta2))
        den = L1*(2*m1+m2 - m2*math.cos(2*theta1-2*theta2))
        a1 = (num1+num2+num3)/den

        num1 = 2*math.sin(theta1-theta2)
        num2 = (omega1**2*L1*(m1+m2) + g*(m1+m2)*math.cos(theta1) + omega2**2*L2*m2*math.cos(theta1-theta2))
        den = L2*(2*m1+m2 - m2*math.cos(2*theta1-2*theta2))
        a2 = num1*num2/den

        omega1 += a1*dt
        omega2 += a2*dt
        theta1 += omega1*dt
        theta2 += omega2*dt

        x1, y1 = L1*math.sin(theta1), -L1*math.cos(theta1)
        x2, y2 = x1 + L2*math.sin(theta2), y1 - L2*math.cos(theta2)

        writer.writerow([t, theta1, theta2, omega1, omega2, x1, y1, x2, y2])
        t += dt
    animate_pendulum('double_pendulum.csv', 
                interval=1,           
                trail_length=500,     
                show_trail=True)