maze-solver
===========

This solves the "impossible" maze from mazes.org.uk.

Reads the image and creates a 2d-list which gets searched with a bfs search.
Outputs the solution and the path found to stdout when running and creates two images.
Can quite easily be changed to solving for another image. Simply change the filename and the
start and end coordinates in the top of the script.

Dependencies
------------

Python 2.7 and Pillow. I use a fork of PIL called Pillow. Not sure if it works under PIL as well.

	pip install --user Pillow # under Linux/OSX
