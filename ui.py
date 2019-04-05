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
    Panel,
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

class UI(Panel):
    bl_space_type = 'NODE_EDITOR'
    bl_label = "PBS Helper"
    bl_category = 'PBS Helper'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        row=layout.row()
        row.label(text="Hello World")
        row=layout.row()
        row.operator("pbs_helper.bake")