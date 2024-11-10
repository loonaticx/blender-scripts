"""
Use to sanitize material names and image names in Blender.
Renames them to the name of the image file, differentiated by "_MTL" and "_IMG" suffixes.

"""

import bpy
import os


def rename_texnodes():
    for material in bpy.data.materials:
        if material.node_tree:
            for node in material.node_tree.nodes:
                if node.type == 'TEX_IMAGE' and node.image:
                    # replace assets with // since that prolly implies its stored in the file itself
                    image_filepath = node.image.filepath.replace("//", "")
                    image_basename = os.path.basename(image_filepath)
                    image_filename = os.path.splitext(image_basename)[0]
                    new_material_name = f"{image_filename}"
                    material.name = new_material_name
                    new_image_name = f"{image_filename}"
                    node.image.name = new_image_name
                    break


rename_texnodes()
print("Conversion completed.")
