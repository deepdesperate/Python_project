bl_info = {
    "name": "Textament",
    "author": "Naman Deep",
    "version": (1, 0),
    "blender": (3, 00, 0),
    "description": "Load and connect node textures",
    "location": "Node_Graph header",
    "category": "Learning"
}

import os
from typing import Set
import bpy
from bpy.types import Context
from bpy_extras.io_utils import ImportHelper

class AddTextures(bpy.types.Operator, ImportHelper):
    """Load and connect material textures"""
    bl_idname = "texture.textament_load"
    bl_label = "Load and connect textures"
    bl_description = "Load and connect material textures"

    directory: bpy.props.StringProperty()
    files: bpy.props.CollectionProperty( 
                    name = "File Paht",
                    type = bpy.types.OperatorFileListElement,
                )
    
    filter_glob = bpy.props.StringProperty( default = "*.png; *.jpg",options= {"HIDDENT"})

    @classmethod
    def poll(cls, context):
        ob = context.object
        if not ob:
            return False
        mat = ob.active_material
        if not mat:
            return False
        tree = mat.node_tree
        if not tree:
            return False
        return tree.nodes.active
    
    def execute(self, context):
        mat = context.object.active_material
        target_mode = mat.node_tree.nodes.active

        match_rule = lambda x : x.lower().replace(" ","")