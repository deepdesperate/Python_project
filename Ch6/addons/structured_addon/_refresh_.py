
from importlib import reload
import sys
import bpy
from . import *

# Using developerui button to enable or disable reload functionality

def reload_modules():
    if not bpy.context.preferences.view.show_developer_ui:
        return
    reload(sys.modules[__name__])
    reload(img_loader)
    reload(panel)
