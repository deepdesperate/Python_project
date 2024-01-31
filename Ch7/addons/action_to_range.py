bl_info = {
    "name": "Action to Range",
    "author": "Naman Deep",
    "version": (1, 0),
    "blender": (3, 00, 0),
    "location": "Timeline > View > Action to Scene Range",
    "description": "Action Duration to Scene Range",
    "category"L "Learning",
}

import bpy

class ActionToSceneRange(bpy.types.Operator):
    """ Set Playback range to current Action Start/End"""
    bl_idname = "anim.action_to_range"
    bl_label = "Action range to scene"
    bl_description = "Transfer action range to scene range"
    bl_options = {'REGISTER','UNDO'}
    
