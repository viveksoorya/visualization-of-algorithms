# AGENTS.md - Guidelines for Agentic Coding in This Repository

## Project Overview

This repository contains quantum algorithm visualization tools:
- **quantumviz package** - Modern Python package in `quantumviz/src/quantumviz/`
- **Legacy modules** - Standalone visualization scripts in `*_Visualization/code/`
- **Dashboard** - FastAPI web API for interactive visualizations

## Project Structure

```
quantumviz/
├── src/quantumviz/     # Main package
│   ├── __init__.py
│   ├── bloch_sphere.py
│   ├── state_city.py
│   ├── cost_landscape.py
│   ├── circuit_diagram.py
│   ├── dynamic_flow.py
│   └── cli.py          # Click-based CLI
├── tests/              # pytest test suite
│   ├── conftest.py    # Shared fixtures
│   └── test_*.py
└── pyproject.toml      # Package config with ruff/mypy settings
```

## Build & Run Commands

### Install Package

```bash
cd quantumviz
pip install -e ".[dev]"    # Install with dev dependencies
pip install -e ".[dashboard]"  # Install with dashboard
```

### Run Visualizations (quantumviz package)

```bash
# Via CLI
quantumviz bloch-sphere input.txt -o output.png
quantumviz state-city input.json -o output/
quantumviz cost-landscape qaoa -o output.png
quantumviz circuit input.json -o output.png
quantumviz dynamic-flow input.json -o output.png

# Direct module execution
python -m quantumviz.cli bloch-sphere input.txt
```

### Legacy Visualizations

```bash
python Bloch_Sphere_Visualization/code/program.py <input.txt>
python State_City_Visualization/code/program.py <input.json>
python Cost_Landscape_Visualization/code/cost_landscape.py
python Circuit_Diagram_Visualization/code/circuit_diagram.py <input.json>
python Dynamic_Flow_Visualization/code/dynamic_flow.py <input.json>
```

### Dashboard

```bash
cd dashboard/api
pip install -r ../requirements.txt
python main.py  # Runs on http://localhost:8000
```

## Testing

### Run All Tests

```bash
cd quantumviz
pytest                    # Run all tests
pytest -v                 # Verbose output
pytest --cov=src          # With coverage
pytest --cov=src --cov-report=html  # HTML coverage report
```

### Run Specific Tests

```bash
# Single test file
pytest tests/test_cost_landscape.py

# Single test class
pytest tests/test_cost_landscape.py::TestQAOACost

# Single test function
pytest tests/test_cost_landscape.py::TestQAOACost::test_qaoa_cost_scalar

# Run tests matching pattern
pytest -k "test_qaoa"    # Tests with "test_qaoa" in name
pytest -k "scalar or array"  # Multiple patterns
```

## Linting & Type Checking

```bash
cd quantumviz

# Run ruff (linting)
ruff check src/

# Fix auto-fixable issues
ruff check --fix src/

# Run mypy (type checking)
mypy src/

# Run both
ruff check src/ && mypy src/
```

## Code Style Guidelines

### Imports

Order: standard library → third-party → local. Use explicit imports.

```python
# Correct
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json
import sys

# Incorrect
from matplotlib import *
from mpl_toolkits.mplot3d import *
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Modules | lowercase | `circuit_diagram.py` |
| Functions | snake_case | `parse_amplitude()`, `plot_bloch_sphere()` |
| Classes | PascalCase | `BlochSphereInput`, `StateVectorInput` |
| Constants | UPPER_SNAKE | `GATE_COLORS`, `DEFAULT_DPI` |
| Variables | snake_case | `state_vector`, `bloch_vector` |

### Type Hints

Use type hints for function signatures.

```python
def parse_amplitude(amp: Any) -> complex:
    """Convert various input formats to a complex number."""

def state_to_density(state_vector: list[complex]) -> np.ndarray:
    """Convert a state vector to a density matrix."""
    psi = np.array(state_vector, dtype=complex).reshape(-1, 1)
    return psi @ psi.conj().T
```

### Docstrings

Use triple-quoted docstrings for all public functions:

```python
def parse_amplitude(amp):
    """Convert various input formats to a complex number.
    
    Args:
        amp: Amplitude in various formats (int, float, str, list/tuple)
        
    Returns:
        complex: Normalized complex amplitude
        
    Raises:
        ValueError: If amplitude format is unsupported
    """
```

### Error Handling

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

- Always use non-interactive backend: `matplotlib.use('Agg')`
- Set figure size: `figsize=(width, height)`
- Use `tight_layout()` before saving
- Always `plt.close()` to free memory
- Use `dpi=150` for publication quality

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
- Specify dtype explicitly: `np.array(data, dtype=complex)`
- Use vectorized operations when possible
- Handle complex numbers explicitly

### FastAPI/Dashboard Guidelines

- Use Pydantic `BaseModel` for request/response schemas
- Use `Field()` for schema descriptions
- Add CORS middleware for frontend access

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class StateVectorInput(BaseModel):
    qubits: int = Field(ge=1, le=10, description="Number of qubits")
    stages: List[Dict[str, Any]]
```

## Quantum Conventions

- Big-endian basis ordering: |q₁q₀⟩ where q₁ is MSB
- Complex amplitudes: use `j` suffix (Python convention)
- Normalize all state vectors to unit length
- Density matrix: ρ = |ψ⟩⟨ψ|

## Input File Formats

### JSON Format (State City, Circuit Diagrams)

```json
{
  "qubits": 2,
  "stages": [
    {"name": "Stage name", "state_vector": [1, 0, 0, 0]}
  ]
}
```

### TXT Format (Bloch Sphere)

```
|0>                    # Ket notation
theta=60 deg, phi=45   # Bloch angles
(x,y,z)               # Cartesian coordinates
```

## Configuration (pyproject.toml)

```toml
[tool.ruff]
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W"]
ignore = ["E501"]

[tool.mypy]
python_version = "3.9"
warn_return_any = "True"
warn_unused_configs = "True"
```
