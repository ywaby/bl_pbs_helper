# blender --background -P install.py
import bpy
import os
import glob
import shutil
PRESET_SUBDIR = "pbs_helper/bake_type"
# install

def install():
    bpy.ops.preferences.addon_install(filepath='./pbs_helper.zip')
    preset_dir = bpy.utils.preset_paths(PRESET_SUBDIR)[0]
    if not os.path.exists(preset_dir):
        os.makedirs(preset_dir)
    for filename in glob.glob('./preset/pbs_helper/bake_type/*.blend'):
        shutil.copy(filename, preset_dir)
    bpy.ops.preferences.app_template_install(filepath='texture_generate_templete.zip')
# pure uninstall
# if addon exist
#     uninstall exist
# if templete exist
#     uninstall templete
# if preset exist
#     unisntall preset
