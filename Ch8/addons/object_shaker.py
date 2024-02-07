bl_info = {
    "name": "Object Shaker",
    "author": "Naman Deep",
    "version": (0,1),
    "blender": (3, 00 ,0),
    "description": "Add Shaky motion to active object",
    "location": "Object Right Click -> Add Object Shake",
    "category": "Learning",
}

import bpy

class OBJECT_SHAKER(bpy.types.Operator):
    """Set playback range to current action Start/End"""
    bl_idname = "object.shaker_animation"
    bl_label = "Add Object Shake"
    bl_description = "Add Shake motion to active object"
    bl_options = {'REGISTER','UNDO'}

    duration : bpy.props.FloatProperty(default = 1.0, min = 0.0)
    strength : bpy.props.FloatProperty(default= 1.0, soft_min = 0.0, soft_max = 1.0)

    @classmethod
    def poll(cls, context):
        return context.object
    
    def execute(self, context):
        