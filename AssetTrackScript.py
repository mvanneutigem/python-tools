import maya.cmds as cmds
import os.path as path

def CreateAssetTrackWindow():
    '''
    creates window for asset tracking fix
    '''
    if cmds.window('windowRep', exists=True):
        cmds.deleteUI('windowRep')
    
    windowRep = cmds.window('windowRep', title="Replace file paths", widthHeight=(350, 80))
    cmds.columnLayout( adjustableColumn=True, columnAttach=("both", 5), rowSpacing=5, columnAlign="left")
    expl = cmds.text(label="enter the new file path eg: textures or C:user/project/textures")
    newPath = cmds.textFieldGrp( label="new Path", adjustableColumn=True, columnAlign= (1,"left"))
    def enter(value):
        CallReplace(newPath)
        
    cmds.button( label='Replace paths', command=enter )
    
    cmds.showWindow( windowRep )

def CallReplace(newPath):
    '''
    CallReplace(textFieldGrp newPath)
    '''
    path = cmds.textFieldGrp(newPath, query=True, text=True)
    Replace(path)

def Replace(newPath):
    '''
    Replace(string newPath)
    replaces old file paths with given file path for all files in scene
    '''
    fileNodes = cmds.ls(type="file")
    for f in fileNodes:
        print f
        attr = "%s.fileTextureName" % f
        fullname = cmds.getAttr(attr)
        name = path.split(fullname)[-1]
        newName = path.join(newPath , name)
        cmds.setAttr(attr,newName, type="string")