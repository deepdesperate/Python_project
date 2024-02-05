bl_info = {
    "name": "Vert Runner",
    "author": "Naman Deep",
    "version": (1,0),
    "blender": (3, 00, 0),
    "location": "Object > Animation > Vert Runner",
    "description": "Run on the vertices of the active object",
    "category": "Learning",
}

import bpy
from math import pi
# Arcsine function
from math import asin

class VertRunner(bpy.types.Operator):
    """Run over vertices of the active object"""
    bl_idname = "object.vert_runner"
    bl_label = "Vertex Runner"
    bl_description = "Animate along vertices of the active object"
    bl_options = {'REGISTER', 'UNDO'}

    step: bpy.props.IntProperty(default = 12)
    loop: bpy.props.BoolProperty(default = True)

    @classmethod
    def poll(cls, context):
        obj = context.object
        if not obj:
            return False
        if not obj.type == 'MESH':
            return False
        if not len(context.selected_objects) > 1:
            return False
        return True
    
    def execute(self, context):
        verts = list(context.object.data.vertices)

        if self.loop:
            verts.append(vert[0])

        for obj in context.selected_objects:
            if not obj == context.object:
                frame = context.scene.frame_current
                for vert in verts:
                    obj.location = vert.co
                    obj.keyframe_insert('location', frame = frame)
                    frame += self.step
        return {'FINISHED'}

def aim_to_point(self, ob, point_co):
    """Orient objects to look at coordinate"""

    direction = point_co - ob.location
    # Normalising the direction so that result is not affected by distance
    direction.normalize()
    arc = asin(direction.y)
    # Making sure when coordinate is of -x axis, we calcuate, by pi-arc, as in 180 - arc
    if direction.x < 0:
        arc = pi-arc

    # Adding 90 cuz in blender object faces opposite Y-axis
    arc += pi/2

def anim_menu_funct(self, context):
    self.layout.separator()
    self.layout.operator(VertRunner.bl_idname, text = VertRunner.bl_label)

def register():
    bpy.utils.register_class(VertRunner)
    bpy.types.VIEW3D_MT_object_animation.append(anim_menu_funct)

def unregister():
    bpy.types.VIEW3D_MT_object_animation.remove(anim_menu_funct)
    bpy.utils.unregister_class(VertRunner)