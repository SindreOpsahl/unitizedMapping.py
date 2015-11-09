# unitizedMapping v0.1
# ---
# by Sindre Opsahl Skaare
# sindre.opsahl@gmail.com
# sindre-skaare.squarespace.com
# ---
#
# A simple script for UV mapping long curved surfaces like tubes, ribbons, branches, etc, into a straight shell.
# Use with directional unfolding for the best and fastest results.
#
# To use, run this Python command:
#
# import unitizedMapping
# unitizedMapping.run()
#
# If you have meshes selected it will use the existing UV seams, and map multiple meshes individually
# If you have edges selected it will use them as the new UV seams
# If you have faces selected it will use the existing UV seams, but only map the connected shell. This is for mapping submeshes, without altering the UV's of the rest of the mesh.

import maya.cmds as cmds
from maya.mel import eval

def run():
	#begin undo chunk, so all steps below count as one action
	cmds.undoInfo(openChunk=True)

	#check if selection is edges
	if cmds.filterExpand(selectionMask=32):
		#run the mapping procedure 
		unitizeAndSew()

	#check if selection is meshes
	elif cmds.filterExpand(selectionMask=12): 
		#if you have multiple meshes selected, map each in turn
		for mesh in cmds.ls(selection=True):
			#make sure only one mesh is selected
			cmds.select(mesh)
			#select the existing UV seams
			eval("ConvertSelectionToUVs")
			eval("polySelectBorderShell 1")
			#run the mapping procedure
			unitizeAndSew()

	#check if selection is faces
	elif cmds.filterExpand(selectionMask=34):
		#select the existing UV seams on the connected UV shells
		eval("ConvertSelectionToUVs")
		eval("polySelectBorderShell 1")
		#run the mapping procedure
		unitizeAndSew()

	else:
		#error if not correct selection 
		cmds.warning("Selection is not an edge, face, or object!")


	#end undo chunk
	cmds.undoInfo(closeChunk=True)

def unitizeAndSew():
	# store UV seam as vertex becase fuck you Maya
	eval("PolySelectConvert 3")
	vtx_seam = cmds.ls(selection=True)
	eval("PolySelectConvert 4")

	#select UV shell, and convert to faces and unitize
	eval("polySelectBorderShell 0")
	eval("PolySelectConvert 1")
	cmds.polyForceUV(unitize=True)

	#convert shell to vertex and subtract the stored vertex seam, and then convert back to UV, because fuck you Maya
	eval("PolySelectConvert 3")
	cmds.select(vtx_seam, deselect=True)
	eval("PolySelectConvert 4")

	#stitch together the UV's that are not by the seam
	cmds.polyMapSewMove()