import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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

def draw_bloch_sphere(ax, vector, title=""):
    u = np.linspace(0, 2 * np.pi, 20)
    v = np.linspace(0, np.pi, 20)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, color='cyan', alpha=0.3, linewidth=0, edgecolor='gray')
    ax.quiver(0, 0, 0, 1.5, 0, 0, color='red', arrow_length_ratio=0.1)
    ax.quiver(0, 0, 0, 0, 1.5, 0, color='green', arrow_length_ratio=0.1)
    ax.quiver(0, 0, 0, 0, 0, 1.5, color='blue', arrow_length_ratio=0.1)
    ax.quiver(0, 0, 0, vector[0], vector[1], vector[2], 
              color='black', linewidth=3, arrow_length_ratio=0.2)
    ax.scatter([vector[0]], [vector[1]], [vector[2]], color='black', s=50)
    ax.set_xlim([-1.2, 1.2])
    ax.set_ylim([-1.2, 1.2])
    ax.set_zlim([-1.2, 1.2])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title, fontsize=10)
    ax.set_aspect('equal')
    ax.view_init(elev=20, azim=30)

def draw_density_matrix(ax, state_vector, title=""):
    psi = np.array([parse_complex(s) for s in state_vector], dtype=complex).reshape(-1, 1)
    rho = psi @ psi.conj().T
    dim = rho.shape[0]
    xpos, ypos = np.meshgrid(range(dim), range(dim), indexing='ij')
    xpos, ypos = xpos.flatten(), ypos.flatten()
    zpos = np.zeros_like(xpos)
    dx = dy = 0.8 * np.ones_like(zpos)
    real_vals = np.real(rho).flatten()
    colors = ['red' if v >= 0 else 'blue' for v in real_vals]
    ax.bar3d(xpos, ypos, zpos, dx, dy, real_vals, color=colors, alpha=0.8)
    ax.set_title(title, fontsize=10)
    ax.set_xlabel('Row')
    ax.set_ylabel('Col')
    ax.set_xticks(range(dim))
    ax.set_yticks(range(dim))

def state_to_density(state_vector):
    psi = np.array([parse_complex(s) for s in state_vector], dtype=complex).reshape(-1, 1)
    return psi @ psi.conj().T

def grover_comparison():
    fig = plt.figure(figsize=(16, 10))
    fig.suptitle("Grover's Search: Visualization Comparison (Oracle-based Algorithm)", fontsize=14, fontweight='bold')
    
    with open('State_City_Visualization/algs/amplitude-dampening-algs/grover-search/grover_2qubit.json', 'r') as f:
        data = json.load(f)
    
    stages = data['stages']
    labels = ['Initial |00>', 'After H', 'After Oracle', 'After Diffusion']
    
    for i, (stage, label) in enumerate(zip(stages, labels)):
        psi = np.array([parse_complex(s) for s in stage['state_vector']], dtype=complex)
        
        ax_bloch = fig.add_subplot(3, 4, i+1, projection='3d')
        if len(psi) == 4:
            vec = np.array([0, 0, 1])
        else:
            vec = bloch_vector([psi[0], psi[1]])
        draw_bloch_sphere(ax_bloch, vec, f'Bloch: {label}')
        
        ax_city = fig.add_subplot(3, 4, i+5, projection='3d')
        rho = state_to_density(stage['state_vector'])
        draw_density_matrix(ax_city, stage['state_vector'], f'State City: {label}')
        
        probs = np.abs(psi) ** 2
        ax_prob = fig.add_subplot(3, 4, i+9)
        basis = [f'|{j:0{int(np.log2(len(psi)))}b}>' for j in range(len(psi))]
        bars = ax_prob.bar(range(len(probs)), probs, color='steelblue')
        ax_prob.set_xticks(range(len(probs)))
        ax_prob.set_xticklabels(basis, rotation=45, fontsize=8)
        ax_prob.set_ylabel('Probability')
        ax_prob.set_title(f'Probability: {label}', fontsize=10)
        ax_prob.set_ylim(0, 1.1)
    
    plt.tight_layout()
    plt.savefig('comparison_grover.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: comparison_grover.png")

def qft_comparison():
    fig = plt.figure(figsize=(14, 8))
    fig.suptitle("QFT: Visualization Comparison (Transform-based Algorithm)", fontsize=14, fontweight='bold')
    
    with open('State_City_Visualization/algs/tranform-based-algs/Quantum_Fourier_Transform/qft_2qubit.json', 'r') as f:
        data = json.load(f)
    
    stages = data['stages']
    labels = ['Initial |01>', 'After QFT']
    
    for i, (stage, label) in enumerate(zip(stages, labels)):
        psi = np.array([parse_complex(s) for s in stage['state_vector']], dtype=complex)
        
        ax_bloch = fig.add_subplot(2, 3, i+1, projection='3d')
        vec = bloch_vector([psi[0], psi[1]])
        draw_bloch_sphere(ax_bloch, vec, f'Bloch: {label}')
        
        ax_city = fig.add_subplot(2, 3, i+4, projection='3d')
        draw_density_matrix(ax_city, stage['state_vector'], f'State City: {label}')
    
    plt.tight_layout()
    plt.savefig('comparison_qft.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: comparison_qft.png")

def qaoa_comparison():
    fig = plt.figure(figsize=(16, 10))
    fig.suptitle("QAOA: Visualization Comparison (Variational Algorithm)", fontsize=14, fontweight='bold')
    
    with open('State_City_Visualization/algs/variational-algs/QAOA/qaoa_2qubit.json', 'r') as f:
        data = json.load(f)
    
    stages = data['stages']
    
    for i, stage in enumerate(stages):
        psi = np.array([parse_complex(s) for s in stage['state_vector']], dtype=complex)
        
        ax_city = fig.add_subplot(2, 4, i+1, projection='3d')
        draw_density_matrix(ax_city, stage['state_vector'], stage['name'])
    
    cost_x = np.linspace(0, 1, 50)
    cost_y = np.linspace(0, 1, 50)
    X, Y = np.meshgrid(cost_x, cost_y)
    Z = 0.5 + 0.3 * np.sin(2*X) * np.cos(2*Y) + 0.2 * np.cos(4*X)
    
    ax_cost = fig.add_subplot(2, 4, 5)
    contour = ax_cost.contourf(X, Y, Z, levels=15, cmap='viridis')
    ax_cost.set_xlabel('gamma')
    ax_cost.set_ylabel('beta')
    ax_cost.set_title('Cost Landscape')
    
    ax_cost2 = fig.add_subplot(2, 4, 6)
    ax_cost2.contourf(X, Y, Z, levels=15, cmap='viridis')
    ax_cost2.scatter([0.8], [0.6], color='red', s=100, marker='*', label='Optimum')
    ax_cost2.legend()
    ax_cost2.set_xlabel('gamma')
    ax_cost2.set_ylabel('beta')
    ax_cost2.set_title('With Optimum')
    
    ax_params = fig.add_subplot(2, 4, 7)
    iterations = range(len(stages))
    gamma_vals = [0.5, 0.5, 0.8, 1.0][:len(stages)]
    beta_vals = [0.3, 0.3, 0.6, 0.8][:len(stages)]
    ax_params.plot(iterations, gamma_vals, 'b-o', label='gamma')
    ax_params.plot(iterations, beta_vals, 'r-s', label='beta')
    ax_params.set_xlabel('Iteration')
    ax_params.set_ylabel('Parameter Value')
    ax_params.set_title('Parameter Evolution')
    ax_params.legend()
    
    plt.tight_layout()
    plt.savefig('comparison_qaoa.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: comparison_qaoa.png")

def simulation_comparison():
    fig = plt.figure(figsize=(16, 10))
    fig.suptitle("Rabi Oscillation: Visualization Comparison (Simulation-based)", fontsize=14, fontweight='bold')
    
    states = [
        ([1, 0], 't=0: |0>'),
        ([0.707, 0.707], 't=pi/4: |+>'),
        ([0, 1], 't=pi/2: |1>'),
        ([-0.707, 0.707], 't=3pi/4: |->'),
        ([-1, 0], 't=pi: -|0>')
    ]
    
    time_points = np.linspace(0, np.pi, 100)
    z_values = np.cos(time_points)
    
    for i, (state, label) in enumerate(states):
        ax_bloch = fig.add_subplot(2, 5, i+1, projection='3d')
        vec = bloch_vector(state)
        draw_bloch_sphere(ax_bloch, vec, label)
    
    ax_trajectory = fig.add_subplot(2, 5, (6, 10))
    theta = np.linspace(0, np.pi, 100)
    z_traj = np.cos(theta)
    ax_trajectory.plot(theta, z_traj, 'b-', linewidth=2)
    ax_trajectory.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax_trajectory.scatter([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi], 
                          [1, 0.707, 0, -0.707, -1], 
                          color='red', s=100, zorder=5, label='Measured points')
    ax_trajectory.set_xlabel('Time (radians)')
    ax_trajectory.set_ylabel('Z (Bloch)')
    ax_trajectory.set_title('Trajectory: Z vs Time')
    ax_trajectory.legend()
    ax_trajectory.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('comparison_simulation.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: comparison_simulation.png")

def main():
    print("Generating side-by-side comparison images...")
    grover_comparison()
    qft_comparison()
    qaoa_comparison()
    simulation_comparison()
    print("All comparisons saved!")

if __name__ == '__main__':
    main()
