bl_info = {
    "name": "Text PunchClock",
    "author": "Naman Deep",
    "version": (1, 0, 1),
    "blender": (3, 00, 0),
    "description": "Create an Hour/Minutes text object",
    "category": "Learning",
}

import bpy
import datetime

class PunchClock(bpy.types.Operator):
    """ Create Hour/Minutes text"""
    bl_idname = "text.punch_clock"
    bl_label = "Create Hour/Minutes Text"
    bl_description = "Create Hour Minutes Text"
    bl_options = {'REGISTER', 'UNDO'}

    hour: bpy.props.IntProperty(default = 0, min = 0, max = 23)
    mins: bpy.props.IntProperty(default = 0, min = 0, max = 59)
    set_hours: bpy.props.BoolProperty(default = True)

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'
    
    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.alignment = 'CENTER'

        row.prop(self, 'hour', text = "")
        row.label(text = ' :',)
        row.prop(self, 'mins',text = "")

    def invoke(self, context, event):
        now = datetime.datetime.now()
        self.hour = now.hour
        self.mins = now.minute

        self.txt_crv = bpy.data.curves.new(type = "FONT", name = "TXT-hhmm")
        self.txt_obj = bpy.data.objects.new(name = "OB-Txt", object_data=self.txt_crv)
        context.collection.objects.link(self.txt_obj)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
        
    @staticmethod
    def modal(self, context, event):
        # Getting the mouse move direction
        if event.type == 'MOUSEMOVE':
            delta = event.mouse_x - event.mouse_prev_x
            delta /= 10

            delta = round(delta)

            if self.set_hours:
                self.hour += delta
            else:
                self.mins += delta
            txt = f"{self.hour:02}:{self.mins: 02}"
            self.txt_crv.body = txt
        
        elif event.type == 'RET':
            return {'FINISHED'}
        
        # https://docs.blender.org/api/3.3/bpy_types_enum_items/event_type_items.html
        # using tab and checking even.value
        if event.type == 'TAB' and event.value == 'PRESS':
            self.set_hours = not self.set_hours
            
        elif event.type == 'ESC':
            # Cleaning up after itself
            bpy.data.objects.remove(self.txt_obj)
            # Cancelled helps avoid the undo queu
            return {'CANCELLED'}
        
        return {'RUNNING_MODAL'}

    
    def execute(self, context):

        txt_crv = bpy.data.curves.new(type = "FONT", name = "TXT-clock")
        # f"{3:02} becomes "03"
        txt_crv.body = f"{self.hour:02}:{self.mins:02}"

        txt_obj = bpy.data.objects.new(name = "Font Object", object_data= txt_crv)

        context.collection.objects.link(txt_obj)

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.separator()
    # setting invoke default when called from pop up, Shift+A
    row = self.layout.row()
    row.operator_context = "INVOKE_DEFAULT"

    self.layout.operator(PunchClock.bl_idname, icon = 'TIME')

def register():
    bpy.utils.register_class(PunchClock)
    bpy.types.VIEW3D_MT_add.append(menu_func)

def unregister():
    bpy.types.VIEW3D_MT_add.remove(menu_func)
    bpy.utils.unregister_class(PunchClock)