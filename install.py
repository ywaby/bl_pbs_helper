# blender --background -P install.py
import sys
import bpy
import os
import glob
import shutil
import distutils.dir_util

PRESET_SUBDIR = "pbs_helper/bake_type"
# addon_install
bpy.ops.preferences.addon_install(filepath='./pbs_helper_addon.zip')
# preset copy and override
preset_dir =bpy.utils.user_resource('SCRIPTS', "presets/pbs_helper")
distutils.dir_util.copy_tree('./presets/pbs_helper', preset_dir)
# fix link broke
# app_template
bpy.ops.preferences.app_template_install(
    filepath='bitmap2tex_templete.zip')
