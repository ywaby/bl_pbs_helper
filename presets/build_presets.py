presets = [{'name': 'godot', 'node_group': "Godot", 'mat': 'Godot'},
           {'name': 'bitmap2tex', 'node_group': "Bitmap2Tex", 'mat': ''},
           {'name': 'unity_spec', 'node_group': "UnitySpec", 'mat': 'UnitySpec'},
           {'name': 'unity_meta', 'node_group': "UnityMeta", 'mat': 'UnityMeta'},
           ]
import bpy
for preset in presets:
    bpy.ops.pbs_helper.preset_add(name=preset['name'],
                                  mat_name=preset['mat'],
                                  node_group_name=preset['node_group'])
