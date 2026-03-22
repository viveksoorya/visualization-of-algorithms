import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def qaoa_cost(gamma, beta):
    g = np.asarray(gamma)
    b = np.asarray(beta)
    cost = 0.5 + 0.3 * np.sin(2*g) * np.cos(2*b) + 0.2 * np.cos(4*g)
    return cost

gammas = np.linspace(0, np.pi, 50)
betas = np.linspace(0, np.pi, 50)
G, B = np.meshgrid(gammas, betas)
Z = qaoa_cost(G, B)

plt.figure(figsize=(10, 8))
contour = plt.contourf(G, B, Z, levels=20, cmap='viridis')
plt.colorbar(contour, label='Cost (Cut Value)')
plt.xlabel('γ (problem parameter)')
plt.ylabel('β (mixer parameter)')
plt.title('QAOA Cost Landscape: MaxCut (2 qubits)')
plt.savefig('qaoa_cost_landscape.png', dpi=150)
plt.close()
print("Saved: qaoa_cost_landscape.png")
