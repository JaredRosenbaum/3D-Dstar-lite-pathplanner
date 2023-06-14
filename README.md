# D* Lite incremental pathplanning algorithm for robotics
### Implementation of the D* lite algorithm for pathplanning in Python and eventually also C++
[![version](https://img.shields.io/badge/version-1.0.1-blue)](https://github.com/JaredRosenbaum/3D-Dstar-lite-pathplanner/releases/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/JaredRosenbaum/3D-Dstar-lite-pathplanner/graphs/commit-activity)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/Sollimann/d-star-lite.svg)](https://github.com/JaredRosenbaum/3D-Dstar-lite-pathplanner/pulls)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


<p align="center">
  <img src="https://github.com/JaredRosenbaum/3D-Dstar-lite-pathplanner/blob/master/docs/D_star_lite_demo3.gif">
</p>


This software is an extended implementation of the D*-Lite algorithm as explained in [Koenig, 2002](http://idm-lab.org/bib/abstracts/papers/aaai02b.pdf). The D* Lite algorithm was developed by Sven Koenig and Maxim Likhachev for a faster more lightweight alternative to the Dynamic A* algorithm (developed by Anthony Stentz in 1995). The express purpose of this version of the algorithm is to allow for 3D navigation on a grounded robot, leading to an added cost function preventing the robot from targetting voxels without a "floor" below them.

## Dependencies
* pip install pygame
* pip install numpy

## install poetry package mananger and virtual env (or use pipenv):
you can use pipenv or [poetry](https://www.pythoncheatsheet.org/blog/python-projects-with-poetry-and-vscode-part-1/) to active virtual env.
```
$ pip install poetry
$ cd /d-star-lite/python
$ poetry install
$ poetry shell
$ python main.py
```

### Commands
* [Space] - move robot along line
* [left click] - place obstacle
* [right click] - remove obstacle
* s_start, s_goal and view range can be changed in main.py

### The cell colors are as follows:
* Red - shortest path
* Green - goal vertex
* grey - obstacle
* light grey - floor (occupied space below the robot)
* white - unoccupied space (both at the Z level of and 1 below the robot)


## Pseudo code, D* Lite optimized version
![D* Lite optimized](docs/pseudocode.png)

## References:
Improved Fast Replanning for Robot Navigation in Unknown Terrain<br>
Sven Koenig, Maxim Likhachev<br>
Technical Report GIT-COGSCI-2002/3,<br>
Georgia Institute of Technology, 2002.

