import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import json

def parse_complex(val):
    if isinstance(val, (int, float)):
        return complex(val, 0)
    elif isinstance(val, str):
        return complex(val.replace(' ', ''))
    return complex(val)

def bloch_vector(state):
    alpha = parse_complex(state[0])
    beta = parse_complex(state[1])
    theta = 2 * np.arccos(np.abs(alpha))
    phi = np.angle(beta) - np.angle(alpha)
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return np.array([x, y, z])

def draw_bloch_sphere(ax, vector, title="", trajectory=None):
    u = np.linspace(0, 2 * np.pi, 20)
    v = np.linspace(0, np.pi, 20)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, color='cyan', alpha=0.3, linewidth=0, edgecolor='gray')
    
    ax.quiver(0, 0, 0, 1.5, 0, 0, color='red', arrow_length_ratio=0.1)
    ax.quiver(0, 0, 0, 0, 1.5, 0, color='green', arrow_length_ratio=0.1)
    ax.quiver(0, 0, 0, 0, 0, 1.5, color='blue', arrow_length_ratio=0.1)
    
    if trajectory is not None and len(trajectory) > 1:
        traj = np.array(trajectory)
        ax.plot(traj[:, 0], traj[:, 1], traj[:, 2], 'r-', linewidth=2, alpha=0.5)
    
    ax.quiver(0, 0, 0, vector[0], vector[1], vector[2], 
              color='black', linewidth=3, arrow_length_ratio=0.2)
    ax.scatter([vector[0]], [vector[1]], [vector[2]], color='black', s=50)
    
    ax.set_xlim([-1.2, 1.2])
    ax.set_ylim([-1.2, 1.2])
    ax.set_zlim([-1.2, 1.2])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)
    ax.set_aspect('equal')
    ax.view_init(elev=20, azim=30)

def draw_trajectory_multi(states, filename, title="Bloch Sphere Trajectory"):
    n = len(states)
    cols = min(4, n)
    rows = (n + cols - 1) // cols
    
    fig = plt.figure(figsize=(5*cols, 5*rows))
    
    trajectory = []
    for i, state in enumerate(states):
        vec = bloch_vector(state)
        trajectory.append(vec)
        
        ax = fig.add_subplot(rows, cols, i+1, projection='3d')
        draw_bloch_sphere(ax, vec, f"t={i}", trajectory.copy())
    
    fig.suptitle(title, fontsize=16)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"Saved: {filename}")

def draw_density_matrix_evolution(data, filename):
    qubits = data['qubits']
    dim = 2 ** qubits
    stages = data['stages']
    
    n = len(stages)
    cols = min(3, n)
    rows = (n + 1) // cols
    
    fig = plt.figure(figsize=(6*cols, 5*rows))
    
    for i, stage in enumerate(stages):
        state_vector = stage['state_vector']
        psi = np.array(state_vector, dtype=complex).reshape(-1, 1)
        rho = psi @ psi.conj().T
        
        ax = fig.add_subplot(rows, cols, i+1, projection='3d')
        
        xpos, ypos = np.meshgrid(range(dim), range(dim), indexing='ij')
        xpos, ypos = xpos.flatten(), ypos.flatten()
        zpos = np.zeros_like(xpos)
        dx = dy = 0.8 * np.ones_like(zpos)
        
        real_vals = np.real(rho).flatten()
        colors = ['red' if v >= 0 else 'blue' for v in real_vals]
        
        ax.bar3d(xpos, ypos, zpos, dx, dy, real_vals, color=colors, alpha=0.8)
        ax.set_title(stage.get('name', f'Stage {i+1}'))
        ax.set_xlabel('Row')
        ax.set_ylabel('Col')
        ax.set_xticks(range(dim))
        ax.set_yticks(range(dim))
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"Saved: {filename}")

def main(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    base_name = input_file.split('/')[-1].replace('.json', '')
    
    if 'trajectory' in data:
        states = [np.array(s) for s in data['trajectory']]
        draw_trajectory_multi(states, f"{base_name}_trajectory.png", data.get('name', 'Bloch Trajectory'))
    else:
        draw_density_matrix_evolution(data, f"{base_name}_evolution.png")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python dynamic_flow.py <input_json>")
        sys.exit(1)
    main(sys.argv[1])
