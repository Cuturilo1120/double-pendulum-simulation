"""
Multi-Pendulum Animation Module
Usage:
    from multi_pendulum_animator import animate_multiple_pendulums

    animate_multiple_pendulums(
        ['pendulum1.csv', 'pendulum2.csv'],
        colors=['royalblue', 'orange'],
        labels=['Pendulum A', 'Pendulum B'],
        interval=10,
        show_trail=True,
        trail_length=400
    )
"""

import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import itertools

def load_data(filename):
    """Load CSV data for one pendulum."""
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

def animate_multiple_pendulums(
    filenames,
    interval=10,
    show_trail=True,
    trail_length=None,
    colors=None,
    labels=None,
    xlim=(-2, 2),
    ylim=(-2, 2),
    save_as=None,
    block=True
):
    """Animate multiple double pendulums from multiple CSV files."""
    
    if not isinstance(filenames, (list, tuple)):
        raise ValueError("filenames must be a list of CSV paths")
    
    datasets = [load_data(f) for f in filenames]
    print(f"Loaded {len(datasets)} pendulums from {len(filenames)} files.")
    
    # Determine total frames = shortest dataset
    total_frames = min(len(t) for t, *_ in datasets)
    
    # Auto-generate colors if not provided
    default_colors = itertools.cycle(['royalblue', 'tomato', 'limegreen', 'orange', 'purple'])
    if colors is None:
        colors = [next(default_colors) for _ in datasets]
    
    # Setup figure
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Multi Double Pendulum Simulation')
    
    # Create pendulum arms and traces
    lines, traces, trails = [], [], []
    for i, (color, data) in enumerate(zip(colors, datasets)):
        line, = ax.plot([], [], 'o-', lw=2, markersize=6, color=color, label=(labels[i] if labels else None))
        trace, = ax.plot([], [], '-', lw=1, alpha=0.5, color=color) if show_trail else (None,)
        lines.append(line)
        traces.append(trace)
        trails.append(([], []))
    
    if labels:
        ax.legend()
    
    def init():
        for line in lines:
            line.set_data([], [])
        if show_trail:
            for trace in traces:
                if trace: trace.set_data([], [])
        return [*lines, *[t for t in traces if t]]
    
    def update(frame):
        artists = []
        for i, (t, x1, y1, x2, y2) in enumerate(datasets):
            x1v, y1v, x2v, y2v = x1[frame], y1[frame], x2[frame], y2[frame]
            line = lines[i]
            line.set_data([0, x1v, x2v], [0, y1v, y2v])
            artists.append(line)
            
            if show_trail:
                tx, ty = trails[i]
                tx.append(x2v)
                ty.append(y2v)
                if trail_length and len(tx) > trail_length:
                    tx.pop(0)
                    ty.pop(0)
                trace = traces[i]
                if trace:
                    trace.set_data(tx, ty)
                    artists.append(trace)
        
        return artists
    
    ani = FuncAnimation(
        fig, update, frames=total_frames, init_func=init,
        blit=True, interval=interval, repeat=True
    )
    
    if save_as:
        print(f"Saving animation to {save_as}...")
        ani.save(save_as, writer='pillow' if save_as.endswith('.gif') else 'ffmpeg')
        print("Animation saved!")
    
    if block or not save_as:
        plt.show(block=block)
    
    return ani

# Allow running as a standalone script
if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python multi_pendulum_animator.py file1.csv file2.csv ...")
        sys.exit(1)
    animate_multiple_pendulums(sys.argv[1:])
