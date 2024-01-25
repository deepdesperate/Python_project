bl_info = {
    "name": "Elevator",
    "author": "Naman Deep",
    "version": (1,0),
    "blender": (3, 00, 0),
    "description": "Move objects up to a minimum height",
    "category": "Object",
}

import bpy
from copy import copy
from bpy.props import FloatProperty, BoolProperty


class OBJECT_OT_elevator(bpy.types.Operator):
    """ Move Objects up to a given height"""
    bl_idname = "object.pckt_floor_transform"
    bl_label = "Elevate Objects"
    bl_options = {'REGISTER','UNDO'}
    
    floor: FloatProperty(name = "Floor", default = 0 )
    constr: BoolProperty(name = "Constraints", default = False)
    reuse: BoolProperty(name = "Reuse Constraints", default = True)
    
    @classmethod
    def poll(cls, context):
        return len(bpy.context.selected_objects)>0
    
    def execute(self, context):
        
        if(self.constr):
            for ob in context.selected_objects:
                limit = get_constraints(ob, 'LIMIT_LOCATION', self.reuse)
                limit.use_min_z = True
                limit.min_z = self.floor
            return {'FINISHED'}
        
        selected_objects = copy(context.selected_objects)
        selected_objects.sort(key = ancestor_count)
        
        for ob in context.selected_objects:
            world_mat = ob.matrix_world
            if world_mat[2][3]  > self.floor:
                continue
            
            world_mat[2][3] = self.floor
        return {'FINISHED'}
    

def get_constraints(obj, constr_type, reuse= True):
    if reuse:
        for constr in obj.constraints:
            if(constr.type == constr_type):
                return constr
            
    return obj.constraints.new(constr_type)


def draw_elevator_item(self, context):
    row = self.layout.row()
    row.operator(OBJECT_OT_elevator.bl_idname)
     
def ancestor_count(ob):
    ancestors = 0
    while ob.parent:
        ancestors += 1
        ob = ob.parent
    return ancestors        
    
def register():
    # Add operator and menu item
    bpy.utils.register_class(OBJECT_OT_elevator)
    object_menu = bpy.types.VIEW3D_MT_object_context_menu
    object_menu.append(draw_elevator_item)
    
def unregister():
    # Remove operator and menu item
    bpy.utils.unregister_class(OBJECT_OT_elevator)
    object_menu = bpy.types.VIEW3D_MT_object_context_menu
    object_menu.remove(draw_elevator_item)
    