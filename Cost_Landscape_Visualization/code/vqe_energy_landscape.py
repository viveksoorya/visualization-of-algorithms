import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def vqe_cost(theta):
    t = np.asarray(theta)
    cost = -1.0 + 0.3 * np.cos(t) + 0.5 * np.cos(2*t)
    return cost

thetas = np.linspace(0, np.pi, 100)
E = vqe_cost(thetas)

plt.figure(figsize=(10, 6))
plt.plot(thetas, E, 'b-', linewidth=2)
plt.axhline(y=-1.0, color='r', linestyle='--', label='Exact ground state')
plt.xlabel('θ (variational parameter)')
plt.ylabel('Energy E(θ)')
plt.title('VQE Energy Landscape: H2 Molecule (2 qubits)')
plt.grid(True, alpha=0.3)
plt.legend()
plt.savefig('vqe_energy_landscape.png', dpi=150)
plt.close()
print("Saved: vqe_energy_landscape.png")
