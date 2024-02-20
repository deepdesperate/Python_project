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
    bl_options = {'REGISTER','UNDO'}

    add_subsurf: bpy.props.BoolProperty(default = True)
    subd_levels: bpy.props.IntProperty(default = 2)

    grid_levels: bpy.props.IntVectorProperty(default = (3, 3, 3) , min = 1, subtype = 'XYZ')
    add_armature: bpy.props.BoolProperty(default = True)

    @classmethod
    def poll(cls, context):
        return context.active_object
    
    def execute(self, context):
        ob = context.object
        if self.add_subsurf:
            subdiv = ob.modifiers.new("Subdivision", "SUBSURF")
            subdiv.levels = self.subd_levels
            subdiv.render_levels = self.subd_levels
            subdiv.subdivision_type = "SIMPLE"

        latt_data = bpy.data.lattices.new(f"LAT-{ob.name}")
        latt_obj = bpy.data.objects.new( name = latt_data.name , object_data=latt_data)
        latt_data.points_u = self.grid_levels[0]
        latt_data.points_v = self.grid_levels[1]
        latt_data.points_w = self.grid_levels[2]
        latt_data.use_outside = True

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
        if not self.add_armature:
            latt_obj.location = ob_translation
        else:
            arm_data = bpy.data.armatures.new(f"ARM-{ob.name}")
            arm_obj = bpy.data.objects.new( name = arm_data.name, object_data= arm_data)
            context.collection.objects.link(arm_obj)

        # latt_obj.location = ob_translation
        latt_obj.parent = arm_obj
        arm_obj.location = ob_translation

        # to make armature's transform pivot under the affected geometry
        half_height = ob.dimension[2]/2
        arm_obj.location[2] -= half_height

        # Lattice should be centerd to geometry
        latt_obj.location[2] += half_height

        context.view_layer.objects.active = arm_obj
        bpy.ops.object.mode_set(mode = 'EDIT', toggle = False)

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