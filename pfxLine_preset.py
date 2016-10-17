import maya.cmds as cmds

def r_init(*args):
    
    nPfx = cmds.ls(typ='pfxToon')
    
    for x in nPfx:
        
        obj = x
        n = cmds.nodeType(obj)
        if (n == "pfxToon"):
        
            # Attribute name var
            obj_disp        = obj + ".displayInViewport"
            obj_border      = obj + ".borderLines"
            obj_int         = obj + ".intersectionLines"
            obj_lw          = obj + ".lineWidth"
            obj_thin        = obj + ".lineEndThinning"
            obj_oc          = obj + ".occlusionWidthScale"
            obj_tight       = obj + ".tighterProfile"
            obj_borderMod   = obj + ".borderWidthModulation"
            obj_selfInt     = obj + ".selfIntersect"
            obj_ssw         = obj + ".screenspaceWidth"
            obj_ds          = obj + ".distanceScaling"
            obj_minpw       = obj + ".minPixelWidth"
            obj_maxpw       = obj + ".maxPixelWidth"
            
            drg = "defaultRenderGlobals"
            drg_os          = drg + ".oversamplePaintEffects"
            drg_osFilter    = drg + ".oversamplePfxPostFilter"
            
           
            cmds.setAttr(obj_disp       , cmds.checkBox('oDisp',q=1,v=True) )            
            cmds.setAttr(obj_int        , cmds.checkBox('oInt',q=1,v=True) )
            cmds.setAttr(obj_oc         , cmds.checkBox('oOc',q=1,v=True) )
            cmds.setAttr(obj_tight      , cmds.checkBox('oTp',q=1,v=True) )
            cmds.setAttr(obj_selfInt    , cmds.checkBox('oSelfInt',q=1,v=True) )
            cmds.setAttr(obj_ssw        , cmds.checkBox('oSsw',q=1,v=True) )
            cmds.setAttr(obj_border     , 3)         
            
            
            cmds.setAttr(obj_lw         , cmds.floatFieldGrp('oLw',q=True,v1=True))
            cmds.setAttr(obj_thin       , cmds.floatFieldGrp('oThin',q=True,v1=True))
            cmds.setAttr(obj_borderMod  , cmds.floatFieldGrp('oBorderMod',q=True,v1=True))
            cmds.setAttr(obj_ds         , cmds.floatFieldGrp('oDs',q=True,v1=True))
            cmds.setAttr(obj_minpw      , cmds.floatFieldGrp('oMinpw',q=True,v1=True))
            cmds.setAttr(obj_maxpw      , cmds.floatFieldGrp('oMaxpw',q=True,v1=True))

            cmds.setAttr(drg+".ren","mayaSoftware",typ="string")                     
            cmds.setAttr(drg_os         , cmds.checkBox('dOs',q=1,v=True))
            cmds.setAttr(drg_osFilter   , cmds.checkBox('dOsFilter',q=1,v=True))
            
def r_default(*args):
    cmds.checkBox('oDisp', edit = True, value = 0)
    cmds.checkBox('oInt', edit = True, value = 1)
    cmds.checkBox('oOc',  edit = True , value = 0)
    cmds.checkBox('oTp',  edit = True, value = 1)
    cmds.checkBox('oSelfInt',  edit = True, value = 1)
    cmds.checkBox('oSsw',  edit = True, value = 1)
    cmds.checkBox('dOs',  edit = True, value = 1)
    cmds.checkBox('dOsFilter',  edit = True, value = 1)

    cmds.floatFieldGrp('oLw',  edit = True,v1 = 0.3)
    cmds.floatFieldGrp('oThin',  edit = True ,v1 = 10.0)
    cmds.floatFieldGrp('oBorderMod',  edit = True ,v1 = 1.0)
    cmds.floatFieldGrp('oDs',  edit = True , v1 = 0.1)
    cmds.floatFieldGrp('oMinpw', edit = True ,v1 = 2.0)
    cmds.floatFieldGrp('oMaxpw', edit = True ,v1 = 3.0)
    


# Main GUI
def pfx_setAttr_gui(*ars):
    gui = 'pxf_setAttr_gui'
    
    if cmds.window(gui, q=1, ex=1):
        cmds.deleteUI(gui)
        
    cmds.window(gui,t="Line Preset")
    cmds.columnLayout(adjustableColumn = True)

    
    cmds.checkBox('oDisp', label ='Display', value = 0)
    cmds.checkBox('oInt', label ='Intersection Lines', value = 1)
    cmds.checkBox('oOc', label ='Occlusion Width Scale', value = 0)
    cmds.checkBox('oTp', label ='Tighter Profile', value = 1)
    cmds.checkBox('oSelfInt', label ='Self Intersect', value = 1)
    cmds.checkBox('oSsw', label ='Screen Space Width', value = 1)
    cmds.checkBox('dOs', label ='OverSample', value = 1)
    cmds.checkBox('dOsFilter', label ='OverSample Filter', value = 1)

    cmds.floatFieldGrp('oLw', label='Line Width', columnAlign=(1,'left'),columnWidth=(1,120),v1 = 0.3)
    cmds.floatFieldGrp('oThin', label='Line End Thinning ', columnAlign=(1,'left'),columnWidth=(1,120),v1 = 10.0)
    cmds.floatFieldGrp('oBorderMod', label='Border Width Mod', columnAlign=(1,'left'),columnWidth=(1,120),v1 = 1.0)
    cmds.floatFieldGrp('oDs', label='Distance Scaling', columnAlign=(1,'left'),columnWidth=(1,120),v1 = 0.1)
    cmds.floatFieldGrp('oMinpw', label='Min Pixel Width', columnAlign=(1,'left'),columnWidth=(1,120),v1 = 2.0)
    cmds.floatFieldGrp('oMaxpw', label='Max Pixel Width', columnAlign=(1,'left'),columnWidth=(1,120),v1 = 3.0)
    


    cmds.button('bPreset', label= "APPLY VALUE", height =35, bgc=(.95,.9,.8), c = r_init)
    cmds.button('bDefault', label= "Default Value", height =35, bgc=(.55,.9,.8), c = r_default)
    
    cmds.window(gui, e=1, width=240, height = 60)
    cmds.showWindow(gui)


# GUI execute
pfx_setAttr_gui()
