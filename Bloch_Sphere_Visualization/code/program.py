import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import re
import sys
import os

# ------------------------- Parser Functions -------------------------

def parse_ket(s):
    """Convert a ket string like |0>, |+>, ... to Bloch vector."""
    s = s.strip().lower()
    if s == '|0>':
        return np.array([0, 0, 1])
    elif s == '|1>':
        return np.array([0, 0, -1])
    elif s == '|+>':
        return np.array([1, 0, 0])
    elif s == '|->':
        return np.array([-1, 0, 0])
    elif s == '|+i>':
        return np.array([0, 1, 0])
    elif s == '|-i>':
        return np.array([0, -1, 0])
    else:
        raise ValueError(f"Unknown ket: {s}")

def parse_complex_pair(s):
    """Parse a string like (a+bi, c+di) into a normalized Bloch vector."""
    # Remove parentheses and split
    s = s.strip().strip('()')
    parts = s.split(',')
    if len(parts) != 2:
        raise ValueError("Complex pair must have exactly two entries")
    # Convert each part to complex number
    def to_complex(t):
        t = t.strip().replace(' ', '')
        # Handle pure real or pure imaginary
        if 'i' in t:
            if t == 'i':
                return 1j
            elif t == '-i':
                return -1j
            else:
                return complex(t.replace('i', 'j'))
        else:
            return complex(float(t), 0)
    alpha = to_complex(parts[0])
    beta = to_complex(parts[1])
    # Normalize
    norm = np.sqrt(abs(alpha)**2 + abs(beta)**2)
    if norm == 0:
        raise ValueError("State vector cannot be zero")
    alpha /= norm
    beta /= norm
    # Compute Bloch angles
    theta = 2 * np.arccos(np.abs(alpha))
    phi = np.angle(beta) - np.angle(alpha)
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return np.array([x, y, z])

def parse_angles(s):
    """Parse a string like theta=1.047, phi=0.785 (radians) or theta=60 deg, phi=45 deg."""
    # Extract theta and phi values
    theta_match = re.search(r'theta\s*=\s*([0-9.-]+)(?:\s*deg)?', s, re.I)
    phi_match = re.search(r'phi\s*=\s*([0-9.-]+)(?:\s*deg)?', s, re.I)
    if not theta_match or not phi_match:
        raise ValueError("Angle specification must contain theta and phi")
    theta = float(theta_match.group(1))
    phi = float(phi_match.group(1))
    # Convert to radians if 'deg' present
    if 'deg' in s.lower():
        theta = np.radians(theta)
        phi = np.radians(phi)
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return np.array([x, y, z])

def parse_bloch_vector(s):
    """Parse a string like (x,y,z) into a Bloch vector."""
    s = s.strip().strip('()')
    parts = s.split(',')
    if len(parts) != 3:
        raise ValueError("Bloch vector must have three coordinates")
    vec = np.array([float(p.strip()) for p in parts])
    # Normalize (in case it's not unit)
    norm = np.linalg.norm(vec)
    if norm > 1e-12:
        vec /= norm
    else:
        raise ValueError("Bloch vector too close to zero")
    return vec

def parse_stage(line):
    """Parse a single line describing a stage into a Bloch vector."""
    line = line.strip()
    if not line or line.startswith('#'):
        return None
    # Try each format in order
    try:
        if line.startswith('|') and '>' in line:
            return parse_ket(line)
    except:
        pass
    try:
        if 'theta' in line.lower() and 'phi' in line.lower():
            return parse_angles(line)
    except:
        pass
    try:
        if line.count('(') == 1 and line.count(')') == 1 and line.count(',') == 2:
            return parse_bloch_vector(line)
    except:
        pass
    try:
        if '(' in line and ')' in line and line.count(',') == 1:
            return parse_complex_pair(line)
    except:
        pass
    raise ValueError(f"Unable to parse line: {line}")

# ------------------------- Bloch Sphere Plotting -------------------------

def draw_bloch_sphere(ax, vector, title=""):
    """Draw a Bloch sphere on the given 3D axes with the state vector."""
    # Sphere surface
    u = np.linspace(0, 2 * np.pi, 20)
    v = np.linspace(0, np.pi, 20)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, color='cyan', alpha=0.3, linewidth=0, edgecolor='gray')

    # Coordinate axes
    ax.quiver(0, 0, 0, 1.5, 0, 0, color='red', arrow_length_ratio=0.1)
    ax.quiver(0, 0, 0, 0, 1.5, 0, color='green', arrow_length_ratio=0.1)
    ax.quiver(0, 0, 0, 0, 0, 1.5, color='blue', arrow_length_ratio=0.1)

    # State vector
    ax.quiver(0, 0, 0, vector[0], vector[1], vector[2], 
              color='black', linewidth=3, arrow_length_ratio=0.2)

    # Mark the tip with a point
    ax.scatter([vector[0]], [vector[1]], [vector[2]], color='black', s=50)

    # Labels and appearance
    ax.set_xlim([-1.2, 1.2])
    ax.set_ylim([-1.2, 1.2])
    ax.set_zlim([-1.2, 1.2])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)
    ax.set_aspect('equal')
    ax.view_init(elev=20, azim=30)

# ------------------------- Main Program -------------------------

def main(input_source):
    """
    input_source can be:
    - a filename (string) containing one stage per line
    - a list of strings, each describing a stage
    """
    if isinstance(input_source, str):
        with open(input_source, 'r') as f:
            lines = f.readlines()
        base_name = os.path.splitext(os.path.basename(input_source))[0]
        output_file = f"{base_name}.png"
    else:
        lines = input_source
        output_file = "bloch_sphere_visualization.png"

    vectors = []
    titles = []
    stage_num = 0
    for i, line in enumerate(lines):
        try:
            vec = parse_stage(line)
            if vec is not None:
                stage_num += 1
                vectors.append(vec)
                titles.append(f"Stage {stage_num}")
        except Exception as e:
            print(f"Error in line {i+1}: {line.strip()}\n{e}")

    if not vectors:
        print("No valid stages found.")
        return

    # Create a grid of subplots (one per stage)
    n = len(vectors)
    cols = min(3, n)
    rows = (n + cols - 1) // cols
    fig = plt.figure(figsize=(5*cols, 5*rows))

    for idx, (vec, title) in enumerate(zip(vectors, titles)):
        ax = fig.add_subplot(rows, cols, idx+1, projection='3d')
        draw_bloch_sphere(ax, vec, title)

    plt.tight_layout()
    plt.savefig(output_file, dpi=150)
    print(f"Saved visualization to {output_file}")

# Example usage
if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        main(input_file)
    else:
        sample_stages = [
            "|0>",
            "|+>",
            "theta=60 deg, phi=45 deg",
            "(0.707+0j, 0.707+0j)",
            "(-0.5+0.5j, 0.5+0.5j)"
        ]
        main(sample_stages)