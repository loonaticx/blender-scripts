import bpy

def convert_material_to_principled(material):
    if material.node_tree:
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
            if node.type == 'BSDF_DIFFUSE' or node.type == 'BSDF_GLOSSY' or node.type == 'BSDF_PRINCIPLED':
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
