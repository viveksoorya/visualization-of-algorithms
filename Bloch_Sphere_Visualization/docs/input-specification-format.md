Input Specification Format

## Usage

Run the program from the command line:

    python program.py <input-file>

The program reads stages from the input file and saves the visualization to a PNG file with the same name as the input file (e.g., `grover_N16.txt` → `grover_N16.png`).

## Input Formats

The user provides a list of stages, where each stage describes the state of the qubit. The input can be given in one of the following formats (case‑insensitive):

    Ket notation – e.g., |0>, |1>, |+>, |->, |+i>, |-i>

    Complex coefficients – two complex numbers (alpha, beta) representing the state α|0⟩ + β|1⟩.
    Format: (a+bi, c+di) or (a,b) if imaginary parts are zero.

    Bloch angles – the polar angle θ (from +z axis) and azimuthal angle φ.
    Format: theta=1.047, phi=0.785 (angles in radians) or theta=60, phi=45 with a unit specifier deg.

    Bloch vector – the Cartesian coordinates (x,y,z) of the Bloch vector.
    Format: (0,0,1) for |0⟩.

The program accepts input either from a text file (one stage per line) or directly from a list defined in the code. Comments (starting with #) and empty lines are ignored.
