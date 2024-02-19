bl_info = {
    "name": "Latte Express",
    "author": "Naman Deep",
    "version": (1, 0),
    "blender": (3, 00, 0),
    "description": "Create a Lattice on the active object",
    "category": "Learning",
}

import bpy
from mathutils import Vector


class LatteExpress(bpy.types.Operator):
    """Set up Lattice Deformation"""
    bl_idname = "object.latte_expresso"
    bl_label = "Create Lattice on active object"

    @classmethod
    def poll(cls, context):
        return context.active_object
    
    def execute(self, context):
        ob = context.object
        latt_data = bpy.data.lattices.new(f"LAT-{ob.name}")
        latt_obj = bpy.data.objects.new( name = latt_data.name , object_data=latt_data)
        
        context.collection.objects.link(latt_obj)

        latt_obj.scale = ob.dimensions
        ob_translation = ob.matrix_world.to_translation()

        # Getting bounding box size from coordinate
        btm_left = min( (c for c in ob.bound_box), key = sum)
        top_right = max((c for c in ob.bound_box), key = sum)

        # 0.5 for half way
        btm_left = Vector(btm_left)
        ob_center = btm_left.lerp(top_right, 0.5)

        ob_translation += ob_center
        latt_obj.location = ob_translation

        mod = ob.modifiers.new("Lattice", 'LATTICE')
        mod.object = latt_obj
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(LatteExpress.bl_idname , icon = "MOD_LATTICE")

def register():
    bpy.utils.register_class(LatteExpress)
    ob_menu = bpy.types.VIEW3D_MT_object_context_menu
    ob_menu.append(menu_func)

def unregister():
    ob_menu = bpy.types.VIEW3D_MT_object_context_menu
    ob_menu.remove(menu_func)
    bpy.utils.unregister_class(LatteExpress)