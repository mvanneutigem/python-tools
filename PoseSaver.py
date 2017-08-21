import maya.cmds as cmds
import os
from functools import partial

#point this path to a folder where you want to save icons/savefiles on your computer -->
path = "C:/Users/Marieke/Documents/DAE/summer/niels/icons/"

if not os.path.exists(path):
    os.makedirs(path)#create folder if not exists

class obj(object):
    def __init__(self, name):
        self.name = name
        self.attr = {}#dictionary of keyable attributes
        
    def GetName(self):
        return self.name
        
    def AddAttr(self, attr, value):
        self.attr[attr] = value
    
    def SetAttr(self):
        for attr, value in self.attr.items():#loop over dictionary and save values
            fullAttr = self.name + '.' + attr
            cmds.setAttr(fullAttr, value)
            
    def GetAttrs(self):
        return self.attr

class keyGroup(object):
    def __init__(self, name):
        self.name = name
        self.keys = []
        
    def GetName(self):
        return self.name
        
    def AddKey(self, key):
        self.keys.append(key)
        
    def SetKeys(self):
        for key in self.keys:
            key.SetAttr()
            
    def GetKeys(self):
        return self.keys

keyGroups = []

def ShowGroup(g):
    def set(g, *args):
        g.SetKeys()
    def remove(g, *args):
        for k in g.GetKeys():
            k.GetAttrs().clear()
        g.GetKeys()[:]=[]
        keyGroups.remove(g)
        #TODO: delete associated image in icons folder
        cmds.deleteUI(setpose)
        cmds.deleteUI(remove)
        cmds.deleteUI(title)

    name = g.GetName()
    title = cmds.frameLayout ( name, collapsable = True, parent = "columnLayout01")
    fullPath = path + name + ".png"
    setpose = cmds.iconTextButton( style='iconOnly', image1=fullPath, label='set pose', command=partial(set,g) )
    remove = cmds.button( label='delete', command=partial(remove,g))
    
def ShowGroups():
    for g in keyGroups:
        ShowGroup(g)

def LoadPoseSaver():
    '''
    Call this function to launch pose saver, 
    make sure you have set up your icon path before attempting to use this script.
    Click add pose to add currently selected controllers to the saved pose
    Click load setup to load previously saved poses from file 
    Click save setup to save current poses to file
    '''
    if cmds.window('windowRep', exists=True):
        cmds.deleteUI('windowRep')
        
    windowRep = cmds.window('windowRep', title="PoseSaver", widthHeight=(200, 400))
    cmds.scrollLayout( )
    cmds.columnLayout("columnLayout01", adjustableColumn=True, columnAttach=("both", 5), rowSpacing=5, columnAlign="left")
    
    def AddKeyGroup(value1):
        #get selected group and save transforms
        keyList = []
        keys = cmds.ls(sl=1, type='transform')
        print keys
        for k in keys:
            o = obj(k)
            attributes = cmds.listAttr(k, k=True)
            for a in attributes:
                attr = k + '.' + a
                value = cmds.getAttr(attr)
                if type(value) is float:
                    o.AddAttr(a, cmds.getAttr(attr))
            keyList.append(o)
        
        #name group
        if cmds.window('winName', exists=True):
            cmds.deleteUI('winName')
        winName = cmds.window('winName', title="name group", widthHeight=(400, 20))
        cmds.columnLayout("columnLayout02", adjustableColumn=True, columnAttach=("both", 5), rowSpacing=5, columnAlign="left")
        
        def closeWindow(value1):
            name = cmds.textFieldGrp( nameVal, query=True, text=True)
            gr = keyGroup(name)
            for k in keyList:
                gr.AddKey(k)
            keyGroups.append(gr)
            cmds.deleteUI('winName')
            
            #screenshot from viewport
            oldFormat = cmds.getAttr("defaultRenderGlobals.imageFormat")
            cmds.setAttr("defaultRenderGlobals.imageFormat", 32)
            fullPath = path + name + ".png"
            cmds.playblast(completeFilename=fullPath,frame=cmds.currentTime(query=True),format="image", widthHeight = (512,256), quality=100, showOrnaments=False)
            cmds.setAttr("defaultRenderGlobals.imageFormat", oldFormat)
            
            ShowGroup(gr)
        
        nameVal = cmds.textFieldGrp(adjustableColumn=True, changeCommand=closeWindow, label='name')
        
        cmds.showWindow( winName )
    
    cmds.button( label='add pose', command=AddKeyGroup)
    
    def LoadSetup(filename):
        #load previous saved setup from file   
        counter = 0            
        readFile = open(path + filename + ".txt", "r")
        if readFile.readline() != "POSESAVER\n":
            print "error expected POSESAVER"
            return
        nrOfGroups = int(float(readFile.readline()))
        print str(nrOfGroups)
        groupCounter = 0
        while groupCounter < nrOfGroups:
            groupname = readFile.readline().strip('\n')
            nrOfKeys = int(float(readFile.readline()))
            keyList = []
            
            keyCounter = 0
            while keyCounter < nrOfKeys:
                keyname = readFile.readline().strip('\n')
                print keyname
                nrOfAttrs = int(float(readFile.readline()))
                o = obj(keyname)
                
                attrCounter = 0
                while attrCounter < nrOfAttrs:
                    attrString = readFile.readline()
                    attrList = attrString.split(' ', 1 )
                    o.AddAttr(attrList[0], float(attrList[1]))
                    attrCounter += 1
                    
                keyList.append(o)
                keyCounter +=1
                
            gr = keyGroup(groupname)
            for k in keyList:
                gr.AddKey(k)
            keyGroups.append(gr)
            groupCounter += 1
        ShowGroups()
        
    
    def LoadSetupPrompt(value1):
        if cmds.window('winName', exists=True):
            cmds.deleteUI('winName')
        winName = cmds.window('winName', title="name group", widthHeight=(400, 50))
        cmds.columnLayout("columnLayout02", adjustableColumn=True, columnAttach=("both", 5), rowSpacing=5, columnAlign="left")
        
        def closeWindow(value1):
            filename = cmds.textFieldGrp( nameVal, query=True, text=True)
            cmds.deleteUI('winName')
            LoadSetup(filename)
            
        expl = cmds.text(label="enter the filename to open the setup from eg: handposes")
        nameVal = cmds.textFieldGrp(adjustableColumn=True, changeCommand=closeWindow, label='name')
        cmds.showWindow( winName )

    
    cmds.button( label='load setup', command=LoadSetupPrompt)
    
    def SaveSetup(filename):
        #write current setup to file
        savefile = open(path + filename + '.txt', 'w')
        savefile.write('POSESAVER\n')
        savefile.write(str(len(keyGroups)) + '\n')#nrofgroups
        for kGroup in keyGroups:
            savefile.write(kGroup.GetName() + '\n')#groupname
            keys = kGroup.GetKeys()
            savefile.write(str(len(keys)) + '\n')#nrofkeys
            for k in keys:
                savefile.write(k.GetName() + '\n')#keyname
                attrs = k.GetAttrs()
                savefile.write(str(len(attrs)) + '\n')#nrofattrs
                for attr, value in attrs.items():
                    savefile.write(attr + ' ' + str(value) + '\n')#attr value
                
        savefile.close()
        
    def CreateSetupPrompt(value1):
        if cmds.window('winName', exists=True):
            cmds.deleteUI('winName')
        winName = cmds.window('winName', title="name group", widthHeight=(400, 50))
        cmds.columnLayout("columnLayout02", adjustableColumn=True, columnAttach=("both", 5), rowSpacing=5, columnAlign="left")
        
        def closeWindow(value1):
            filename = cmds.textFieldGrp( nameVal, query=True, text=True)
            cmds.deleteUI('winName')
            SaveSetup(filename)
        expl = cmds.text(label="enter the filename to save the setup to eg: handposes")
        nameVal = cmds.textFieldGrp(adjustableColumn=True, changeCommand=closeWindow, label='name')
        cmds.showWindow( winName )
    
    cmds.button( label='save setup', command=CreateSetupPrompt)
    
    ShowGroups()
    
    cmds.showWindow( windowRep )