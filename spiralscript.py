import maya.cmds as cmds

def CreateSpiral(height, degreeStep, NrOffBalls, radius):
    '''
    CreateSpiral(float height, float degreeStep, int NrOffBalls, float radius)
    creates a spiral of balls
    '''
    degrees = 0
    h = height/NrOffBalls
    for i in range(NrOffBalls):
        thisName = "SpiralSphere_%s" % i
        parts = cmds.sphere(name=thisName, pivot=[radius, h*i, 0])
        transform = parts[0]
        rotY = transform + ".rotateY"
        cmds.setAttr(rotY, degrees)
        degrees += degreeStep
        degrees = degrees%360
        
def CreateSpiralWindow():
    '''
    creates window for creating spiral, with ui to change variables
    '''
    window = cmds.window( title="Create Spiral", widthHeight=(200, 300))
    cmds.columnLayout( columnAttach=('both', 5), rowSpacing=5,adjustableColumn=True)
    height = cmds.floatFieldGrp( numberOfFields=1, label='height', value1=10.0)
    degreeStep = cmds.floatFieldGrp( numberOfFields=1, label='degreeStep', value1=30.0)
    NrOffBalls = cmds.intFieldGrp( numberOfFields=1, label='NrOffBalls', value1=20)
    radius = cmds.floatFieldGrp( numberOfFields=1, label='radius', value1=3)

    def click(value):
        doCreateSpiral(height, degreeStep, NrOffBalls, radius)
        
    cmds.button( label='Create Spiral!', command=click )
    
    closeCmd = 'cmds.deleteUI("%s", window=True)' % window
    cmds.button( label='Close', command=closeCmd )
    
    cmds.showWindow( window )
    
def doCreateSpiral(height, degreeStep, NrOffBalls, radius):

    heightVal = cmds.floatFieldGrp(height, query=True, value1=True)
    degreeStepVal = cmds.floatFieldGrp(degreeStep, query=True, value1=True)
    NrOffBallsVal = cmds.intFieldGrp(NrOffBalls, query=True, value1=True)
    radiusVal = cmds.floatFieldGrp(radius, query=True, value1=True)
    
    CreateSpiral(heightVal, degreeStepVal, NrOffBallsVal, radiusVal)