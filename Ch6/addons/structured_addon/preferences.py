import bpy
from bpy.props import IntProperty

class StructuredPreferences(bpy.types.AddonPreferences):
    # Takes the same name as of that of the addon name
    bl_idname = __package__

    max_objects: IntProperty(name = "Maximum Objects", default = 3)

    def draw(self, context):
        layout = self.layout
        split = layout.split(factor=0.5)
        split.separator()
        split.label(text = "Maximum objects")
        split.prop(self,'max_objects', text = "")

def register_classes():
    bpy.utils.register_class(StructuredPreferences)

def unregister_classes():
    bpy.utils.unregister_class(StructuredPreferences)
