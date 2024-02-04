import bpy

bpy.context.object.location = 10.0, 10.0, 10.0
bpy.context.object.keyframe_insert('location', frame = 1)

bpy.context.object.location = -10.0, -10.0, -10.0
bpy.context.object.keyframe_insert('location', frame = 24)

anim_data = bpy.context.object.animation_data
action = anim_data.action
f_curve = action.fcurves

for fc in f_curve:
    # Stores data path and index for mutliple values
    print(fc.data_path, fc.array_index)
    
    for f in fc.keyframe_points:
        frame,value = f.co
        print("\t Frame", frame, "value", value)