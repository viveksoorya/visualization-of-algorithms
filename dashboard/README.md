# Quantum Algorithm Visualization Dashboard

An interactive web dashboard for visualizing quantum algorithms with Qiskit integration for real quantum hardware.

## Features

- **Interactive Visualizations**: Bloch Sphere, Probability Distribution, Density Matrix
- **Multiple Algorithms**: Grover's Search, QFT, QAOA, VQE
- **Real Hardware Support**: Run on IBM Quantum devices
- **Animation**: Animate algorithm stages
- **Scalable**: Support for 2-4 qubits

## Quick Start

### Option 1: Standalone HTML (No Installation Required)

Simply open the HTML file in a browser:

```bash
cd dashboard/frontend
python -m http.server 8080
# Open http://localhost:8080
```

### Option 2: Full API with Qiskit

1. Install dependencies:

```bash
cd dashboard/api
pip install -r requirements.txt
```

2. Run the server:

```bash
python main.py
# Opens at http://localhost:8000
```

## Usage

### Web Interface

1. Select an algorithm (Grover's, QFT, QAOA, VQE)
2. Choose number of qubits (2-4)
3. View Bloch Sphere and probability distribution
4. Click "Animate" to see algorithm stages
5. Optionally run on real quantum hardware

### API Endpoints

```bash
# Visualize a state vector
POST /api/visualize
{
  "qubits": 2,
  "stages": [{"name": "Test", "state": [1, 0, 0, 0]}]
}

# Run on quantum hardware
POST /api/run-hardware
{
  "qubits": 2,
  "backend": "ibmq_qasm_simulator",
  "token": "your_ibm_token",
  "shots": 1024
}

# Health check
GET /api/health

# List available backends
GET /api/backends
```

## Running on Real Quantum Hardware

1. Get an IBM Quantum API token from [quantum-computing.ibm.com](https://quantum-computing.ibm.com)
2. Enter your token in the dashboard
3. Select a backend (e.g., `ibmq_quito`, `ibmq_bogota`)
4. Click "Run on Hardware"

## Project Structure

```
dashboard/
├── api/
│   ├── main.py           # FastAPI backend
│   ├── requirements.txt  # Python dependencies
│   └── results/          # Hardware execution results
├── frontend/
│   └── index.html       # Standalone web interface
├── static/
│   └── results/         # Generated visualizations
└── README.md
```

## Requirements

- Python 3.8+
- For full functionality:
  - `pip install fastapi uvicorn`
  - `pip install qiskit qiskit-ibm-runtime`
- For visualization: Internet connection (loads Plotly.js from CDN)

## Algorithm Details

### Grover's Search
- Oracle-based algorithm for database search
- Shows amplitude amplification across stages
- Bloch Sphere shows rotation toward target state

### Quantum Fourier Transform (QFT)
- Transform-based algorithm for frequency analysis
- Phase periodicity visible in density matrix
- State City reveals periodic phase patterns

### QAOA (Quantum Approximate Optimization)
- Variational algorithm for combinatorial optimization
- Parameter evolution visible across stages
- Cost landscape shows optimization surface

### VQE (Variational Quantum Eigensolver)
- Finds ground state energies
- Parameter optimization visible
- Energy landscape shows minimization

## License

MIT License
