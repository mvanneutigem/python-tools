mirrorPose('X', True)

#mirrorpose script
#example call: mirrorPose('X', True)
import maya.cmds as cmds

class obj(object):
    def __init__(self, name):
        self.name = name
        self.attr = {}#dictionary of keyable attributes
        
    def GetName(self):
        return self.name
        
    def AddAttr(self, attr, value):
        self.attr[attr] = value
            
    def GetAttrs(self):
        return self.attr

def mirrorPose(axis, flipRot):
    '''
    mirrorPose(string axis, bool flipRot)
    axis is the axis to mirror on eg: 'X' or 'Y'
    flipRot is whether to invert rotations on the rig, True or False
    call to mirror currently selected controllers
    '''
    keyList = []
    keys = cmds.ls(sl=1, type='transform')
    for k in keys:
        o = obj(k)
        attributes = cmds.listAttr(k, k=True)
        for a in attributes:
            attr = k + '.' + a
            value = cmds.getAttr(attr)
            if type(value) is float:
                o.AddAttr(a, cmds.getAttr(attr))
        keyList.append(o)
            

    for k in keyList:
        attributes = k.GetAttrs()
        prefix = k.GetName()[:2]
        if prefix == 'R_':
            newk = 'L_' + k.GetName()[2:]
            print 'new: ' +newk
            for a, value in attributes.items():
                attr = k.GetName() + '.' + a
                postfix = attr[-1:]
                print 'post ' + postfix
                if postfix != axis:
                    if type(value) is float:
                        newattr = newk + '.' + a
                        if flipRot:
                            rotString = attr[-7:-1]
                            print 'rotstring ' + rotString
                            if rotString == 'rotate':
                                cmds.setAttr(newattr, -value)
                            elif rotString == 'nslate':
                                cmds.setAttr(newattr, value)
                        else:
                            cmds.setAttr(newattr, value)
                else:
                    if type(value) is float:
                        newattr = newk + '.' + a
                        if flipRot:
                            rotString = attr[-7:-1]
                            print 'rotstring ' + rotString
                            if rotString == 'rotate':
                                cmds.setAttr(newattr, -value)
                            elif rotString == 'nslate':
                                cmds.setAttr(newattr, -value)
                        else:
                            cmds.setAttr(newattr, value)
        elif prefix == 'L_':
            newk = 'R_' + k.GetName()[2:]
            print 'new: ' +newk
            for a, value in attributes.items():
                attr = k.GetName() + '.' + a
                postfix = attr[-1:]
                print 'post ' + postfix
                if postfix != axis:
                    if type(value) is float:
                        newattr = newk + '.' + a
                        if flipRot:
                            rotString = attr[-7:-1]
                            print 'rotstring ' + rotString
                            if rotString == 'rotate':
                                cmds.setAttr(newattr, -value)
                            elif rotString == 'nslate':
                                cmds.setAttr(newattr, value)
                        else:
                            cmds.setAttr(newattr, value)
                else:
                    if type(value) is float:
                        newattr = newk + '.' + a
                        if flipRot:
                            rotString = attr[-7:-1]
                            print 'rotstring ' + rotString
                            if rotString == 'rotate':
                                cmds.setAttr(newattr, -value)
                            elif rotString == 'nslate':
                                cmds.setAttr(newattr, -value)
                        else:
                            cmds.setAttr(newattr, value)