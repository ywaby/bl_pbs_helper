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

from bpy.types import (
    Panel, Menu
)

from bpy.props import (
    BoolProperty,
    EnumProperty,
    FloatProperty,
    FloatVectorProperty,
    IntProperty,
    PointerProperty,
    StringProperty,
)


def add_image_bake(self, context):
    bake_node = self.layout.operator('pbs_helper.add_image_bake',
                                     text="Image Bake")


def is_image_bake(self, context):
    obj = context.active_object
    mat = obj.active_material
    tree = mat.node_tree
    nodes = tree.nodes
    layout = self.layout
    node = nodes.active
    if node and node.bl_idname == 'ShaderNodeTexImage':
        row = layout.row()
        row.prop(node, 'is_image_bake')


class PBS_HELPER_PT_panel(Panel):
    bl_space_type = 'NODE_EDITOR'
    bl_label = "PBS Helper"
    bl_category = 'PBS Helper'
    bl_region_type = 'UI'
    #bl_options = {'HIDE_HEADER'}
    COMPAT_ENGINES = {'CYCLES'}

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("pbs_helper.bake")



