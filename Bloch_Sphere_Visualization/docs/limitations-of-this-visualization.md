Limitations

*Single‑qubit only* – The Bloch sphere represents the state of exactly one qubit. Multi‑qubit states cannot be visualized directly.

*Pure states only* – The standard Bloch sphere surface corresponds to pure states. Mixed states (points inside the sphere) are not handled, though the code could be extended to plot interior points.

*Normalization assumed* – Input states that are not normalized will be normalized automatically, but the original amplitudes are lost.

*No gate evolution* – The user must explicitly provide the state after each stage. The program does not simulate the action of quantum gates.

*Static visualization* – The spheres are rendered as a static grid of images saved to a file (bloch_sphere_visualization.png); there is no interactive animation or real-time exploration of the stages.

*Limited error checking* – Parsing is basic and may fail for unusual formatting. The program expects correct input and may raise unhandled exceptions.

*Mathematical representation* – Phase differences are handled, but global phase is ignored (as it should be for the Bloch sphere).

*Scalability* – Many stages will produce a crowded grid of small spheres, making details hard to see.

Despite these limitations, the tool provides a quick and intuitive way to inspect the evolution of a qubit’s state through the stages of a quantum algorithm.
