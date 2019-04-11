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
# TODO
# 1. clear import
# 2. only poll for shader node editor
#
import os
from .preset import register as preset_register, unregister as preset_unregister
from .ui import PBS_HELPER_PT_panel
from .material_bake import BakeMaterial
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
    AddonPreferences, Operator
)
import bpy

bl_info = {
    "name": "PBS Helper",
    "author": "ywaby",
    "version": (0, 1, 2),
    "description": "shader bake"
    'material merge'
    'pbr paint helper',
    "blender": (2, 80, 0),
    "location": "Shader Node->Properties->PBS Hepler",
    "warning": "",
    "tracker_url": "http://github.com/ywaby/bl_pbs_helper/issue",
    "wiki_url": "http://github.com/ywaby/bl_pbs_helper",
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


# ((id, name, dest),...) node group name==id
PBS_NODE_TYPES = (('Build In', 'Build In', ''),
                  ('PBSH Emission Bake', 'PBSH Emission Bake', ''),
                  ('PBSH Principled BSDF Bake', 'PBSH Principled BSDF Bake', ''),
                  ('PBSH Displacement Bake', 'PBSH Displacement Bake', ''),
                  ('PBSH Image Bake', 'PBSH Image Bake', ''),
                  ('PBSH Mix Alpha', 'PBSH Mix Alpha', ''))

PBS_NODE_ADD_TYPES = (
    ('PBSH Emission Bake', 'PBSH Emission Bake', ''),
    ('PBSH Principled BSDF Bake', 'PBSH Principled BSDF Bake', ''),
    ('PBSH Displacement Bake', 'PBSH Displacement Bake', ''),
    ('PBSH Image Bake', 'PBSH Image Bake', ''),
    ('PBSH Mix Alpha', 'PBSH Mix Alpha', ''))


class FixData(Operator):
    '''add godot bake preset,fix broken link node group'''
    bl_label = "fix Data"
    bl_idname = "pbs_helper.fix_data"
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and
                obj.active_material and
                context.area.type == "NODE_EDITOR")

    def execute(self, context):
        data_path = os.path.join(os.path.dirname(__file__), 'data.blend')
        with bpy.data.libraries.load(data_path, link=True) as (data_from, data_to):
            data_to.node_groups = data_from.node_groups
        mats = context.materials
        for mat in mats:
            tree = mat.node_tree
            nodes = tree.nodes
            for node in nodes:
                if node.pbs_node_type != 'Build In' and node.bl_idname == 'ShaderNodeGroup':
                    node.node_tree = bpy.data.node_groups[node.pbs_node_type]
        return {"FINISHED"}


class AddPBSHplerNode(Operator):
    bl_idname = 'pbs_helper.add_shader_bake_node'
    bl_label = 'Add A PBS Helper Node'
    node_type: EnumProperty(items=PBS_NODE_ADD_TYPES,
                            default='PBSH Image Bake',
                            name='PBS Node Type')

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and
                obj.active_material and
                context.area.type == "NODE_EDITOR")

    def execute(self, context):
        if self.node_type == 'Build In':
            return {'CANCELLED'}
        data_path = os.path.join(os.path.dirname(__file__), 'data.blend')  # TODO to be func load all
        with bpy.data.libraries.load(data_path, link=True) as (data_from, data_to):
            data_to.node_groups = data_from.node_groups
        obj = context.active_object
        mat = obj.active_material
        tree = mat.node_tree
        nodes = tree.nodes
        bpy.ops.node.add_node('INVOKE_DEFAULT',
                              type="ShaderNodeGroup",)
        node = nodes.active
        node.node_tree = bpy.data.node_groups[self.node_type]
        node.pbs_node_type = self.node_type
        bpy.ops.node.translate_attach_remove_on_cancel('INVOKE_DEFAULT')
        return {'FINISHED'}


def add_PBS_helper_nodes(self, context):
    self.layout.operator_menu_enum(AddPBSHplerNode.bl_idname,
                                   "node_type",
                                   text="Add PBS helper Nodes")  # sub menu


classes = [
    BakeMaterial, AddPBSHplerNode,
    PBS_HELPER_PT_panel,
    Preferences, FixData,
]


def bake_type_set(self, context):
    obj = context.active_object
    mat = obj.active_material
    tree = mat.node_tree
    nodes = tree.nodes
    layout = self.layout
    node = nodes.active
    row = layout.row()
    row.prop(node, 'pbs_node_type')

def register():
    preset_register()
    bpy.types.Scene.target_object = StringProperty()
    bpy.types.Scene.target_mat = PointerProperty(type=bpy.types.Material)
    bpy.types.ShaderNode.pbs_node_type = EnumProperty(items=PBS_NODE_TYPES,
                                                      name='PBS Node Type',
                                                      default='Build In')
    for cls in classes:
        bpy.utils.register_class(cls)
    # bpy.types.NODE_MT_add.append(add_image_bake)
    bpy.types.NODE_MT_add.append(add_PBS_helper_nodes)
    bpy.types.NODE_PT_active_node_properties.append(bake_type_set)


def unregister():
    bpy.types.ShaderNode.remove(pbs_node_type)
    # bpy.types.NODE_MT_add.remove(add_image_bake)
    bpy.types.NODE_MT_add.remove(add_PBS_helper_nodes)
    bpy.types.NODE_PT_active_node_properties.remove(bake_type_set)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.ShaderNodeTexImage.is_image_bake
    preset_unregister()
