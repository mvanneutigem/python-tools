import maya.cmds as cmds

def LoadLightControllerV2():
    '''
    LoadLightControllerV2()
    new and improved lightcontroller script, allows to change visibility, intensity and color
    directly linked to light properties, so no need to manually update
    '''    
    if cmds.window('windowRep', exists=True):
        cmds.deleteUI('windowRep')
        
    windowRep = cmds.window('windowRep', title="LightController", widthHeight=(430, 400))
    cmds.scrollLayout( )
    cmds.columnLayout("columnLayout01", adjustableColumn=True, columnAttach=("both", 5), rowSpacing=5, columnAlign="left")

    lights = cmds.ls(lights=True)
    for l in lights:
        cmds.frameLayout ( label = l, collapsable = True, parent = "columnLayout01")
        cmds.attrControlGrp( attribute='%s.visibility' % l )
        cmds.attrColorSliderGrp(at='%s.color' % l )
        cmds.attrFieldSliderGrp( min=0.0, max=10.0, at='%s.intensity' % l )
    
    cmds.showWindow( windowRep )