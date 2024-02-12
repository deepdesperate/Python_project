
bl_info = {
    "name": "Object Pendulum",
    "author": "Naman Deep",
    "version": (1,0),
    "blender": (3, 00, 0),
    "description": "Add swing motion to active object",
    "category": "Learning",
}

from typing import Set
import bpy
from bpy.types import Context

class ObjectPendulum(bpy.types.Operator):
    """ Set up swinging motion on active object"""
    bl_idname = "object.shaker_animation"
    bl_label = "Make Pendulum"
    bl_description = "Add swinging motion to Active Object"
    bl_options = {'REGISTER', 'UNDO' }

    amplitude : bpy.props.FloatProperty(default = 0.25, min = 0.0)

    length : bpy.props.FloatProperty(default = 5.0, min = 0.0)

    @classmethod
    def poll(cls, context):
        return bool(context.object)
    
    def execute(self, context: Context):
        ob = context.object
        pivot_name = f"EMP-{ob.name}_pivot"
        pivot = bpy.data.objects.new(pivot_name, None)
        context.collection.objects.link(pivot)

        pivot.matrix_world = ob.matrix_world
        # Third row and fourth column, fourth column for rotation
        pivot.matrix_world[2][3] += self.length

        pivot["amplitude"] = self.amplitude

        constr = ob.constraints.new('PIVOT')
        constr.target = pivot
        constr.rotation_range = 'ALWAYS_ACTIVE'

        # driver_add returns the drive curve
        driver_crv = ob.driver_add('rotation_euler',0)
        driver = driver_crv.driver

        driver.type = "SCRIPTED"
        xpr = "sin(frame / fps /sqrt(length/9.8)) * amp * pi"
        driver.expression = xpr

        # Creating fps variables
        fps = driver.variables.new()
        fps.name = "fps"
        fps.type = "SINGLE_PROP"
        fps.targets[0].id_type = 'SCENE'
        fps.targets[0].id = context.scene
        fps.targets[0].data_path = "render.fps"

        # Creating length variable for driver
        len = driver.variables.new()
        len.name = "length"
        len.type = "LOC_DIFF"
        len.targets[0].id = pivot
        len.targets[1].id = ob

        # Creating the amplitude variable
        amp = driver.variables.new()
        amp.name = "amp"
        amp.type = "SINGLE_PROP"
        amp.targets[0].id_type = "OBJECT"
        amp.targets[0].id = pivot
        amp.targets[0].data_path = "[\"amplitude\"]"
        
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.separator()
    self.layout.operator(ObjectPendulum.bl_idname)

def register():
    bpy.utils.register_class(ObjectPendulum)
    ob_menu = bpy.types.VIEW3D_MT_object_context_menu
    ob_menu.append(menu_func)

def unregister():
    ob_menu = bpy.types.VIEW3D_MT_object_context_menu
    ob_menu.remove(menu_func)
    bpy.utils.unregister_class(ObjectPendulum)