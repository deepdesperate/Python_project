bl_info = {
    "name": "Action to Range",
    "author": "Naman Deep",
    "version": (1, 0),
    "blender": (3, 00, 0),
    "location": "Timeline > View > Action to Scene Range",
    "description": "Action Duration to Scene Range",
    "category": "Learning",
}

import bpy

class ActionToSceneRange(bpy.types.Operator):
    """ Set Playback range to current Action Start/End"""
    bl_idname = "anim.action_to_range"
    bl_label = "Action range to scene"
    bl_description = "Transfer action range to scene range"
    bl_options = {'REGISTER','UNDO'}
    
    use_preview: bpy.props.BoolProperty(default = True)

    @classmethod
    def poll(cls, context):
        obj = context.object
        if not obj:
            return False
        if not obj.animation_data:
            return False
        if not obj.animation_data.action:
            return False
        return True

    def execute(self, context):
        anim_data = context.object.animation_data
        first, last = anim_data.action.frame_range
        scn = context.scene
        if self.use_preview:
            scn.frame_preview_start = int(first)
            scn.frame_preview_end = int(last)
        else:
            scn.frame_start = int(first)
            scn.frame_end = int(last)
        bpy.ops.action.view_all()
        return {'FINISHED'}
    
def view_menu_items(self, context):
    props = self.layout.operator( ActionToSceneRange.bl_idname, text = ActionToSceneRange.bl_idname + " (preview)")
    props.use_preview = True

    props = self.layout.operator( ActionToSceneRange.bl_idname)
    props.use_preview = False