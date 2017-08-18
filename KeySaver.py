import maya.cmds as cmds

def LoadKeySaver():
    if cmds.window('windowRep', exists=True):
        cmds.deleteUI('windowRep')
        
    windowRep = cmds.window('windowRep', title="KeySaver", widthHeight=(200, 400))
    cmds.scrollLayout( )
    cmds.columnLayout("columnLayout01", adjustableColumn=True, columnAttach=("both", 5), rowSpacing=5, columnAlign="left")
    cmds.showWindow( windowRep )