from bpy.utils import previews
import os

# Gloabl list for our previews collection
# Follwiing the name with underscore means private member
_CUSTOM_ICONS = None

def get_icons_collection():
    """ Get icons loaded from folder"""
    register_icons()

    # will cause error if variable isn't set despite our previous statement
    assert _CUSTOM_ICONS # if None Something is wrong
    return _CUSTOM_ICONS

def register_icons():
    """ Load icons from the add-on folder"""
    global _CUSTOM_ICONS
    if _CUSTOM_ICONS:
        # the collection list is already stored
        return
    
    collection = previews.new()
    img_extensions = ('.png','.jpg','.tif')

    # path function from os is preferred for multi-platform compatibility
    
    module_path = os.path.dirname(__file__)
    picture_path = os.path.join(module_path, 'pictures')

    # os.listdir returns a list of all filenames in directory
    for img_file in os.listdir(picture_path):
        img_name, ext = os.path.splitext(img_file)
        if ext.lower() not in img_extensions:
            continue

        disk_path = os.path.join(picture_path, img_file)
        collection.load(img_name, disk_path, 'IMAGE')

    _CUSTOM_ICONS = collection


def unregister_icons():
    """ Removing the icons when disabled"""
    global _CUSTOM_ICONS
    if _CUSTOM_ICONS:
        previews.remove(_CUSTOM_ICONS)
    # Making the global list to None
    _CUSTOM_ICONS = None