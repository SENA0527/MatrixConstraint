# -*- coding: utf-8 -*-
import maya.api.OpenMaya as OpenMaya
import maya.OpenMayaMPx
import sys

kPluginNodeName = "MatrixConstraint"
kPluginNodeId = OpenMaya.MTypeId(0x87008)

def maya_useNewAPI():
    pass

class MatrixConstraint(OpenMaya.MPxNode):

    input = OpenMaya.MObject()
    offset = OpenMaya.MObject()
    parent = OpenMaya.MObject()
    rot = OpenMaya.MObject()
    sca = OpenMaya.MObject()
    tra = OpenMaya.MObject()

    def __init__(self):
        OpenMaya.MPxNode.__init__(self)

    def compute(self, plug, data):

        rotHandle = data.outputValue(MatrixConstraint.rot)
        scaHandle = data.outputValue(MatrixConstraint.sca)
        traHandle = data.outputValue(MatrixConstraint.tra)

        parentValue = data.inputValue(MatrixConstraint.parent).asMatrix().inverse()
        inputValue = data.inputValue(MatrixConstraint.input)
        inputValue = inputValue.asMatrix()
        offsetValue = data.inputValue(MatrixConstraint.offset).asMatrix()

        tMatrix = OpenMaya.MTransformationMatrix(offsetValue * inputValue * parentValue)

        if plug == MatrixConstraint.tra:

            exHandle = data.outputValue(MatrixConstraint.traArray[0])
            eyHandle = data.outputValue(MatrixConstraint.traArray[1])
            ezHandle = data.outputValue(MatrixConstraint.traArray[2])

            tra = tMatrix.translation(OpenMaya.MSpace.kTransform)

            exHandle.setDouble(tra.x)   
            eyHandle.setDouble(tra.y)   
            ezHandle.setDouble(tra.z)   
            data.setClean(plug)

        if plug == MatrixConstraint.rot:
    
            exHandle = data.outputValue(MatrixConstraint.rotArray[0])
            eyHandle = data.outputValue(MatrixConstraint.rotArray[1])
            ezHandle = data.outputValue(MatrixConstraint.rotArray[2])

            rot = tMatrix.rotation()
            euler = OpenMaya.MEulerRotation(rot[0], rot[1], rot[2],0)

            exHandle.setDouble(euler.x)   
            eyHandle.setDouble(euler.y)   
            ezHandle.setDouble(euler.z)  
            data.setClean(plug)

        if plug == MatrixConstraint.sca:
    
            exHandle = data.outputValue(MatrixConstraint.scaArray[0])
            eyHandle = data.outputValue(MatrixConstraint.scaArray[1])
            ezHandle = data.outputValue(MatrixConstraint.scaArray[2])

            scale = tMatrix.scale(OpenMaya.MSpace.kTransform)

            exHandle.setDouble(scale[0])   
            eyHandle.setDouble(scale[1])   
            ezHandle.setDouble(scale[2])   
            data.setClean(plug)

def nodeCreator():
    return MatrixConstraint()

def nodeInitializer():
    #input
    typedAttr = OpenMaya.MFnMatrixAttribute()
    MatrixConstraint.input = typedAttr.create("Input", "in")
    typedAttr.writable = True
    typedAttr.readable = False
    typedAttr.keyable = True
    typedAttr.connectable = True

    #off
    MatrixConstraint.offset = typedAttr.create("Offset", "off")
    typedAttr.writable = True
    typedAttr.readable = False
    typedAttr.keyable = True
    typedAttr.connectable = True

    #parent
    MatrixConstraint.parent = typedAttr.create("Parent", "par")
    typedAttr.writable = True
    typedAttr.readable = False
    typedAttr.keyable = True
    typedAttr.connectable = True

    #tra
    cAttr = OpenMaya.MFnCompoundAttribute()
    MatrixConstraint.tra = cAttr.create("translate", "translate")

    nAttr = OpenMaya.MFnNumericAttribute()
    MatrixConstraint.traArray = []
    MatrixConstraint.traArray = MatrixConstraint.traArray + \
        [nAttr.create("translateX", "translateX", OpenMaya.MFnNumericData.kDouble,0.0)]
    nAttr.writable = False
    nAttr.readable = True
    cAttr.addChild(MatrixConstraint.traArray[0])
    MatrixConstraint.traArray = MatrixConstraint.traArray + \
        [nAttr.create("translateY", "translateY", OpenMaya.MFnNumericData.kDouble,0.0)]
    nAttr.writable = False
    nAttr.readable = True
    cAttr.addChild(MatrixConstraint.traArray[1])
    MatrixConstraint.traArray = MatrixConstraint.traArray + \
        [nAttr.create("translateZ", "translateZ", OpenMaya.MFnNumericData.kDouble,0.0)]
    nAttr.writable = False
    nAttr.readable = True
    cAttr.addChild(MatrixConstraint.traArray[2])


    #sca
    cAttr = OpenMaya.MFnCompoundAttribute()
    MatrixConstraint.sca = cAttr.create("scale", "scale")

    nAttr = OpenMaya.MFnNumericAttribute()
    MatrixConstraint.scaArray = []
    MatrixConstraint.scaArray = MatrixConstraint.scaArray + \
        [nAttr.create("scaleX", "scaleX", OpenMaya.MFnNumericData.kDouble,1.0)]
    nAttr.writable = False
    nAttr.readable = True
    cAttr.addChild(MatrixConstraint.scaArray[0])
    MatrixConstraint.scaArray = MatrixConstraint.scaArray + \
        [nAttr.create("scaleY", "scaleY", OpenMaya.MFnNumericData.kDouble,1.0)]
    nAttr.writable = False
    nAttr.readable = True
    cAttr.addChild(MatrixConstraint.scaArray[1])
    MatrixConstraint.scaArray = MatrixConstraint.scaArray + \
        [nAttr.create("scaleZ", "scaleZ", OpenMaya.MFnNumericData.kDouble,1.0)]
    nAttr.writable = False
    nAttr.readable = True
    cAttr.addChild(MatrixConstraint.scaArray[2])

    #rotate
    cAttr = OpenMaya.MFnCompoundAttribute()
    MatrixConstraint.rot = cAttr.create("rotate", "rotate")

    nAttr = OpenMaya.MFnUnitAttribute()
    MatrixConstraint.rotArray = []
    MatrixConstraint.rotArray = MatrixConstraint.rotArray+ \
        [nAttr.create("rotateX", "rotateX", OpenMaya.MFnUnitAttribute.kAngle)]
    nAttr.writable = False
    nAttr.readable = True
    cAttr.addChild(MatrixConstraint.rotArray[0])
    MatrixConstraint.rotArray = MatrixConstraint.rotArray + \
        [nAttr.create("rotateY", "rotateY", OpenMaya.MFnUnitAttribute.kAngle)]
    nAttr.writable = False
    nAttr.readable = True
    cAttr.addChild(MatrixConstraint.rotArray[1])
    MatrixConstraint.rotArray = MatrixConstraint.rotArray + \
        [nAttr.create("rotateZ", "rotateZ", OpenMaya.MFnUnitAttribute.kAngle)]
    nAttr.writable = False
    nAttr.readable = True
    cAttr.addChild(MatrixConstraint.rotArray[2])


    #addatter
    MatrixConstraint.addAttribute(MatrixConstraint.input)
    MatrixConstraint.addAttribute(MatrixConstraint.offset)
    MatrixConstraint.addAttribute(MatrixConstraint.parent)
    MatrixConstraint.addAttribute(MatrixConstraint.rot)
    MatrixConstraint.addAttribute(MatrixConstraint.sca)
    MatrixConstraint.addAttribute(MatrixConstraint.tra)

    MatrixConstraint.attributeAffects(MatrixConstraint.input, MatrixConstraint.rot)
    MatrixConstraint.attributeAffects(MatrixConstraint.input, MatrixConstraint.sca)
    MatrixConstraint.attributeAffects(MatrixConstraint.input, MatrixConstraint.tra)
    MatrixConstraint.attributeAffects(MatrixConstraint.offset, MatrixConstraint.rot)
    MatrixConstraint.attributeAffects(MatrixConstraint.offset, MatrixConstraint.sca)
    MatrixConstraint.attributeAffects(MatrixConstraint.offset, MatrixConstraint.tra)
    MatrixConstraint.attributeAffects(MatrixConstraint.parent, MatrixConstraint.rot)
    MatrixConstraint.attributeAffects(MatrixConstraint.parent, MatrixConstraint.sca)
    MatrixConstraint.attributeAffects(MatrixConstraint.parent, MatrixConstraint.tra)


#init
def initializePlugin(mobject):
    mplugin = OpenMaya.MFnPlugin(mobject)
    try:
        mplugin.registerNode(kPluginNodeName, kPluginNodeId, nodeCreator,
                                nodeInitializer, OpenMaya.MPxNode.kDependNode,)#kPluginNodeClassify
    except:
        sys.stderr.write('Failed to register node: %s' % kPluginNodeName)
        raise

def uninitializePlugin(mobject):
    mplugin = OpenMaya.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(kPluginNodeId)
    except:
        sys.stderr.write('Failed to deregister node: %s' % kPluginNodeName)
        raise