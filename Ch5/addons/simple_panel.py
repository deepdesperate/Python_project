bl_info = {
    "name": "A Very Simple Panel",
    "author": "Naman Deep",
    "version": (1,0),
    "blender": (3, 6, 0),
    "description": "Just show a panel in UI",
    "category": "Learning",
}

import bpy
from bpy.utils import previews
import os
import random

# Global Variable for icon storage
custom_icons = None


# Function to load custom icons which will be register in register function
def load_custom_icons():
    '''Load icon from the add-on folder'''
    Addon_path = os.path.dirname(__file__)
    img_file = os.path.join(Addon_path,"icon_smile_64.png")
    
    global custom_icons
    custom_icons = previews.new()
    custom_icons.load("smiling_face", img_file, 'IMAGE')

def remove_custom_icons():
    """ Clear Icons loaded from file  """
    
    global custom_icons
    bpy.utils.previews.remove(custom_icons)
    
def add_random_location(objects, amount = 1, do_axis = (True, True, True)):
    for ob in objects:
        for i in range(3):
            if(do_axis[i]):
                loc = ob.location
                loc[i] += random.randint(-amount, amount)

# Panel will be part of object properties
# So class name begin with OBJECT

class TRANSFORM_OT_random_location(bpy.types.Operator):
    """ Add units to the location of selected objects"""
    bl_idname = "transform.add_random_location"
    bl_label = "Add random location"
    bl_options = {'REGISTER','UNDO'}
    
    amount: bpy.props.IntProperty(name = "Amount", default  = 1)
    axis: bpy.props.BoolVectorProperty(name = "Displace Axis", default = (True, True, True))
    
    @classmethod
    def poll(cls, context):
        return context.selected_objects
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def execute(self, context):
        add_random_location(context.selected_objects, self.amount, self.axis)
        return {"FINISHED"}
    


class OBJECT_PT_very_simple(bpy.types.Panel):
    ''' Creates a Panel in the object context of properties panel'''
    bl_label = "A Very Simple Panel"
    bl_idname = "VERYSIMPLE_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Our Panel'

    max_objects = 3
    
    def draw (self , context):
        #       icon_id = custom_idcons['smile_face'].icon_id
#               layout.label(text = "Smile", icon_value = icon_id)

        col = self.layout.column()
        col.label(text = "A Very Simple Label", icon = 'INFO')
        row = col.row()
        row.label(text = "Isn't it great?", icon = 'QUESTION')
        
        box = col.box()
        split = box.split(factor = 0.33)
        left_col = split.column()
        right_col = split.column()
        
        for k, v in bl_info.items():
            if not v:
                continue
            left_col.label(text = k)
            right_col.label(text = str(v))
        
        col.label(text = "Scene Objects:")
        grid = col.grid_flow(columns = 2, row_major = True)
        
        
        for i,ob in enumerate(context.scene.objects):
#            if i > self.max_objects:
#                obj_count = len(context.scene.objects)
#                obj_left = obj_count - self.max_objects
#                txt = f"... (more {obj_left} objects"
#                grid.label(text = txt)
#                break
            item_layout = grid.column()
            
            item_layout.enabled =  ob.select_get()
            item_layout.alert = ob == context.object
            item_layout.label(text = ob.name, icon = f"OUTLINER_OB_{ob.type}")
        
        num_selected = len(context.selected_objects)
        if num_selected > 0:
            txt = f"Delete {num_selected} object"
            if num_selected > 1:
                txt += "s"
            # Operator Calls return its properties that can be set also
            props = col.operator(bpy.ops.object.delete.idname(), text = txt)
            props.confirm = False 
        else:
            to_disable = col.column()
            to_disable.enabled = True
            to_disable.operator(bpy.ops.object.delete.idname(), text = "Delete Selected")
            
        col.operator(TRANSFORM_OT_random_location.bl_idname)
        

        
        


def register():
#    load_custom_icons()
    bpy.utils.register_class(OBJECT_PT_very_simple)
    bpy.utils.register_class(TRANSFORM_OT_random_location)

def unregister():
#    remove_custom_icons()
    bpy.utils.unregister_class(OBJECT_PT_very_simple)
    bpy.utils.unregister_class(TRANSFORM_OT_random_location)
    
    
if __name__ == '__main__':
    register()
