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
    

# Panel will be part of object properties
# So class name begin with OBJECT
class OBJECT_PT_very_simple(bpy.types.Panel):
    ''' Creates a Panel in the object context of properties panel'''
    bl_label = "A Simple Panel"
    bl_idname = "VERYSIMPLE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'

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
        
        

        
        


def register():
#    load_custom_icons()
    bpy.utils.register_class(OBJECT_PT_very_simple)

def unregister():
#    remove_custom_icons()
    bpy.utils.unregister_class(OBJECT_PT_very_simple)
    
    
if __name__ == '__main__':
    register()
