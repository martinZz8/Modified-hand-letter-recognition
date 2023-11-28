This script shifts skeletons from "input" folder, to have it's COG (central of gravity) in point (0,0).
Shifted skeletons are saved in "output" folder.

Output data can then be used to train PyTorch models using "Python-train-model" script.
There is better performance in models learned on shifted models than on original ones.