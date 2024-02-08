bl_info = {
    "name": "Object Shaker",
    "author": "Naman Deep",
    "version": (0,1),
    "blender": (3, 00 ,0),
    "description": "Add Shaky motion to active object",
    "location": "Object Right Click -> Add Object Shake",
    "category": "Learning",
}

import bpy

class OBJECT_SHAKER(bpy.types.Operator):
    """Set playback range to current action Start/End"""
    bl_idname = "object.shaker_animation"
    bl_label = "Add Object Shake"
    bl_description = "Add Shake motion to active object"
    bl_options = {'REGISTER','UNDO'}

    duration : bpy.props.FloatProperty(default = 1.0, min = 0.0)
    strength : bpy.props.FloatProperty(default= 1.0, soft_min = 0.0, soft_max = 1.0)

    @classmethod
    def poll(cls, context):
        return context.object
    
    def execute(self, context):
        if not context.object.animation_data:
            anim = context.object.animation_data_create()
        else:
            anim = context.object.animation_data

        if not anim.action:
            action = bpy.data.actions.new('ShakeMotion')
            anim.action = action
        else:
            action = anim.action

        # Getting duration in terms of frames
        # Creating animation before and after of current frame
        fps = context.scene.render.fps
        duration_frames = self.duration * fps / 2
        current = context.scene.frame_current
        start = current - duration_frames
        end = current + duration_frames

        #Getting fcurves for locationZ, rotation_euler X and rotation_euler Y
        z_loc_crv = self.get_fcurve( context,'location', index = 2)
        x_rot_crv = self.get_fcurve(context, 'rotation_euler', index = 0)
        y_rot_crv = self.get_fcurve(context, 'rotation_euler' , index = 1)

def get_fcurve(self, obj, data_path, index):
    """Return F-Curve of given data_path/ index"""
    action = obj.animation_data.action
    # Halt the script, if for unforeseen reasons, no current action is found
    assert action
    try: 
        crv = action.fcurves.new(data_path, index = index)
    except RuntimeError:
        # next can be applied to iterators as wella as arrays or collection
        crv = next(fc for fc in action.fcurves if fc.data_path == data_path and fc.array_index == index)
        
    # Making sure our fcurve has keyframes
    if not crv.keyframe_points:
        crv.keyframe_points.insert( frame = context.scene.frame_current, value = getattr(obj,data_path)[index])

    return crv