import maya.cmds as cmds
from functools import partial

class obj(object):
    def __init__(self, name):
        self.name = name
        self.attr = {}#dctionary of keyable attributes
        
    def AddAttr(self, attr, value):
        self.attr[attr] = value

class keyGroup(object):
    def __init__(self, name):
        self.name = name
        self.keys = []
        
    def GetName(self):
        return self.name
        
    def AddKey(self, key):
        self.keys.append(key)

keyGroups = []
def ShowGroups():
    def update(g, *args):
        keyGroups.remove(g)
    for g in keyGroups:
        cmds.frameLayout ( label = g.GetName(), collapsable = True, parent = "columnLayout01")
        cmds.button( label='delete', command=partial(update,g))

def LoadKeySaver():
    if cmds.window('windowRep', exists=True):
        cmds.deleteUI('windowRep')
        
    windowRep = cmds.window('windowRep', title="KeySaver", widthHeight=(200, 400))
    cmds.scrollLayout( )
    cmds.columnLayout("columnLayout01", adjustableColumn=True, columnAttach=("both", 5), rowSpacing=5, columnAlign="left")
    
    def AddKeyGroup(value1):
        #get selected group and save transforms
        keyList = []
        keys = cmds.ls(sl=1, type='transform')
        print keys
        for k in keys:
            o = obj(k)
            print k
            attributes = cmds.listAttr(k, k=True)
            for a in attributes:
                print a
                attr = k + '.' + a
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
            ShowGroups()
        
        nameVal = cmds.textFieldGrp(adjustableColumn=True, changeCommand=closeWindow, label='name')
        cmds.showWindow( winName )
    
    cmds.button( label='add keygroup', command=AddKeyGroup)
            
    ShowGroups()
    
    cmds.showWindow( windowRep )