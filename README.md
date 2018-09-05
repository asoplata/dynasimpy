
# dynasimpy-alpha
Preliminary dynaSimPy development repo pre-packaging
This repo will eventually be deprecated once I figure out how to properly
develop Python packages, including separating the package code from the
run/debug code. The contents of the subfolder `dynasimpy` will eventually go on
to become its own package, while everything else is run/debug code for this
future package.
Notes and plans for this project are in the `s6-python-dynasimpy.org` file.
`dynasimpy` is intended to be an "interface" for the deploying the power of the
[DynaSim simulator](https://github.com/dynasim/dynasim/wiki), but using the
([Brian 2 simulator](http://brian2.readthedocs.io/en/stable/) as its core
engine. In other words, this is an attempt to bring DynaSim's mechanism
modularity, parameter sweeping, and batch job distribution to Brian 2.
