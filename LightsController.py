import maya.cmds as cmds
from functools import partial

def makeLightController():
    ctrl = LightController()
    ctrl.LoadLightController()
    
class Light(object):
    def __init__(self, light):
        self.light = light
        self.intensity = 1.0
        self.colorR = 1.0
        self.colorG = 1.0
        self.colorB = 1.0
        
    def SetFields(self):
        self.intensityField = cmds.floatFieldGrp( label="intensity", adjustableColumn=True, columnAlign= (1,"left"))
        print self.intensityField
        self.colorField = cmds.colorSliderGrp( label="color", adjustableColumn=True, columnAlign= (1,"left"))
        
    def GetName(self):
        return self.light
        
    def GetIntensityField(self):
        return self.intensityField
        
    def GetColorField(self):
        return self.colorField
        
    def SetIntensity(self, intensity):
        print "intensity" + str(intensity)
        self.intensity = intensity
        print "self intensity" + str(self.intensity)
        
    def SetColor(self, R,G,B):
        self.colorR = R
        self.colorG = G
        self.colorB = B
        
    def Update(self):
        myAttr =  self.light + ".intensity"
        print "update intensity" + str(self.intensity)
        cmds.setAttr(myAttr, self.intensity)
        myAttr =  self.light + ".colorR"
        cmds.setAttr(myAttr, self.colorR)
        myAttr =  self.light + ".colorG"
        cmds.setAttr(myAttr, self.colorG)
        myAttr =  self.light + ".colorB"
        cmds.setAttr(myAttr, self.colorB)
        
class LightController(object):
    def __init__(self):
        self.lights = []
    def LoadLightController(self):
        '''
        LightController()
        only works with standard maya lights so far
        '''
        self.lights = cmds.ls(lights=True)
        
        lightsList = []
        for l in self.lights:
            light= Light(l)
            lightsList.append(light)
            
        if cmds.window('windowRep', exists=True):
            cmds.deleteUI('windowRep')
    
        windowRep = cmds.window('windowRep', title="LightController", widthHeight=(430, 400))
        cmds.scrollLayout( )
        cmds.columnLayout("columnLayout01", adjustableColumn=True, columnAttach=("both", 5), rowSpacing=5, columnAlign="left")
        
        def update(light, *args):
            print light
            print light.GetIntensityField()
            i = cmds.floatFieldGrp(light.GetIntensityField(), query=True, value1=True)
            print i
            r,g,b = cmds.colorSliderGrp(light.GetColorField(),query=True, rgbValue=True)
            light.SetColor(r,g,b)
            light.SetIntensity(i)
            light.Update()
        
        index = 0;
        for l in lightsList:
            cmds.frameLayout ( label = l.GetName(), collapsable = True, parent = "columnLayout01")
            #expl = cmds.text(label=l.GetName())
            l.SetFields()
            cmds.button( label='update', command=partial(update,l))
            ++index
        
    
        cmds.showWindow( windowRep )