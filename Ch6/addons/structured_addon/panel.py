import bpy
from .import img_loader


class OBJECT_PT_structured(bpy.types.Panel):
    """ Creates a Panel in the object context"""
    bl_label = "A Modular Panel"
    bl_idname = "MODULAR_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'

    max_objects = 3 # limit displayed list to 3 objects

    def draw(self, context):
        layout = self.layout
        icons = img_loader.get_icons_collection()
        row = layout.row(align = True)
        row.label(text = "Scene Objects", icon_value = icons['pack_64'].icon_id)
        row.layout(text = " ", icon_value = icons['smile_64'].icon_id )

        grid = row.grid_flow(columns=2, row_major= True)

        for i, obj in enumerate(context.scene.objects):
            if i > self.max_objects:
                grid.label(text = "...")
                break
            grid.label(text = obj.name, icon = f'OUTLINER_OB_{obj.type}')



def register_classes():
    bpy.utils.register_class(OBJECT_PT_structured)

def unregister_classes():
    bpy.utils.unregister_class(OBJECT_PT_structured)
