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
        
        
        # Checking for each windows' scene whether there is a DOPSHEET EDITOR
        for window in context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type != 'DOPESHEET_EDITOR':
                    continue
                for region in area.regions:
                    if region.type == 'WINDOW':
                        with context.temp_override ( window = window, area= area, region = region):
                            bpy.ops.action.view_all
                        break
                break


        return {'FINISHED'}
    
def view_menu_items(self, context):
    props = self.layout.operator( ActionToSceneRange.bl_idname, text = ActionToSceneRange.bl_idname + " (preview)")
    props.use_preview = True

    props = self.layout.operator( ActionToSceneRange.bl_idname)
    props.use_preview = False


def register():
    bpy.utils.register_class(ActionToSceneRange)
    bpy.types.TIME_MT_view.append(view_menu_items)

def unregister():
    bpy.types.TIME_MT_view.remove(view_menu_items)
    bpy.utils.unregister_class(ActionToSceneRange)
