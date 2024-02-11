bl_info = {
    "name": "Object Pendulum",
    "author": "Naman Deep"
    "version": (1,0),
    "blender": (3, 00, 0),
    "description": "Add swing motion to active object",
    "category": "Learning",
}

import bpy

class ObjectPendulum(bpy.types.Operator):
    """ Set up swinging motion on active object"""
    bl_idname = "object.shaker_animation"
    bl_label = "Make Pendulum"
    bl_description = "Add swinging motion to Active Object"
    bl_options = {'REGISTER', 'UNDO' }