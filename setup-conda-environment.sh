#!/bin/bash

echo "Note: make sure you have the 'brian-team' channel added to your $HOME/.condarc config file!"
conda create --name bb python=3.6 brian2 matplotlib pandas
source activate bb
# then

pip install jsonpickle pyyaml
