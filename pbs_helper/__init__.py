# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "PBS Helper",
    "author" : "ywaby",
    "version": (0, 0, 2),
    "description": "shader bake"
                    'material merge'
                    'pbr paint helper',
    "blender" : (2, 80, 0),
    "location" : "Shader Node->Properties",
    "warning" : "",
    "tracker_url": "http://github.com/pbr_helper/issue",
    "wiki_url": "http://github.com/pbr_helper/wiki",
    "support": "TESTING",
    "category": "Node"
}
import bpy
from os import path
from mathutils import Color
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

# pbr generate env init
class UI(bpy.types.Panel):
    bl_space_type = 'NODE_EDITOR'
    bl_label = "pbr helper"
    bl_category = 'Properties'
    bl_region_type = 'PROPERTIES'
    bl_idname = 'pbr_helper.bake'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        col = layout.col
        col = layout.col




class auto_rotate_light(bpy.types.Operator):
    '''preivew light rotate around active object'''
    pass

def init_addon():
    # addon preference
    # check and init env for bake
    # cycle engine
    # autopack image
    addon_dir = path.dirname(__file__)
    data = path.join(addon_dir, "./data.blend")

class PBS_Helper(bpy.types.AddonPreferences):
    bl_idname = __name__
    sync_paint_node=BoolProperty(
        name='Sync Node Paint',
        default=True,
        description='Sync Active Shader Node With Paint Texture'
    )
    def draw(self, context):
            layout = self.layout
            col = layout.column()
            col.prop(self, "sync_paint_node")

# append workspace PBR
def register():
    init_addon()
    auto_load.register()

def unregister():
    auto_load.unregister()

classes = (
    BakeMaterial,
)
def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
