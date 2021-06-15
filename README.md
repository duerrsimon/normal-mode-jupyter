# Visualize Normal Modes in Jupter Notebook

Simple helper function to visualize molden files containing normal modes using `3Dmol.js` and
`psi4`. 

![Demonstration](./NormalModes.mov)

# Installation

`pip install py3Dmol`

# How to use

You can generate the normal modes e.g using psi4 

`psi4 hooh.dat`

psi4 writes a molden formatted file with the normal modes if the setting `write_normal_modes` is `true`. 

