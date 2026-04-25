# Visualization Comparison: Per-Algorithm Analysis

## Grover's Search (Oracle-based)

### Bloch Sphere Insights
- **What it shows**: State vector rotating from |+⟩ toward |11⟩
- **Key insight**: Amplitude amplification as geometric rotation toward target
- **Stage-by-stage**:
  - Initial |00⟩ → Bloch vector at |0⟩ (z=1)
  - After H: uniform superposition → equator of sphere
  - After Oracle: phase flip (not visible as rotation)
  - After Diffusion: rotation toward |11⟩ target

### State City Insights  
- **What it shows**: Real/imaginary parts of density matrix
- **Key insight**: Diagonal = probabilities; shows success probability increase
- **Stage-by-stage**:
  - Initial: |00⟩ → probability on |00⟩ = 1.0
  - After H: equal probabilities 0.25 each
  - After Oracle: phase flip on |11⟩ (imag part shows -0.5)
  - After Diffusion: probability on |11⟩ = 1.0

### Which is Better?
- **For understanding algorithm mechanics**: Bloch Sphere (rotation)
- **For quantifying success**: State City (probabilities)

---

## Quantum Fourier Transform (Transform-based)

### Bloch Sphere Insights
- **What it shows**: Phase angle φ on single qubit
- **Key limitation**: Cannot capture multi-qubit phase relationships
- **Example**: Shows final state has φ=90° but misses entanglement

### State City Insights
- **What it shows**: Full density matrix with phase patterns
- **Key insight**: Imaginary part reveals periodic phase structure across basis states
- **Example**: QFT on |01⟩ shows phase progression: 0 → π/2 → π → 3π/2

### Which is Better?
- **State City is clearly superior** for QFT
- Bloch Sphere fails to show the key insight (phase periodicity)

---

## QAOA (Variational)

### Bloch Sphere Insights
- **What it shows**: Single qubit state during parameter evolution
- **Key limitation**: Doesn't show parameter optimization or cost
- **Use case**: Limited - only shows final state per iteration

### State City Insights
- **What it shows**: Amplitude distribution across all basis states
- **Key insight**: Shows probability of measuring solution states (|01⟩, |10⟩)
- **Evolution**: Amplitude shifts from uniform → solution states

### Cost Landscape Insights
- **What it shows**: Cost function C(γ, β) as 2D contour
- **Key insight**: Shows optimization landscape, local minima, global optimum
- **Use case**: Essential for understanding variational algorithms

### Which is Better?
- **Cost Landscape is essential** for understanding parameter optimization
- **State City** shows solution quality
- **Bloch Sphere** has limited utility

---

## Overall Recommendations

| Algorithm Family | Primary Visualization | Secondary |
|------------------|----------------------|-----------|
| Oracle-based | Bloch Sphere | State City |
| Transform-based | State City | - |
| Variational | Cost Landscape | State City |
