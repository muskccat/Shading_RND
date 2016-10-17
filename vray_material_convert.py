## Vray Material to PxrDisney Material Convert
##
## 2016.08.17


import maya.cmds as cmds
hi_sels = cmds.ls(typ="VRayMtl")


for x in hi_sels:

    cs = x+".color"                                 # texture attr
    os = x+".outColor"                              # sha45ding group connecte location
    bs = cmds.getAttr(x+".color")                   # Cs value
    bl = cmds.connectionInfo(cs, id=True)           # color attr texture connection check

    outl = cmds.connectionInfo(os, isSource=True)
    
    outc = cmds.connectionInfo(os, dfs=True)
        
    if outl:
        
        vs = cmds.shadingNode("PxrDisney", asShader=True, n = x)
        #lt = cmds.shadingNode("layeredTexture", asTexture=True, n = x+"_layeredTexture")
        
       
        x = outc[0].split(".")
        x = x[0]
        cmds.disconnectAttr(os, outc[0])
        cmds.connectAttr(vs+".outColor", outc[0])
        
        if bl :
            
            c_name = cmds.connectionInfo(cs, sfd=True)
            cmds.connectAttr(c_name,  vs+".baseColor")
                    
            
        else : 
            
            bs = bs[0]
            cmds.setAttr( vs + ".baseColor", bs[0], bs[1], bs[2])