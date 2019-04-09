# Copyright (C) 2019 ywabygl@gmail.com
#
# PBS Helper is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PBS Helper is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with PBS Helper. If not, see <http://www.gnu.org/licenses/>.
# TODO clear import
import os
from bl_operators.presets import AddPresetBase
from os import path
from .ui import PBS_HELPER_PT_panel, add_image_bake, is_image_bake
from .material_bake import BakeMaterial, AddImageBake
#from .paint import Paint2Node
from bpy.props import (
    BoolProperty,
    EnumProperty,
    FloatProperty,
    FloatVectorProperty,
    IntProperty,
    PointerProperty,
    StringProperty,
)
from bpy.types import (
    Operator,
    Menu,
    Panel,
    PropertyGroup,
    AddonPreferences,
)
import bpy

bl_info = {
    "name": "PBS Helper",
    "author": "ywaby",
    "version": (0, 0, 2),
    "description": "shader bake"
    'material merge'
    'pbr paint helper',
    "blender": (2, 80, 0),
    "location": "Shader Node->Properties",
    "warning": "",
    "tracker_url": "http://github.com/pbr_helper/issue",
    "wiki_url": "http://github.com/pbr_helper/wiki",
    "support": "TESTING",
    "category": "Node"
}



class Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    sync_paint_node: BoolProperty(
        name='Paint To Node',
        default=True,
        description='Paint to Active Node'
    )
    auto_save_image: BoolProperty(
        name='Auto Save Image',
        default=True,
        description=''
    )

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(self, "sync_paint_node")
        row.prop(self, "auto_save_image")
        row = layout.row()

classes = [
    BakeMaterial,
    AddImageBake,
    # Paint2Node,
    PBS_HELPER_PT_panel,
    Preferences,
]
from .preset import register as preset_register
from .preset import unregister as preset_unregister

def register():
    preset_register()
    bpy.types.Scene.target_object = StringProperty()
    bpy.types.Scene.target_mat = PointerProperty(type=bpy.types.Material)
    bpy.types.ShaderNodeTexImage.is_image_bake = BoolProperty(
        name='Is Image Bake', default=False)
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.NODE_MT_add.append(add_image_bake)
    bpy.types.NODE_PT_active_node_properties.append(is_image_bake)


def unregister():
    bpy.types.NODE_PT_active_node_properties.remove(is_image_bake)
    bpy.types.NODE_MT_add.remove(add_image_bake)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.ShaderNodeTexImage.is_image_bake
    preset_unregister()

