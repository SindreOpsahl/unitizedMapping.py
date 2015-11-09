# unitizedMapping.py
A Maya Python script that makes unwrapping curved tubes and other cylindrical objects easy.
A simple script for UV mapping long curved surfaces like tubes, ribbons, branches, etc, into a straight shell.
Use with directional unfolding for the best and fastest results.

To use, run this Python command:

import unitizedMapping
unitizedMapping.run()

If you have edges selected it will use them as the new UV seams.

If you have meshes selected it will use the existing UV seams, and map multiple meshes individually.

If you have faces selected it will use the existing UV seams, but only map the connected shell. This is for mapping submeshes, without altering the UV's of the rest of the mesh.
