import bpy
from .import img_loader
from . import operators

class OBJECT_PT_structured(bpy.types.Panel):
    """ Creates a Panel in the object context"""
    bl_label = "A Modular Panel"
    bl_idname = "MODULAR_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'

    # max_objects = 3 limit displayed list to 3 objects

    def draw(self, context):
        layout = self.layout
        icons = img_loader.get_icons_collection()
        row = layout.row(align = True)
        row.label(text = "Scene Objects", icon_value = icons['pack_64'].icon_id)
        row.label(text = " ", icon_value = icons['smile_64'].icon_id )

        grid = layout.grid_flow(columns=2, row_major= True)

        add_on = context.preferences.addons[__package__]
        preferences = add_on.preferences

        for i, obj in enumerate(context.scene.objects):
            if i >= preferences.max_objects:
                grid.label(text = "...")
                break
            grid.enabled = obj.select_get()
            grid.alert = obj == context.object
            grid.label(text = obj.name, icon = f'OUTLINER_OB_{obj.type}')
        
        layout.operator(operators.TRANSFORM_OT_random_location.bl_idname)
        num_selected = len(context.selected_objects)
        if num_selected > 0:
            txt = f"Delete {num_selected} object"
            if num_selected > 1:
                txt += "s"
            props = layout.operator(bpy.ops.object.delete.idname(), text = txt)
            props.confirm = False
        else:
            to_disable = layout
            to_disable.enabled = True
            layout.operator(bpy.ops.object.delete.idname, text = "Delete Selected")

        


def register_classes():
    bpy.utils.register_class(OBJECT_PT_structured)

def unregister_classes():
    bpy.utils.unregister_class(OBJECT_PT_structured)
