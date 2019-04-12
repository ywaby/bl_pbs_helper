# blender --background -P uninstall.py
'''pure uninstall'''

import sys
import bpy
import os
import glob
import shutil
PRESET_SUBDIR = "pbs_helper/bake_type"
# remove addon
bpy.ops.preferences.addon_disable(module="pbs_helper")
bpy.ops.wm.save_userpref()
bpy.ops.preferences.addon_remove(module="pbs_helper")

# remove app templete
# paths=bpy.utils.app_template_paths('bitmap2tex_templete')
# for path in paths
#     shutil.rmtree(path)
target = os.path.expanduser(
    "~/.config//blender/2.80/scripts/startup/bl_app_templates_user/bitmap2tex_templete")
if os.path.exists(target):
    shutil.rmtree(target)
# remove presets
paths = bpy.utils.preset_paths(PRESET_SUBDIR)
for path in paths:
        shutil.rmtree(path)
