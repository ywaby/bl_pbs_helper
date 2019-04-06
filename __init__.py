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
from .ui import PBS_HELPER_PT_panel
from .material_bake import BakeMaterial,AddImageBake
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
from os import path
from mathutils import Color
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


class auto_rotate_light(bpy.types.Operator):
    '''preivew light rotate around active object'''
    pass


def init_addon():
    addon_dir = path.dirname(__file__)
    data = path.join(addon_dir, "./data.blend")
    # link workspace not work as need to oprater
    # if 'PBR' not in bpy.data.workspaces.keys():
        # bpy.ops.wm.link(directory="./data.blend/WorkSpace", filename="PBR",relative_path=True)
        
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
    user_data : StringProperty(name='User Data file(*.blend)',subtype='FILE_PATH',description='default is addon data.blend')
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(self, "sync_paint_node")
        row.prop(self, "auto_save_image")
        row = layout.row()
        row.prop(self, "user_data")

classes = [
    BakeMaterial,
    AddImageBake,
    # Paint2Node,
    PBS_HELPER_PT_panel,
    Preferences
]

def add_image_bake(self, context):
    bake_node=self.layout.operator(AddImageBake.bl_idname,
                        text = "Image Bake")

def register():
    bpy.types.ShaderNodeTexImage.is_image_bake=BoolProperty(name='Is Image Bake',default=False)
    for cls in classes:
        bpy.utils.register_class(cls)
    init_addon()
    bpy.types.NODE_MT_add.append(add_image_bake)

def unregister():
    bpy.types.NODE_MT_add.remove(add_image_bake)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.ShaderNodeTexImage.is_image_bake
