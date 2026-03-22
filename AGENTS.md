# AGENTS.md - Guidelines for Agentic Coding in This Repository

## Project Overview

This repository contains quantum algorithm visualization tools. Each visualization type is a self-contained module with input files for different algorithm families (oracle-based, transform-based, variational, simulation-based).

## Build & Run Commands

### Running Visualizations

```bash
# Bloch Sphere Visualization
cd Bloch_Sphere_Visualization/code
python program.py <input_file.txt>

# State City Visualization  
cd State_City_Visualization/code
python program.py <input_file.json>

# Cost Landscape Visualization
cd Cost_Landscape_Visualization/code
python cost_landscape.py          # QAOA landscape
python vqe_energy_landscape.py    # VQE landscape

# Circuit Diagram Visualization
cd Circuit_Diagram_Visualization/code
python circuit_diagram.py <circuit.json>

# Dynamic Flow Visualization
cd Dynamic_Flow_Visualization/code
python dynamic_flow.py <input.json>

# Generate comparison images
cd /home/uni/visualization-of-algorithms
python generate_comparisons.py
```

### Compiling LaTeX Paper

```bash
cd paper
pdflatex main.tex      # First pass
pdflatex main.tex      # Second pass (fix references)
```

## Code Style Guidelines

### Imports
- Standard library imports first (json, sys, os, re)
- Third-party imports next (numpy, matplotlib)
- Use `matplotlib.use('Agg')` for non-interactive backend
- Import specific modules to avoid namespace pollution

```python
# Correct
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Incorrect
from matplotlib import pyplot as *
from mpl_toolkits.mplot3d import *
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Modules | lowercase | `circuit_diagram.py` |
| Functions | snake_case | `parse_amplitude()`, `draw_bloch_sphere()` |
| Classes | PascalCase | (not used extensively) |
| Constants | UPPER_SNAKE | `GATE_COLORS`, `DEFAULT_DPI` |
| Variables | snake_case | `state_vector`, `bloch_vector` |
| Input files | lowercase + underscore | `grover_2qubit.json` |

### File Structure

```
visualization-module/
├── code/
│   └── program.py          # Main visualization program
├── docs/
│   └── documentation.md   # Module-specific docs
└── algs/
    └── <category>/
        └── <algorithm>/
            └── input files (.json or .txt)
```

### Docstrings

- Use triple-quoted docstrings for all public functions
- Include description, parameters, and return values

```python
def parse_amplitude(amp):
    """Convert various input formats to a complex number.
    
    Args:
        amp: Amplitude in various formats (int, float, str, list)
        
    Returns:
        complex: Normalized complex amplitude
        
    Raises:
        ValueError: If amplitude format is unsupported
    """
```

### Error Handling

- Use descriptive error messages with context
- Catch specific exceptions when needed
- Print helpful usage instructions on failure

```python
if len(sys.argv) != 2:
    print("Usage: python program.py <input_file>")
    sys.exit(1)
    
try:
    result = parse_input(data)
except ValueError as e:
    print(f"Invalid input: {e}")
    raise
```

### Matplotlib Guidelines

- Always use non-interactive backend (`matplotlib.use('Agg')`)
- Set figure size with `figsize=(width, height)`
- Use `tight_layout()` before saving
- Always `plt.close()` to free memory
- Use `dpi=150` for publication-quality output

```python
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(10, 6))
# ... plotting code ...
plt.tight_layout()
plt.savefig('output.png', dpi=150)
plt.close()
```

### NumPy Guidelines

- Use `np.` prefix for all numpy functions
- Specify dtype explicitly for arrays: `np.array(data, dtype=complex)`
- Use vectorized operations when possible
- Handle complex numbers explicitly

### Input File Formats

#### JSON Format (State City, Circuit Diagrams)
```json
{
  "qubits": 2,
  "stages": [
    {"name": "Stage name", "state_vector": [1, 0, 0, 0]}
  ]
}
```

#### TXT Format (Bloch Sphere)
```
|0>                    # Ket notation
theta=60 deg, phi=45   # Bloch angles
(x,y,z)               # Cartesian coordinates
```

### Directory Naming
- Use lowercase with hyphens for directories: `bloch-sphere-visualization/`
- Algorithm categories: `oracle-based-algs/`, `transform-based-algs/`, etc.
- Algorithm names: `grover-search/`, `quantum-fourier-transform/`

### Quantum Conventions
- Big-endian basis ordering: |q₁q₀⟩ where q₁ is MSB
- Complex amplitudes: use `j` suffix (Python convention)
- Normalize all state vectors to unit length
- Density matrix: ρ = |ψ⟩⟨ψ|

## Testing

### Manual Testing
No formal test suite exists. Test by running visualizations:
```bash
# Test Bloch Sphere
python Bloch_Sphere_Visualization/code/program.py \
  Bloch_Sphere_Visualization/algs/oracle-based-algs/deutsch-jozsa/dj_stages.txt

# Test State City
python State_City_Visualization/code/program.py \
  State_City_Visualization/algs/amplitude-dampening-algs/grover-search/grover_2qubit.json
```

### Adding New Algorithms
1. Create input file in appropriate `algs/<category>/<algorithm>/` directory
2. Follow existing input format conventions
3. Run visualization and verify output

## Common Patterns

### Parsing Complex Numbers
```python
def parse_complex(val):
    if isinstance(val, (int, float)):
        return complex(val, 0)
    elif isinstance(val, str):
        return complex(val.replace(' ', ''))
    return complex(val)
```

### Density Matrix Calculation
```python
def state_to_density(state_vector):
    psi = np.array(state_vector, dtype=complex).reshape(-1, 1)
    return psi @ psi.conj().T
```

### CLI Entry Point
```python
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python program.py <input_file>")
        sys.exit(1)
    main(sys.argv[1])
```
