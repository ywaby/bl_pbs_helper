
import os  
from bl_operators.presets import AddPresetBase
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
PRESET_SUBDIR = "pbs_helper/bake_type"


def add_presets(self, context):
    bake_node = self.layout.menu("PBS_HELPER_MT_preset", text='Bake Presets')


class PBS_HELPER_MT_add_presets(Menu):
    """preset menu by finding all preset files in the preset directory"""
    bl_label = "Material Bake Presets"
    preset_subdir = PRESET_SUBDIR
    draw = Menu.draw_preset
    preset_operator = 'pbs_helper.use_preset'  # run preset
    preset_extensions = {'.blend'}


class PBS_HELPER_PT_presets_manager(Panel):
    bl_space_type = 'NODE_EDITOR'
    bl_label = "Preset Manager"
    bl_category = 'PBS Helper'
    bl_region_type = 'UI'
    # bl_options = {'HIDE_HEADER'}
    @classmethod
    def poll(cls, context):
        # area is shadernode and active_material!=None
        return True

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.menu("PBS_HELPER_MT_preset")
        row.operator('pbs_helper.preset_add', text="", icon='ADD')
        row.operator('pbs_helper.preset_add', text="",
                     icon='REMOVE').remove_active = True


class PBS_HELPER_MT_preset(Menu):
    """preset menu by finding all preset files in the preset directory"""
    bl_label = "Material Bake Presets"
    preset_subdir = PRESET_SUBDIR
    draw = Menu.draw_preset
    preset_operator = 'pbs_helper.use_preset'  # run preset
    preset_extensions = {'.blend'}


class UsePreset(Operator):
    bl_idname = "pbs_helper.use_preset"
    bl_label = "Execute a Python Preset"

    filepath: StringProperty(
        subtype='FILE_PATH',
        options={'SKIP_SAVE'},
    )
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and
                obj.active_material and
                context.area.type == "NODE_EDITOR")

    def execute(self, context):
        obj = context.active_object
        mat = obj.active_material
        # append data
        with bpy.data.libraries.load(self.filepath, link=False) as (data_from, data_to):
            data_to.materials = data_from.materials
            data_to.node_groups = data_from.node_groups
        # apply data
        node_group = data_to.node_groups[0]
        bpy.ops.node.add_node('INVOKE_DEFAULT',
                              type="ShaderNodeGroup",
                              # use_transform=True
                              )
        mat.node_tree.nodes.active.node_tree = node_group
        bpy.ops.node.group_ungroup()
        bpy.ops.node.translate_attach_remove_on_cancel('INVOKE_DEFAULT')
        return {'FINISHED'}


class AddPreset(AddPresetBase, Operator):
    """add preset to library"""
    bl_label = "Add Preset"
    bl_idname = "pbs_helper.preset_add"
    preset_subdir = PRESET_SUBDIR
    preset_menu = 'PBS_HELPER_MT_preset'
    name: StringProperty(
        name="Name",
        description="Name of the preset, used to make the path name",
        maxlen=64,
        options={'SKIP_SAVE'},
    )
    remove_active: BoolProperty(
        default=False,
        options={'HIDDEN', 'SKIP_SAVE'},
    )
    remove_name: BoolProperty(
        default=False,
        options={'HIDDEN', 'SKIP_SAVE'},
    )
    ext = '.blend'
    # TODO when is possible use PointerProperty
    mat_name: StringProperty(name="Preview Material")
    node_name: StringProperty(name="bake node_group  ")

    def execute(self, context):
        if not self.remove_active:
            if self.node_name == '':
                return {'CANCELLED'}
            node_group = bpy.data.node_groups[self.node_name]
            filename = self.name+self.ext
            filepath = os.path.join(bpy.utils.preset_paths(self.preset_subdir)[0],
                                    filename)
            data_blocks = [node_group]
            if not self.mat_name == '':
                mat = bpy.data.materials[self.mat_name]
                data_blocks.append(mat)
            bpy.data.libraries.write(filepath, set(data_blocks))
        else:
            preset_menu_class = getattr(bpy.types, self.preset_menu)
            preset_active = preset_menu_class.bl_label
            filepath = bpy.utils.preset_find(preset_active,
                                             self.preset_subdir,
                                             ext=self.ext)
            if not filepath:
                filepath = bpy.utils.preset_find(preset_active,
                                                 self.preset_subdir,
                                                 display_name=True,
                                                 ext=self.ext)
            if not filepath:
                return {'CANCELLED'}
            try:
                if hasattr(self, "remove"):
                    self.remove(context, filepath)
                else:
                    os.remove(filepath)
            except Exception as e:
                self.report({'ERROR'}, "Unable to remove preset: %r" % e)
                import traceback
                traceback.print_exc()
                return {'CANCELLED'}
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "name")
        row = layout.row()
        row.prop_search(self, "mat_name", bpy.data, "materials")
        row.prop_search(self, "node_name", bpy.data, "node_groups")


classes = [AddPreset,
           PBS_HELPER_MT_add_presets,
           PBS_HELPER_MT_preset,
           PBS_HELPER_PT_presets_manager,
           UsePreset]


def register():
    bpy.utils.user_resource('SCRIPTS',
                            path="presets/"+PRESET_SUBDIR,
                            create=True)
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.NODE_MT_add.append(add_presets)


def unregister():
    bpy.types.NODE_MT_add.remove(add_presets)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
