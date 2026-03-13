import json
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def parse_amplitude(amp):
    """Convert various input formats to a complex number."""
    if isinstance(amp, (int, float)):
        return complex(amp, 0)
    elif isinstance(amp, str):
        # Remove any spaces and try to convert
        amp = amp.replace(' ', '')
        if amp.endswith('j'):
            return complex(amp)
        else:
            # Treat as real number
            return complex(float(amp), 0)
    elif isinstance(amp, (list, tuple)) and len(amp) == 2:
        return complex(amp[0], amp[1])
    else:
        raise ValueError(f"Unsupported amplitude format: {amp}")

def state_to_density(state_vector):
    """Convert a state vector (list of complex numbers) to a density matrix."""
    psi = np.array(state_vector, dtype=complex).reshape(-1, 1)
    return psi @ psi.conj().T

def plot_state_city(rho, title, filename):
    """
    Create a state city plot (real and imag parts of the density matrix)
    and save it to a file.
    """
    dim = rho.shape[0]
    xpos, ypos = np.meshgrid(range(dim), range(dim), indexing='ij')
    xpos = xpos.flatten()
    ypos = ypos.flatten()
    zpos = np.zeros_like(xpos)

    # Bar dimensions
    dx = dy = 0.8 * np.ones_like(zpos)

    # Real part
    real_vals = np.real(rho).flatten()
    # Imag part
    imag_vals = np.imag(rho).flatten()

    # Determine colors: red for positive, blue for negative
    real_colors = ['red' if v >= 0 else 'blue' for v in real_vals]
    imag_colors = ['red' if v >= 0 else 'blue' for v in imag_vals]

    # Create figure with two subplots
    fig = plt.figure(figsize=(14, 6))
    fig.suptitle(title, fontsize=16)

    # Real part subplot
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.bar3d(xpos, ypos, zpos, dx, dy, real_vals, color=real_colors, alpha=0.8)
    ax1.set_title('Real part')
    ax1.set_xlabel('Basis state (row)')
    ax1.set_ylabel('Basis state (col)')
    ax1.set_zlabel('Amplitude')
    ax1.set_xticks(range(dim))
    ax1.set_yticks(range(dim))

    # Imaginary part subplot
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.bar3d(xpos, ypos, zpos, dx, dy, imag_vals, color=imag_colors, alpha=0.8)
    ax2.set_title('Imaginary part')
    ax2.set_xlabel('Basis state (row)')
    ax2.set_ylabel('Basis state (col)')
    ax2.set_zlabel('Amplitude')
    ax2.set_xticks(range(dim))
    ax2.set_yticks(range(dim))

    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()

def main(input_file):
    # Load and parse input
    with open(input_file, 'r') as f:
        data = json.load(f)

    n_qubits = data['qubits']
    dim = 2 ** n_qubits
    stages = data['stages']

    for i, stage in enumerate(stages):
        name = stage.get('name', f'Stage {i+1}')
        raw_state = stage['state_vector']

        # Parse each amplitude to complex
        state_vector = [parse_amplitude(amp) for amp in raw_state]

        if len(state_vector) != dim:
            raise ValueError(f"Stage '{name}': state vector length {len(state_vector)} "
                             f"does not match 2^{n_qubits}={dim}")

        # Compute density matrix
        rho = state_to_density(state_vector)

        # Create plot
        filename = f"stage_{i+1:02d}_{name.replace(' ', '_')}.png"
        plot_state_city(rho, name, filename)
        print(f"Saved: {filename}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python state_city.py <input_json_file>")
        sys.exit(1)
    main(sys.argv[1])