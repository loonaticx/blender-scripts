"""
Script converts meshes materials to use their vertex colors multiplied with the existing texture,
so that vertex colors can be previewed in the viewport.

Note: Be mindful that you will likely need to run the bsdf export script before trying to export to another
file format.
"""

import bpy

from bpy.types import Material, Mesh


def get_vcol_name(mesh: Mesh, attr_name: str = 'Col'):
    """
    Ensure the specified color attribute exists on the given mesh.
    If it doesn't exist, create it with default white color.
    """
    # Check existing color attributes
    existing_attr_names = [color_attr.name for color_attr in mesh.color_attributes]
    if attr_name in existing_attr_names:
        return attr_name

    # Return the first available color attribute if any...
    if existing_attr_names:
        return existing_attr_names[0]

    # Create a new color attribute
    color_attr = mesh.color_attributes.new(name=attr_name, domain='POINT', type='FLOAT_COLOR')

    # Initialize the color data with white
    for loop_index in range(min(len(mesh.loops), len(color_attr.data))):
        color_attr.data[loop_index].color = (1.0, 1.0, 1.0, 1.0)

    return attr_name


def convert_material(material: Material, attr_name: str):
    """
    Modify the material to include a color attribute multiplied with an existing texture.
    """
    if material.node_tree:
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        # Find the existing texture node, if any
        texture_node = next((node for node in nodes if node.type == 'TEX_IMAGE'), None)

        # Clear existing nodes except the texture node
        for node in list(nodes):
            if node != texture_node:
                nodes.remove(node)

        # Add a Vertex Color node
        color_attr_node = nodes.new(type='ShaderNodeVertexColor')
        color_attr_node.layer_name = attr_name
        color_attr_node.location = (-400, -200)

        # Add a Mix RGB node for multiplication
        mix_node = nodes.new(type='ShaderNodeMixRGB')
        mix_node.blend_type = 'MULTIPLY'
        mix_node.inputs[0].default_value = 1.0  # Set factor to 1 for full multiplication
        mix_node.location = (-200, 0)

        # Add a Material Output node
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (200, 0)

        # Link the nodes
        if texture_node:
            links.new(texture_node.outputs['Color'], mix_node.inputs[1])
        links.new(color_attr_node.outputs['Color'], mix_node.inputs[2])
        links.new(mix_node.outputs['Color'], output_node.inputs['Surface'])


# Process all mesh objects in the scene
for obj in bpy.data.objects:
    if obj.type == 'MESH' and obj.data:
        attr_name = get_vcol_name(obj.data, attr_name='Col')
        for material_slot in obj.material_slots:
            material = material_slot.material
            if material and material.use_nodes:
                # Update Vertex Color node with the correct attribute
                for node in material.node_tree.nodes:
                    if node.type == 'VERTEX_COLOR':
                        node.layer_name = attr_name
                convert_material(material, attr_name)

print("Conversion completed.")
