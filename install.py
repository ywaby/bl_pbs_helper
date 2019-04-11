# blender --background -P install.py
import sys
import bpy
import os
import glob
import shutil
PRESET_SUBDIR = "pbs_helper/bake_type"

def install():
    bpy.ops.preferences.addon_install(filepath='./pbs_helper.zip')
    preset_dir = bpy.utils.preset_paths('pbs_helper')[0]
    if not os.path.exists(preset_dir):
        os.makedirs(preset_dir)
    shutil.copytree('./presets/pbs_helper', preset_dir)
    bpy.ops.preferences.app_template_install(
        filepath='texture_generate_templete.zip')

def uninstall():
    '''pure uninstall'''
    # remove addon
    bpy.ops.preferences.addon_remove(module="pbs_helper")
    # remove app templete 
    # paths=bpy.utils.app_template_paths(texture_generate_templete)
    # for path in paths
    #     shutil.rmtree(path)
    target = os.path.expanduser("~/.config//blender/2.80/scripts/startup/bl_app_templates_user/texture_generate_templete")
    shutil.rmtree(target)
    # remove presets
    paths = bpy.utils.preset_paths(PRESET_SUBDIR)
    for path in paths
        shutil.rmtree(path)

if '-U' in sys.argv:
    uninstall()
else:
    install()
