The user provides the stages in a JSON file.

* qubits : integer – the number of qubits in the system.
The state vector must have length 2qubits2qubits.

* stages : array of stage objects. Each stage has:
  - name : string – a descriptive label (e.g., "After Hadamard on q0").
  - state_vector : array of complex amplitudes. Amplitudes can be given in any of the following forms:
    * Real number: 0.7071
    * Complex number as a string: "0.7071+0.7071j"
    * Complex number as an array [real, imag]: [0.7071, 0.7071]

The program assumes the computational basis order is big‑endian (i.e., the most significant qubit is the leftmost bit in the ket label). The state vector must be normalized (the program will not renormalize automatically).
