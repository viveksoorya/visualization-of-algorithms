Limitations

    Exponential scaling: The density matrix size grows as 2n×2n2n×2n. For n>5n>5 qubits, the plots become overcrowded and the computation may become memory‑intensive.

    Pure states only: The program builds the density matrix from a state vector; it does not accept general mixed states (although a user could provide a full density matrix by extending the format).

    Basis ordering: The computational basis order is fixed to big‑endian. This must match the user’s interpretation of the state vector entries.

    No phase information in color: The current coloring only distinguishes sign (positive/negative). Phase is only indirectly visible via the real/imag split.

    Static images: The program saves separate PNG files; it does not create animations or interactive views.

    Normalization: The user must supply normalized state vectors; the program does not check or enforce this.


Despite these limitations, the tool provides a clear, intuitive visualization of how quantum states evolve through an algorithm, making it useful for small‑scale demonstrations and educational purposes.
