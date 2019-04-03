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
    Operator,
    PropertyGroup,
    AddonPreferences,
    ShaderNodeGroup
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
from mathutils import Color,Vector
import bpy
'''
bake a material to simple pbr material
'''


class Preset():
    # option
    # preset godot unity bake output# new material for preview
    # create image size， base name
    # custom preset name
    def load(self):
        pass

    def save(self):
        pass


class BakeMaterial(Operator):
    '''bake texture from a material'''
    bl_label = "Bake A Material "  # 默认text，空格搜索命令
    bl_idname = "pbs_helper.bake"  # id，脚本调用,必须为a.b的格式
    bl_options = {'REGISTER', 'UNDO'}  # 允许undo
    COMPAT_ENGINES = {'CYCLES'}

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        self.obj = bpy.context.active_object
        self.orign_mat = self.obj.active_material
        self.mat = self.orign_mat.copy()
        self.obj.active_material = self.mat
        self.tree = self.mat.node_tree
        self.nodes = self.tree.nodes
        self.links = self.tree.links
        self.output_node = [node for node in self.nodes if node.bl_idname ==
                            'ShaderNodeOutputMaterial' and node.is_active_output][0]
        # init bake set
        self.tree_parse()
        self.bake_images()
        self.obj.active_material = self.orign_mat
        bpy.data.materials.remove(self.mat)
        print(" Bake finish, save image or pack it yourself!")
        return{'FINISHED'}

    def mix_alpha(self, merge_image, alpha_image):
        pixels = merge_image.pixels[:]
        alpha_pixels = alpha_image.pixels[:]
        for i in range(3, len(pixels), 4):  # TODO use numpy for faster
            pixels[i] = alpha_pixels[i-3]
        merge_image.pixels[:] = pixels
        merge_image.update()

    def node_group_new(self, group_name: str) -> ShaderNodeGroup:
        node = self.nodes.new('ShaderNodeGroup')
        node.node_tree = bpy.data.node_groups[group_name]
        return node

    def copy_input(self, input_copy_to, input_copy_from, copy_value=True):
        if input_copy_from.links:
            self.links.new(input_copy_to, input_copy_from.links[0].from_socket)
        elif copy_value:
            input_copy_to.default_value = input_copy_from.default_value
        return

    def tree_recurse_parse(self, bake_socket, link):
        '''
        parse node = link.from_node
        '''
        from_node = link.from_node
        to_node = link.to_node

        def copy_output(output_to, link):
            '''copy link to output_to'''
            if to_node.bl_idname == 'ShaderNodeOutputMaterial':
                for link in bake_socket.links:
                    self.links.new(output_to, link.to_socket)
            else:
                self.links.new(output_to,
                               link.to_socket)

        if bake_socket.name == 'Normal' or bake_socket.name == 'Clearcoat Normal':
            if from_node.bl_idname == 'ShaderNodeMixShader':
                convert_node = self.node_group_new('Normal Blend')
                copy_output(convert_node.outputs['Normal'], link)
                self.copy_input(convert_node.inputs['Fac'],
                                from_node.inputs['Fac'])
                self.copy_input(convert_node.inputs[1],
                                from_node.inputs[1], False)
                self.copy_input(convert_node.inputs[2],
                                from_node.inputs[2], False)
            elif from_node.bl_idname == 'ShaderNodeBsdfPrincipled':
                convert_node = self.nodes.new('ShaderNodeVectorMath')
                convert_node.inputs[1].default_value = Vector((0,0,0))
                copy_output(convert_node.outputs['Vector'], link)
                self.copy_input(convert_node.inputs[0],
                                from_node.inputs[bake_socket.name],False)
            elif from_node.outputs[0].type == 'SHADER':
                self.links.remove(link)
                return
            else:
                return
        elif bake_socket.type == 'VECTOR':
            if from_node.bl_idname == 'ShaderNodeMixShader':
                convert_node = self.node_group_new('Normal Blend')
                copy_output(convert_node.outputs['Normal'], link)
                self.copy_input(convert_node.inputs['Fac'],
                                from_node.inputs['Fac'])
                self.copy_input(convert_node.inputs[1],
                                from_node.inputs[1], False)
                self.copy_input(convert_node.inputs[2],
                                from_node.inputs[2], False)
            elif from_node.bl_idname == 'ShaderNodeBsdfPrincipled':
                convert_node = self.nodes.new('ShaderNodeVectorMath')
                convert_node.inputs[1].default_value = Vector(0,0,0)
                copy_output(convert_node.outputs['Vector'], link)
                self.copy_input(convert_node.inputs[0],
                                from_node.inputs[bake_socket.name],False)
            elif from_node.outputs[0].type == 'SHADER':
                self.links.remove(link)
                return
            else:
                return
        elif bake_socket.type == 'RGBA':
            if from_node.bl_idname == 'ShaderNodeMixShader':
                convert_node = self.nodes.new('ShaderNodeMixRGB')
                copy_output(convert_node.outputs['Color'], link)
                self.copy_input(convert_node.inputs['Fac'],
                                from_node.inputs['Fac'])
                self.copy_input(convert_node.inputs[1],
                                from_node.inputs[1], False)
                self.copy_input(convert_node.inputs[2],
                                from_node.inputs[2], False)
            elif from_node.bl_idname == 'ShaderNodeBsdfPrincipled':
                convert_node = self.nodes.new('ShaderNodeMixRGB')
                convert_node.inputs['Fac'].default_value = 0
                copy_output(convert_node.outputs['Color'], link)
                self.copy_input(convert_node.inputs[1],
                                from_node.inputs[bake_socket.name])
            elif from_node.outputs[0].type == 'SHADER':
                self.links.remove(link)
                return
            else:
                return
        elif bake_socket.type == 'VALUE':
            if from_node.bl_idname == 'ShaderNodeMixShader':
                convert_node = self.node_group_new('Mix Value')
                copy_output(convert_node.outputs['Value'], link)
                self.copy_input(convert_node.inputs['Fac'],
                                from_node.inputs['Fac'])
                self.copy_input(convert_node.inputs[1],
                                from_node.inputs[1], False)
                self.copy_input(convert_node.inputs[2],
                                from_node.inputs[2], False)
            elif from_node.bl_idname == 'ShaderNodeBsdfPrincipled':
                convert_node = self.nodes.new('ShaderNodeMath')
                convert_node.inputs[1].default_value = 0
                copy_output(convert_node.outputs['Value'], link)
                self.copy_input(convert_node.inputs[0],
                                from_node.inputs[bake_socket.name])
            elif from_node.outputs[0].type == 'SHADER':
                self.links.remove(link)
                return
            else:
                return
        for node_input in convert_node.inputs:
            for link in node_input.links:
                self.tree_recurse_parse(bake_socket, link)

    def tree_parse(self):
        # Principled BSDF Bake
        shader_bake_nodes = [node for node in self.nodes
                             if node.bl_idname == 'ShaderNodeGroup' and
                             node.node_tree == bpy.data.node_groups['Principled BSDF Bake']]
        for bake_node in shader_bake_nodes:
            for output in [output for output in bake_node.outputs if output.links]:
                link = self.output_node.inputs[0].links[0]
                self.tree_recurse_parse(output, link)
        # emisssion bake
        # displacement bake
        if self.output_node.inputs['Displacement'].links:
            shader_bake_nodes = [node for node in self.nodes
                                 if node.bl_idname == 'ShaderNodeGroup' and
                                 node.node_tree == bpy.data.node_groups['Displacement Bake']]
            for bake_node in shader_bake_nodes:
                if not bake_node.outputs['Displacement'].links:
                    continue
                for link in output.links:
                    self.links.new(self.output_node.inputs['Displacement'].links[0].from_socket,
                                   link.to_socket)

    def bake_images(self):
        bake_image_nodes = [node for node in self.nodes
                            if node.bl_idname == 'ShaderNodeTexImage' and
                            node.label == 'Image Bake']
        emit_node = self.nodes.new('ShaderNodeEmission')
        self.links.new(emit_node.outputs['Emission'],
                       self.output_node.inputs['Surface'])
        for bake_image_node in bake_image_nodes:
            bake_image = bake_image_node.image
            if not bake_image_node.inputs[0].links:
                continue
            if not bake_image:
                self.report(
                    {'INFO'}, f'bake node "{bake_image_node.name}" missing image')
                continue
            before_bake_node = bake_image_node.inputs[0].links[0].from_node
            if before_bake_node == 'ShaderNodeGroup' and before_bake_node.node_tree == bpy.data.node_groups['Mix Alpha']:
                # bake color
                self.copy_input(emit_node.inputs['Color'],
                                before_bake_node.inputs['Color'])
                self.nodes.active = bake_image_node
                bpy.ops.object.bake(type='EMIT')
                # bake alpha
                self.copy_input(emit_node.inputs['Color'],
                                before_bake_node.inputs['Alpha'])
                alpha_tmp = bpy.data.images.new(
                    'alpha.tmp', bake_image.size[0], bake_image.size[1], alpha=False, float_buffer=bake_image.is_float)
                bake_alpha_node = self.nodes.new(type='ShaderNodeTexImage')
                bake_alpha_node.image = alpha_tmp
                self.nodes.active = bake_alpha_node
                bpy.ops.object.bake(type='EMIT')
                # mix alpha+color
                self.mix_alpha(bake_image, alpha_tmp)
                bpy.data.images.remove(alpha_tmp)
            else:
                self.copy_input(emit_node.inputs['Color'],
                                bake_image_node.inputs[0])
                self.nodes.active = bake_image_node
                bpy.ops.object.bake(type='EMIT')


classes = (
    BakeMaterial,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


# for test
if __name__ == "__main__":
    register()
    bpy.ops.pbs_helper.bake()
