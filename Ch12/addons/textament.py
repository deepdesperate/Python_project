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

    # Nodes spacing
    _spacing = 340.0

    directory: bpy.props.StringProperty()
    files: bpy.props.CollectionProperty( 
                    name = "File Path",
                    type = bpy.types.OperatorFileListElement,
                )
    
    filter_glob : bpy.props.StringProperty( default = "*.png; *.jpg",options= {"HIDDENT"})

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
        target_node = mat.node_tree.nodes.active

        match_rule = lambda x : x.lower().replace(" ","")

        input_names = target_node.inputs.keys()

        matching_names = {}
        for f in self.files:
            for inp in input_names:
                if match_rule(inp) in match_rule(f.name):
                    matching_names[inp] = f.name
                    break
        # TO get the input nodes of the PS, in order
        sorted_inputs = [i for i in input_names if i in matching_names]
        
        for i ,inp in enumerate(sorted_inputs):
            img_path = os.path.join(self.directory, matching_names[inp] )

            img = bpy.data.images.load( img_path, check_existing= True)
            
            if target_node.inputs[inp].type != "RGBA":
                img.colorspace_settings.name = "Non-Color"

            tree = mat.node_tree
            img_node = tree.nodes.new("ShaderNodeTexImage")
            img_node.image = img

            img_node.location = target_node.location
            img_node.location.x -= self._spacing
            img_node.location.y -= i * self._spacing

            if inp  == "Base Color":
                mix = mat.node_tree.nodes.new("ShaderNodeMixRGB")
                mix.location = img_node.location
                img_node.location.x -= self._spacing / 2
                mix.location.x += self._spacing / 2

                mat.node_tree.links.new(img_node.outputs["Color"], mix.inputs["Color1"])

                img_node = mix

            if inp != "Normal":
                tree.links.new(img_node.outputs["Color"] , target_node.inputs[inp] )
                continue

            normal_map = tree.nodes.new("ShaderNodeNormalMap")
            normal_map.location = img_node.location
            
            img_node.location.x -= self._spacing / 2
            normal_map.location.y += self._spacing / 2

            tree.links.new( normal_map.outputs["Normal"], target_node.inputs[inp] )

            tree.links.new( img_node.outputs["Color"], normal_map.inputs["Color"] )
        
        return {'FINISHED'}

def shader_header_button(self, context):
    self.layout.operator(AddTextures.bl_idname, icon = "NODE_TEXTURE", text = "Load Textures")


def register():
    bpy.utils.register_class(AddTextures)
    bpy.types.NODE_HT_header.append(shader_header_button)

def unregister():
    bpy.types.NODE_HT_header.remove(shader_header_button)
    bpy.utils.unregister_class(AddTextures)