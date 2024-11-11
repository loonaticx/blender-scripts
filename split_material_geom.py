"""
Used to split out meshes by material into separate objects.
Also renames the objects to match the material names.

Note: Recommended to run the rename_texnodes.py script first to sanitize material names.
"""

import bpy


def sanitize_name(name):
    # Replace non-UTF-8 or problematic characters with underscores
    return ''.join([c if ord(c) < 128 else '_' for c in name])


def separate_mesh_by_material():
    # Get the active object (must be a mesh)
    obj = bpy.context.active_object

    if obj is None or obj.type != 'MESH':
        print("Please select a mesh object.")
        return

    # Ensure the object is in object mode before starting
    bpy.ops.object.mode_set(mode='OBJECT')

    # Deselect all objects to ensure only the active one is processed
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    # Enter edit mode to select and separate by material
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')

    # Get the list of materials
    materials = obj.data.materials

    if not materials:
        print("No materials found on the object.")
        bpy.ops.object.mode_set(mode='OBJECT')
        return

    # Iterate through materials and separate by each
    for i, material in enumerate(materials):
        # Ensure correct material slot is active
        obj.active_material_index = i

        # Select faces by material index
        bpy.ops.object.material_slot_select()

        # Check if any faces are selected before separating
        bpy.ops.object.mode_set(mode='OBJECT')
        if len([face for face in obj.data.polygons if face.select]) == 0:
            print(f"No faces found for material: {material.name}")
            bpy.ops.object.mode_set(mode='EDIT')
            continue
        bpy.ops.object.mode_set(mode='EDIT')

        # Separate the selection into a new object
        bpy.ops.mesh.separate(type='SELECTED')

        # Go back to object mode to rename
        bpy.ops.object.mode_set(mode='OBJECT')

        # Get the newly created object and rename it
        new_obj = bpy.context.selected_objects[-1]
        sanitized_name = sanitize_name(material.name)
        new_obj.name = sanitized_name
        new_obj.data.name = f"{sanitized_name}"

        # Assign only the relevant material to the new object
        new_obj.data.materials.clear()
        new_obj.data.materials.append(material)

        # Return to edit mode to process the next material
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')

    # Return to object mode when done
    bpy.ops.object.mode_set(mode='OBJECT')
    print("Separation complete.")


# Run the function
separate_mesh_by_material()
