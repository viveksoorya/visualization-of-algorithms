Program Design

The program consists of the following components:

    Parser – converts the textual description of each stage into a normalized Bloch vector (x, y, z).

    Bloch sphere drawer – creates a 3D matplotlib figure with a sphere, coordinate axes, and an arrow pointing to the state on the sphere’s surface.

    Main loop – reads the stages, computes the Bloch vectors, and creates a grid of subplots (one per stage).

The code is modular so that new input formats can be added easily.
