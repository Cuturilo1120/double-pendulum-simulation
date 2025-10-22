"""
Double Pendulum Animation Module
Usage:
    from pendulum_animator import animate_pendulum
    
    # Basic usage
    animate_pendulum('double_pendulum.csv')
    
    # With options
    animate_pendulum('double_pendulum.csv', 
                    interval=10, 
                    show_trail=True,
                    trail_length=500,
                    save_as='animation.gif')
"""

import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def load_data(filename):
    t, x1, y1, x2, y2 = [], [], [], [], []
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            t.append(float(row['time']))
            x1.append(float(row['x1']))
            y1.append(float(row['y1']))
            x2.append(float(row['x2']))
            y2.append(float(row['y2']))
    return t, x1, y1, x2, y2

def animate_pendulum(filename, interval=10, show_trail=True, trail_length=None, 
                    xlim=(-2, 2), ylim=(-2, 2), save_as=None, block=True):
    """
    Animate a double pendulum from CSV data
    
    Parameters:
    -----------
    filename : str
        Path to CSV file with columns: time, x1, y1, x2, y2
    interval : int, optional
        Delay between frames in milliseconds (default: 10)
    show_trail : bool, optional
        Whether to show the trail of the second pendulum (default: True)
    trail_length : int, optional
        Maximum number of points in trail. None for full trail (default: None)
    xlim : tuple, optional
        x-axis limits (default: (-2, 2))
    ylim : tuple, optional
        y-axis limits (default: (-2, 2))
    save_as : str, optional
        Filename to save animation (e.g., 'output.gif', 'output.mp4')
        If None, just displays animation (default: None)
    block : bool, optional
        Whether to block execution until window is closed (default: True)
    
    Returns:
    --------
    ani : FuncAnimation
        The animation object (in case you want to save it later)
    """
    # Load data
    t, x1, y1, x2, y2 = load_data(filename)
    print(f"Loaded {len(t)} frames from {filename}")
    
    # Setup figure
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'Double Pendulum: {filename}')
    
    # Create line objects
    line, = ax.plot([], [], 'o-', lw=2, markersize=8, color='royalblue')
    trace, = ax.plot([], [], '-', lw=1, alpha=0.5, color='red') if show_trail else (None,)
    
    # Trail storage
    trail_x, trail_y = [], []
    
    def init():
        line.set_data([], [])
        if show_trail:
            trace.set_data([], [])
            return line, trace
        return line,
    
    def update(i):
        # Update trail
        if show_trail:
            trail_x.append(x2[i])
            trail_y.append(y2[i])
            
            # Limit trail length if specified
            if trail_length is not None and len(trail_x) > trail_length:
                trail_x.pop(0)
                trail_y.pop(0)
            
            trace.set_data(trail_x, trail_y)
        
        # Update pendulum arms
        line.set_data([0, x1[i], x2[i]], [0, y1[i], y2[i]])
        
        if show_trail:
            return line, trace
        return line,
    
    # Create animation
    ani = FuncAnimation(fig, update, frames=len(t), init_func=init, 
                       blit=True, interval=interval, repeat=True)
    
    # Save or display
    if save_as:
        print(f"Saving animation to {save_as}...")
        ani.save(save_as, writer='pillow' if save_as.endswith('.gif') else 'ffmpeg')
        print("Animation saved!")
    
    if block or not save_as:
        plt.show(block=block)
        if not block:
            plt.pause(len(t) * interval / 1000)
            plt.close()
    
    return ani

# Allow running as script for testing
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'double_pendulum.csv'
    
    animate_pendulum(filename)