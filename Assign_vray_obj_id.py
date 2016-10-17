### assign vray obj id 


import maya.cmds as cmds



def create_id_attr(obj_name, id_num):
    
    cmds.addAttr(obj_name , ln = "vrayObjectID", at="long", min=0, max = 1000000, dv = 0)
    cmds.setAttr(obj_name+".vrayObjectID", id_num)
    


def assign_obj_id(*args):
    
    sels = cmds.ls(sl=1)
    id_num = cmds.intSliderGrp('get_id_num',q=True, v=True)
    for x in sels:
        if cmds.objectType(x) == 'transform' : create_id_attr(x, id_num)


# Vray Object ID assign function
def assign_vray_obj_id_GUI(*args):
    
    gui = 'assign_vray_obj_id'                              #GUI name var
    if cmds.window(gui, q=1, ex=1):
        cmds.deleteUI(gui)

    cmds.window(gui,t="Assign Vray object ID")
    cmds.columnLayout(adjustableColumn = True)
    
    cmds.rowColumnLayout(nc = 2)
    cmds.text('Object ID', width = 60)
    cmds.intSliderGrp('get_id_num', f=True, fs = 1,min=0, max = 64, width =250)
    cmds.setParent("..")
    cmds.columnLayout(adjustableColumn = True)
    cmds.button('assign_id', w = 180,bgc=(0.2,0.1,0.4), c = assign_obj_id)
    
    cmds.window(gui, e=1, width=180, height = 120)
    cmds.showWindow(gui)

   
assign_vray_obj_id_GUI()