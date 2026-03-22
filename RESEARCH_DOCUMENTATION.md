# Quantum Algorithm Visualization Research Project

## Research Hypothesis

### Original Hypothesis (DeepSeek)

> **Certain visualization styles are optimal for specific quantum algorithm families.**

| Algorithm Family | Proposed Best Visualization | Rationale |
|------------------|---------------------------|-----------|
| **Oracle-based** | Geometric (Bloch sphere) + Algebraic (amplitude bars) | Shows rotation toward target + quantifies success probability |
| **Transform-based** | Algebraic (phase/amplitude vs. index) | Periodic phase patterns are the key output |
| **Variational** | Graph-based (circuit diagram) + Geometric (cost landscape) | Circuit structure shows parameter dependencies; cost landscape explains optimization |
| **Simulation-based** | Dynamic/Flow (trajectory) + Geometric | Hamiltonian dynamics visible as state evolution |

---

## Methodology

### Visualization Tools Used

| Tool | Type | What It Shows |
|------|------|---------------|
| **Bloch Sphere** | Geometric | Single-qubit state as 3D vector; phase as angle φ |
| **State City** | Geometric (Density Matrix) | 2^n × 2^n bar chart; real/imaginary parts |
| **Cost Landscape** | Geometric (Parameter Space) | 2D plot of cost vs. parameters |
| **Circuit Diagram** | Graph-based | Quantum circuit gates and connectivity |
| **Dynamic Flow** | Dynamic/Trajectory | State evolution over time |

### Algorithms Tested

| Family | Algorithm | Qubits | Scalability Tested |
|--------|-----------|--------|-------------------|
| Oracle-based | Grover's Search | 2, 3, 4 | ✓ |
| Oracle-based | Deutsch-Jozsa | 2 | - |
| Transform-based | QFT | 2, 3, 4 | ✓ |
| Transform-based | QPE | 2 | - |
| Variational | QAOA | 2, 3 | ✓ |
| Variational | VQE | 2, 3 | ✓ |
| Simulation-based | Rabi Oscillation | 1 | - |
| Simulation-based | Transverse Field Ising | 2 | - |

---

## Part 1: Hypothesis Testing Results

### Oracle-Based Algorithms

| Algorithm | Qubits | Bloch | State City | Circuit | Finding |
|-----------|--------|-------|-----------|---------|---------|---------|
| Grover's | 2, 3, 4 | ✓ Rotation | ✓ Probability | ✓ Gate structure | ✓ Confirms |
| Deutsch-Jozsa | 2 | ✓ Return to \|0⟩ | ✓ Deterministic | ✓ Oracle box | ✓ Confirms |

**Conclusion**: Bloch + State City + Circuit together provide complete picture.

---

### Transform-Based Algorithms

| Algorithm | Qubits | Bloch | State City | Circuit | Finding |
|-----------|--------|-------|-----------|---------|---------|---------|
| QFT | 2, 3, 4 | ✗ | ✓ Phase periodicity | ✓ Butterfly pattern | ✓ Confirms |
| QPE | 2 | ⚠ | ✓ Phase extraction | ✓ Controlled-U | ✓ Confirms |

**Conclusion**: **State City is essential** for transform-based algorithms.

---

### Variational Algorithms

| Algorithm | Qubits | Bloch | State City | Cost Landscape | Circuit | Finding |
|-----------|--------|-------|-----------|----------------|---------|---------|---------|
| QAOA | 2, 3 | ✗ | ⚠ | ✓ Surface | ✓ Ansatz | ✓ Confirms |
| VQE | 2, 3 | ✗ | ⚠ | ✓ Energy min | ✓ Ansatz | ✓ Confirms |

**Conclusion**: **Circuit + Cost Landscape** complete the variational picture.

---

### Simulation-Based Algorithms

| Algorithm | Qubits | Bloch | State City | Dynamic Flow | Finding |
|-----------|--------|-------|-----------|-------------|---------|---------|
| Rabi Oscillation | 1 | ✓ Trajectory | ✓ Density | ✓ Time evolution | ✓ Confirms |
| Ising Model | 2 | N/A | ✓ Entanglement | ✓ Correlation build | ✓ Confirms |

**Conclusion**: **Dynamic Flow is essential** for simulation-based algorithms. Shows Hamiltonian evolution over time.

---

## Part 2: Scalability Analysis

### State City Scalability

| Qubits | Matrix Size | Usability | Notes |
|--------|-------------|-----------|-------|
| 2 | 4×4 | ✓ Excellent | Clear bars |
| 3 | 8×8 | ✓ Good | Still readable |
| 4 | 16×16 | ⚠ Challenging | Crowded |
| 5+ | 32×32+ | ✗ Impractical | Too dense |

### Visualization Scalability Summary

| Visualization | 2 qubits | 3 qubits | 4 qubits | 5+ qubits |
|---------------|----------|----------|----------|-----------|
| **Bloch Sphere** | ✓ | ✓ | ✓ | ✓ |
| **State City** | ✓ | ✓ | ⚠ | ✗ |
| **Cost Landscape** | ✓ | ✓ | ✓ | ✓ |
| **Circuit Diagram** | ✓ | ✓ | ✓ | ⚠ |
| **Dynamic Flow** | ✓ | ✓ | ✓ | ✓ |

---

## Part 3: Paper-Ready Comparison Images

Side-by-side comparison images generated for each algorithm family:

| Image | Content |
|-------|---------|
| `comparison_grover.png` | Bloch + State City + Probability for each stage |
| `comparison_qft.png` | Bloch + State City for QFT stages |
| `comparison_qaoa.png` | State City + Cost Landscape + Parameter evolution |
| `comparison_simulation.png` | Bloch trajectory + Z vs Time plot |

---

## Summary: Final Hypothesis Validation

| Algorithm Family | Hypothesis | Validation | Best Combination |
|------------------|------------|------------|-----------------|-----------------|-----------------|
| Oracle-based | Geometric + Algebraic | ✓ CONFIRMED | Bloch + State City + Circuit |
| Transform-based | Algebraic | ✓ CONFIRMED | State City + Circuit |
| Variational | Graph + Geometric | ✓ CONFIRMED | Circuit + Cost Landscape |
| Simulation-based | Dynamic + Geometric | ✓ CONFIRMED | Dynamic Flow + Bloch |

---

## Conclusions

1. **Oracle-based**: Bloch (rotation) + State City (probability) + Circuit (structure) — all three needed.

2. **Transform-based**: State City essential for phase periodicity. Circuit shows butterfly pattern.

3. **Variational**: Circuit shows ansatz/parameters. Cost Landscape shows optimization. Both needed.

4. **Simulation-based**: Dynamic Flow essential for Hamiltonian dynamics. Bloch shows single-qubit trajectory.

5. **Scalability**: Bloch, Circuit, Dynamic Flow scale well. State City practical limit is 3-4 qubits.

---

## Files Generated

### Visualization Modules
```
Bloch_Sphere_Visualization/code/program.py
State_City_Visualization/code/program.py
Cost_Landscape_Visualization/code/cost_landscape.py
Cost_Landscape_Visualization/code/vqe_energy_landscape.py
Circuit_Diagram_Visualization/code/circuit_diagram.py
Dynamic_Flow_Visualization/code/dynamic_flow.py
```

### Side-by-Side Comparisons
```
comparison_grover.png
comparison_qft.png
comparison_qaoa.png
comparison_simulation.png
```

### Algorithm Inputs
```
State_City_Visualization/algs/oracle-based-algs/...
State_City_Visualization/algs/transform-based-algs/...
State_City_Visualization/algs/variational-algs/...
State_City_Visualization/algs/simulation-based-algs/...
```

---

## Future Work

1. Add animation for dynamic/trajectory visualizations
2. Test 5+ qubits with alternative density matrix visualization
3. Add more simulation algorithms (quantum walks, adiabatic evolution)
