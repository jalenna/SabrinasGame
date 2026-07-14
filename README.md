# Sabrina's Game

An analysis of weighted matching approaches.

<center>
<img src="./resources/images/solved_board.png" alt="Solved board" width="256"/>
</center>
<center>
Solved board
</center>
<br>

In Sabrina's game, we start off with a grid of numbers. A valid cover of the
grid means that every cell in the matrix is covered by exactly one tile.
However, an invalid cover means that not all cells are covered. The objective of
the game is to create a valid cover where the summed objective value of all
tiles is lowest. The value of a tile is the difference between the largest and
the smallest value covered by the tile.

# Description

This repo contains 3 algorithms that solve Sabrina's game:

- Minimum Cost Maximum Flow (MCMF)
- Depth First Search (DFS)
- Convolutional Neural Network (CNN) Guided DFS

# Installation

Create a virtual environment and run: `pip install -r requirements.txt`

# Usage

All algorithms are located in the [algorithms](./src/algorithms/) folder.

You can edit the [config.py](./src/algorithms/utils/config.py) and ml
[config.py](./src/algorithms/ml/config.py) files to your needs.

Make sure to train the guided model first before using it:
`python -m src.algorithms.ml.train`

Take a look at the [core.py](./src/algorithms/utils/core.py) file too to get a
better understanding of the code structure.

Your solutions can be verified with the `solution_verifier` located in the
[verifier.py](./src/algorithms/utils/verifier.py) file.

You can evaluate the models using the `evaluate` function in the
[eval.py](./src/algorithms/utils/eval.py) file. Just uncomment the last few
lines, or import it in your own main function.

# License

Copyright 2026 Jalen

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
