import json
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

GATE_COLORS = {
    'H': '#FF6B6B',
    'X': '#4ECDC4',
    'Y': '#45B7D1',
    'Z': '#96CEB4',
    'CNOT': '#FFEAA7',
    'CZ': '#DDA0DD',
    'T': '#98D8C8',
    'S': '#F7DC6F',
    'RX': '#BB8FCE',
    'RY': '#85C1E9',
    'RZ': '#F8B500',
    'U': '#AED6F1',
    'measure': '#E74C3C',
    'default': '#D5D8DC'
}

def draw_qubit_line(ax, y, num_wires, color='black'):
    ax.plot([0, num_wires * 2], [y, y], color=color, linewidth=1.5)

def draw_single_gate(ax, gate, x, y, label=None):
    color = GATE_COLORS.get(gate, GATE_COLORS['default'])
    rect = patches.Rectangle((x - 0.3, y - 0.3), 0.6, 0.6,
                               linewidth=1.5, edgecolor='black',
                               facecolor=color, zorder=3)
    ax.add_patch(rect)
    if label:
        ax.text(x, y, label, ha='center', va='center', fontsize=8, zorder=4)
    else:
        ax.text(x, y, gate, ha='center', va='center', fontsize=8, fontweight='bold', zorder=4)

def draw_cnot(ax, ctrl_x, ctrl_y, target_x, target_y):
    ax.plot([ctrl_x, ctrl_x], [ctrl_y, ctrl_y - 0.5], color='black', linewidth=1.5)
    ax.plot([ctrl_x, target_x], [ctrl_y - 0.5, ctrl_y - 0.5], color='black', linewidth=1.5)
    ax.plot([target_x, target_x], [ctrl_y - 0.5, target_y], color='black', linewidth=1.5)
    ax.scatter([ctrl_x], [ctrl_y], color='black', s=80, zorder=5, marker='o')
    rect = patches.Rectangle((target_x - 0.3, target_y - 0.3), 0.6, 0.6,
                               linewidth=1.5, edgecolor='black',
                               facecolor=GATE_COLORS['CNOT'], zorder=3)
    ax.add_patch(rect)
    ax.text(target_x, target_y, 'X', ha='center', va='center', fontsize=8, fontweight='bold', zorder=4)

def draw_controlled_gate(ax, ctrl_x, ctrl_y, target_x, target_y, gate='Z'):
    ax.plot([ctrl_x, ctrl_x], [ctrl_y, ctrl_y - 0.5], color='black', linewidth=1.5)
    ax.plot([ctrl_x, target_x], [ctrl_y - 0.5, ctrl_y - 0.5], color='black', linewidth=1.5)
    ax.plot([target_x, target_x], [ctrl_y - 0.5, target_y], color='black', linewidth=1.5)
    ax.scatter([ctrl_x], [ctrl_y], color='black', s=80, zorder=5, marker='o')
    rect = patches.Rectangle((target_x - 0.3, target_y - 0.3), 0.6, 0.6,
                               linewidth=1.5, edgecolor='black',
                               facecolor=GATE_COLORS.get(gate, GATE_COLORS['default']), zorder=3)
    ax.add_patch(rect)
    ax.text(target_x, target_y, gate, ha='center', va='center', fontsize=8, fontweight='bold', zorder=4)

def draw_measure(ax, x, y):
    rect = patches.Rectangle((x - 0.3, y - 0.3), 0.6, 0.6,
                               linewidth=1.5, edgecolor='black',
                               facecolor=GATE_COLORS['measure'], zorder=3)
    ax.add_patch(rect)
    ax.text(x, y, 'M', ha='center', va='center', fontsize=8, fontweight='bold', zorder=4)
    ax.plot([x + 0.3, x + 0.7], [y, y + 0.3], color='black', linewidth=1)
    ax.plot([x + 0.7, x + 0.7], [y + 0.3, y + 0.4], color='black', linewidth=1)

def parse_circuit(data):
    layers = []
    current_layer = []
    for gate in data['gates']:
        if gate['type'] == 'CNOT':
            if current_layer:
                layers.append(current_layer)
                current_layer = []
            layers.append([gate])
        else:
            current_layer.append(gate)
    if current_layer:
        layers.append(current_layer)
    return layers

def draw_circuit(data, filename):
    qubits = data['qubits']
    layers = parse_circuit(data)
    n_layers = len(layers)
    n_gates = sum(len(layer) for layer in layers)
    
    fig, ax = plt.subplots(figsize=(max(10, n_gates * 1.2), max(4, qubits * 1.5)))
    
    for i in range(qubits):
        draw_qubit_line(ax, i * 2, n_layers)
        ax.text(-0.5, i * 2, f'|{i}⟩', ha='right', va='center', fontsize=10)
    
    layer_idx = 0
    for layer in layers:
        x_pos = layer_idx * 2 + 1
        
        if len(layer) == 1 and layer[0]['type'] == 'CNOT':
            gate = layer[0]
            ctrl_q = gate['control']
            target_q = gate['target']
            draw_cnot(ax, x_pos, ctrl_q * 2, x_pos, target_q * 2)
        else:
            for gate in layer:
                q = gate['qubit']
                if gate['type'] == 'H':
                    draw_single_gate(ax, 'H', x_pos, q * 2)
                elif gate['type'] == 'X':
                    draw_single_gate(ax, 'X', x_pos, q * 2)
                elif gate['type'] == 'measure':
                    draw_measure(ax, x_pos, q * 2)
                elif gate['type'] in ['RX', 'RY', 'RZ']:
                    theta = gate.get('theta', 0)
                    label = f"{gate['type']}\nθ={theta:.2f}"
                    draw_single_gate(ax, gate['type'], x_pos, q * 2, label)
                elif gate['type'] == 'P' or gate['type'] == 'U':
                    phi = gate.get('phi', 0)
                    draw_single_gate(ax, 'U', x_pos, q * 2, f'P\nφ={phi:.2f}')
                elif gate['type'] == 'R':
                    phi = gate.get('phi', 0)
                    draw_single_gate(ax, 'R', x_pos, q * 2, f'R\nφ={phi:.2f}')
                else:
                    draw_single_gate(ax, gate['type'], x_pos, q * 2)
        
        layer_idx += 1
    
    ax.set_xlim(-1, n_gates * 2 + 1)
    ax.set_ylim(-1, (qubits - 1) * 2 + 1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(data.get('name', 'Quantum Circuit'), fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Saved: {filename}")

def main(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    base_name = input_file.split('/')[-1].replace('.json', '')
    output_file = f"{base_name}_circuit.png"
    draw_circuit(data, output_file)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python circuit_diagram.py <circuit_json>")
        sys.exit(1)
    main(sys.argv[1])
