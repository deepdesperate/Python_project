bl_info = {
    "name": "Collector",
    "author":" Naman Deep",
    "version": "(1,0)",
    "blender": "(4,00,0)",
    "description": "Create collections for object types",
    "category": "Object",
}

import bpy

class OBJECT_OT_collector_types(bpy.types.Operator):
    """ Create collections based on objects types"""
    bl_idname = "object.pckt_type_collector"
    bl_lable = "Create Type Collections"

    @classmethod
    def poll(cls, context):
        return len(bpy.data.objects) > 0

    @staticmethod
    def get_collection(name):

        ''' Returns the collection named after the given argument, If it doesn't exist, a new collection is created and linked to the scene'''
        try:
            return bpy.data.collections[name]
        except KeyError:
            col = bpy.data.collections.new(name)
            bpy.context.scene.collection.children.link(col)
            return col

    def execute(self, context):
        # Code
        for obj in context.scene.objects:
            col = self.get_collection(obj.type.title())
            try:
                col.objects.link(ob)
            except RuntimeError:
                continue

        return {'FINISHED'}

def draw_collector_items(self, context):
    row = self.layout.row()
    row.operator(OBJECT_OT_collector_types)



def register():
    # this function is called when add-on is enabled
    bpy.utils.register_class(OBJECT_OT_collector_types)
    menu = bpy.types.VIEW3D_MT_object_context_menu
    menu.append(draw_collector_items)
    

def unregister():
    # this function is called when the add-on is disabled
    bpy.utils.unregister_class(OBJECT_OT_collector_types)
    menu = bpy.types.VIEW3D_MT_object_context_menu
    menu.remove(draw_collector_items)
