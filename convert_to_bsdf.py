"""
Converts materials to use the Principled BSDF shader node, which is needed when exporting out of Blender.
"""

import bpy

from bpy.types import Material


def convert_material_to_principled(material: Material):
    if not material.node_tree:
        return
    nodes = material.node_tree.nodes
    links = material.node_tree.links

    # Find existing texture node
    texture_node = None
    for node in nodes:
        if node.type == 'TEX_IMAGE':
            texture_node = node
            break

    # Remove existing shader nodes
    for node in nodes:
        if str(node.type).startswith("BSDF_"):
            nodes.remove(node)

    # Add a Principled BSDF node
    principled_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled_node.location = (200, 0)

    # Add a Material Output node if it doesn't exist
    output_node = None
    for node in nodes:
        if node.type == 'OUTPUT_MATERIAL':
            output_node = node
            break
    if not output_node:
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (400, 0)

    # Link texture node to Principled BSDF if found
    if texture_node:
        links.new(texture_node.outputs['Color'], principled_node.inputs['Base Color'])

    # Link Principled BSDF to Material Output
    links.new(principled_node.outputs['BSDF'], output_node.inputs['Surface'])


# Loop through all materials in the scene and convert them
for material in bpy.data.materials:
    if material.use_nodes:
        convert_material_to_principled(material)

print("Conversion to Principled BSDF completed.")
