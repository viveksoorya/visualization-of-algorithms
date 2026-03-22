# Quantum Algorithm Visualization Project

## Project Overview

This project contains visualizations for quantum algorithms using different representation approaches. Currently implemented visualizations compare geometric representations (Bloch Sphere and State City), with a focus on amplitude amplification algorithms (Grover's search).

## Directory Structure

```
visualization-of-algorithms/
├── Bloch_Sphere_Visualization/          # Geometric visualization (single-qubit Bloch sphere)
│   ├── code/
│   │   └── program.py                   # Main visualization program
│   ├── docs/
│   │   ├── program-design.md            # Architecture overview
│   │   ├── input-specification-format.md # Input format documentation
│   │   └── limitations-of-this-visualization.md
│   ├── algs/
│   │   └── amplitude-dampening-algs/
│   │       └── grover-search/
│   │           ├── grover_N16.txt       # Input file (Bloch angles)
│   │           └── grover_N16.png       # Output visualization
│   └── grover_N16.png                   # Example output
│
└── State_City_Visualization/            # Geometric visualization (density matrix)
    ├── code/
    │   └── program.py                   # Main visualization program
    ├── docs/
    │   ├── program-design.md            # Architecture overview
    │   ├── input-format-specification.md # Input format documentation
    │   ├── example-input-format.json    # JSON schema example
    │   ├── example-input.json           # Full example
    │   └── limitations.md
    ├── algs/
    │   └── amplitude-dampening-algs/
    │       └── grover-search/
    │           ├── grover_2qubit.json   # Input file (state vectors)
    │           ├── setup-explanation.md # Algorithm walkthrough
    │           ├── results-and-interpretation.md
    │           └── stage_*.png          # Output visualizations
```

## Visualization Types Implemented

### 1. Bloch Sphere Visualization (`Bloch_Sphere_Visualization/`)

**Type**: Geometric - Single Qubit

**Representation**: 3D Bloch sphere with state vector as an arrow

**How it works**:
- Converts quantum state to Bloch vector (x, y, z) coordinates
- Renders sphere surface with coordinate axes
- Draws arrow from origin to state point on sphere surface

**Input Format**: Text file, one stage per line
- Ket notation: `|0>`, `|1>`, `|+>`, `|->`, `|+i>`, `|-i>`
- Complex coefficients: `(a+bi, c+di)` representing α|0⟩ + β|1⟩
- Bloch angles: `theta=60 deg, phi=45 deg`
- Bloch vector: `(x,y,z)` Cartesian coordinates

**Limitations**:
- Single qubit only (cannot visualize entanglement directly)
- Pure states only (no mixed states)
- Cannot show multi-qubit correlations

**Dependencies**: numpy, matplotlib

**Run**: `python program.py <input-file>`

---

### 2. State City Visualization (`State_City_Visualization/`)

**Type**: Geometric - Multi Qubit Density Matrix

**Representation**: 3D bar chart showing density matrix elements

**How it works**:
- Converts state vector to density matrix: ρ = |ψ⟩⟨ψ|
- Creates two 3D bar charts: real part (left) and imaginary part (right)
- Color coding: red = positive, blue = negative

**Input Format**: JSON file
```json
{
  "qubits": 2,
  "stages": [
    {
      "name": "Stage description",
      "state_vector": [amplitude_0, amplitude_1, ...]
    }
  ]
}
```
Amplitudes can be: real numbers, complex strings ("0.5+0.5j"), or [real, imag] arrays.

**Limitations**:
- Exponential scaling: 2^n × 2^n matrix (practical limit ~5 qubits)
- Pure states only
- Big-endian basis ordering
- No phase color encoding

**Dependencies**: numpy, matplotlib

**Run**: `python program.py <input-json-file>`

---

## Algorithm Categories for Future Expansion

### 1. Quantum Fourier Transform (QFT) Kind
**Characteristics**:
- Uses Hadamard and controlled-R gates
- Creates entangled states with periodic amplitudes
- Phase relationships are crucial
- Output is frequency domain representation

**Visualization Needs**:
- Phase information critical (Bloch sphere good for single qubit phases)
- Multi-qubit entanglement visualization (state city shows coherences)
- Complex-valued amplitudes with specific phase patterns

**Example algorithms**: QFT, Quantum Phase Estimation, Shor's algorithm

---

### 2. Amplitude Dampening Kind
**Characteristics**:
- Amplitude amplification/probability redistribution
- Typically involves oracle + diffusion (Grover-style)
- Probability redistribution without phase changes
- Iterative approach converging to solution

**Visualization Needs**:
- Probability distribution across basis states
- Amplitude changes between iterations
- Coherence patterns during amplification

**Currently Implemented**: Grover's Search (2-qubit and N=16 examples)

**Example algorithms**: Grover's Search, Amplitude Estimation, Quantum Counting

---

### 3. Variational Algorithms Kind
**Characteristics**:
- Hybrid quantum-classical approach
- Parameterized quantum circuits (PQC)
- Expectation value measurement
- Classical optimization loop
- Typically uses ansatz circuits

**Visualization Needs**:
- Circuit structure visualization
- Parameter evolution tracking
- Cost function landscapes
- Measurement outcome distributions
- Entanglement patterns across iterations

**Example algorithms**: VQE, QAOA, Variational Quantum Eigensolver, Quantum Approximate Optimization Algorithm

---

## Comparison Matrix: Visualization Types

| Aspect | Bloch Sphere | State City | Graph-Based | Algebraic |
|--------|-------------|------------|-------------|-----------|
| **Type** | Geometric | Geometric | Graph | Symbolic |
| **Qubits** | 1 | n (≤5) | n | n |
| **Phase** | Via angle φ | Via Im(ρ) | N/A | Exact |
| **Entanglement** | Limited | Via off-diagonals | Via edges | Matrix rank |
| **Coherence** | Vector position | Bar heights | N/A | Matrix elements |
| **Probability** | Via θ | Via diagonal ρ | Node weights | Exact values |
| **Scalability** | Good | Poor (2^n) | Medium | Good |

---

## Adding New Visualizations

### For Bloch Sphere (Single Qubit)
1. Add input file to `Bloch_Sphere_Visualization/algs/<category>/<algorithm>/`
2. Follow input format (ket/angles/vector per line)
3. Run: `python code/program.py algs/<path>/input.txt`

### For State City (Multi Qubit)
1. Add JSON file to `State_City_Visualization/algs/<category>/<algorithm>/`
2. Follow JSON schema with qubits + stages + state_vectors
3. Run: `python code/program.py algs/<path>/input.json`

### For Graph-Based Visualization (Future)
Consider:
- Circuit diagrams (gate-level graphs)
- Tensor network representations
- Entanglement graphs (basis state connections)
- Qubit connectivity/interaction graphs

### For Algebraic Visualization (Future)
Consider:
- Matrix representations (density matrices, unitary operators)
- Bra-ket notation rendering
- Equation display for gate transformations
- Probability table outputs

---

## Input/Output Conventions

### Naming Conventions
- Input files: `<algorithm>_<qubits>.<txt|json>`
- Output files: `<algorithm>_<qubits>.png` or `stage_XX_<name>.png`
- Algorithm categories: `quantum-fourier-transform/`, `amplitude-dampening/`, `variational/`

### State Vector Ordering
- Big-endian: |q₁q₀⟩ where q₁ is most significant bit
- Basis order: |00⟩, |01⟩, |10⟩, |11⟩ for 2 qubits

### Amplitude Format
- Must be normalized (program does not renormalize)
- Complex amplitudes supported in all visualizations

---

## Running Visualizations

```bash
# Bloch Sphere
cd Bloch_Sphere_Visualization/code
python program.py ../algs/amplitude-dampening-algs/grover-search/grover_N16.txt

# State City
cd State_City_Visualization/code
python program.py ../algs/amplitude-dampening-algs/grover-search/grover_2qubit.json
```

---

## Dependencies

All visualizations require:
- Python 3.7+
- NumPy
- Matplotlib

Install all: `pip install numpy matplotlib`

---

## Extension Priorities for Comparative Analysis

1. **QFT Implementation**: Add QFT algorithm to both visualization types to compare phase evolution
2. **Graph-Based**: Add circuit diagram renderer showing gate connectivity
3. **Variational**: Add parameter tracking and cost landscape visualization
4. **Unified Pipeline**: Create common input format that generates all visualization types simultaneously

---

## Notes

- Current focus: Amplitude Dampening (Grover's algorithm)
- Both geometric visualizations are static (PNG output, no animation)
- No quantum simulator included - user provides state vectors
- Each visualization requires manual state computation or external simulator
