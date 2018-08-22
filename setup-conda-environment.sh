#!/bin/bash

# Create a new conda environment called "bb":
conda create --name bb python=3.6

# Now let's add the "conda-forge" "channel" to your Anaconda install:
conda config --add channels conda-forge

# Now let's go inside the environment
source activate bb

# Your terminal prompt should now say "(bb)" at the beginning. If you
# want to test that you're in the environment, run:
which python
# ...and it should say you're running the python interpreter from your
# new environment's "bin" directory.

# Now that we're inside the environment, let's install some packages:
pip install cython ipython jupyter matplotlib nose pandas sympy

# Since we've added the "conda-forge" channel, we can install brian2 the
# same way:
pip install brian2

# dynasimpy-specific packages:
pip install jsonpickle pyyaml
