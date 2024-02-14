bl_info = {
    "name": "Text PunchClock",
    "author": "Naman Deep",
    "version": (1, 0),
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

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'
    
    def invoke(self, context, event):
        now = datetime.datetime.now()
        self.hour = now.hour
        self.mins = now.minute
        return self.execute(context)
    
    def execute(self, context):

        txt_crv = bpy.data.curves.new(type = "FONT", name = "TXT-clock")
        # f"{3:02} becomes "03"
        txt_crv.body = f"{self.hour:02}:{self.mins:02}"

        txt_obj = bpy.data.objects.new(name = "Font Object", object_data= txt_crv)

        context.collection.objects.link(txt_obj)

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.separator()
    self.layout.operator(PunchClock.bl_idname, icon = 'TIME')

def register():
    bpy.utils.register_class(PunchClock)
    bpy.types.VIEW3D_MT_add.append(menu_func)

def unregister():
    bpy.types.VIEW3D_MT_add.remove(menu_func)
    bpy.utils.unregister_class(PunchClock)