bl_info = {
    "name": "A Structured Add-on",
    "author": "Naman Deep",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "description": "Add-on consisting of multiple files",
    "category": "Learning",
}
#Testing Repo
import bpy
from . import img_loader
from . import panel
from . import _refresh_
from . import preferences

_refresh_.reload_modules()
# from importlib import reload

# Adding functionality for the addon to update its file during development
# Using importlib
# reload(img_loader)
# reload(panel)

def register():
    img_loader.register_icons()
    preferences.register_classes()
    panel.register_classes()

def unregister():
    panel.unregister_classes()
    preferences.unregister_classes()
    img_loader.unregister_icons()
    
