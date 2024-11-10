"""
Use to sanitize material names and image names in Blender.
Renames them to the name of the image file, differnetiated by "_MTL" and "_IMG" suffixes.

"""

import bpy
import os


def rename_texnodes():
    for material in bpy.data.materials:
        if material.node_tree:
            for node in material.node_tree.nodes:
                if node.type == 'TEX_IMAGE' and node.image:
                    image_filepath = node.image.filepath
                    image_basename = os.path.basename(image_filepath)
                    image_filename = os.path.splitext(image_basename)[0]
                    # "_Mtl" suffix because blender doesn't like anything with identical names
                    new_material_name = f"{image_filename}_MTL"
                    material.name = new_material_name
                    new_image_name = f"{image_filename}_IMG"
                    node.image.name = new_image_name
                    break


rename_texnodes()
print("Conversion completed.")
