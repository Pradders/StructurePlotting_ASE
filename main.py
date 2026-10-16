import os #System
import glob #File locations

from load import load_atoms, get_reference_structure, check_reference_structure
from inputs import choose_shift_mode
from shift import get_structure_shift,apply_shift
from plotting import plot_surface_views, prepare_visual_structure

# Reference structure settings

# IMPORTANT:
# Ensure that the reference structure and input structures have compatible unit cell dimensions and orientation, and that the selected substrate atoms are listed in the same order.
# The reference structure is used to provide a consistent substrate representation in the plotted structures.
# If the atoms and unit cell do not match, then include_reference should be set to False.

include_reference = True

# Folder containing the reference CONTCAR/POSCAR. The folder is called "Reference" by default, but this can be altered.
# Set include_reference = False to process structures without an external reference.
reference_folder = "Reference" if include_reference else None

# Reference structure settings
if include_reference:

    # Elements that belong to the reference substrate
    reference_symbols = ("Ni",)

    #Collect the atoms within the reference folder
    reference_atoms = get_reference_structure(
        reference_folder,
        repeat=(1, 1, 1)
    )
else:
    reference_symbols = None
    reference_atoms = None

# Find structure files
structure_files = [
    file for file in glob.glob("**/CONTCAR", recursive=True)
    if reference_folder is None or os.path.basename(os.path.dirname(file)) != reference_folder
    ] + [
    file for file in glob.glob("**/POSCAR", recursive=True)
    if (reference_folder is None or os.path.basename(os.path.dirname(file)) != reference_folder)
    and not any(
        os.path.dirname(file) == os.path.dirname(c)
        for c in glob.glob("**/CONTCAR", recursive=True)
    )
    ]
print(f"Found {len(structure_files)} structure files.")

# Shift
shift_mode = choose_shift_mode()

# Figure
figsize = (12, 6)
dpi = 300
# Font
font_family = "Times New Roman"
font_size = 24
title_size = 24
font_weight = "bold"
# Colours
element_colors = {
    "Ni": "lightgray",
    "C": "black"}

# Output directory
output_folder = "Figures"

os.makedirs(output_folder,exist_ok=True)

# Process each structure
for file in structure_files:
    # Load structure
    atoms = load_atoms(file,repeat=(1, 1, 1))
    # Apply shift
    if shift_mode != 3:
        shift = get_structure_shift(atoms,shift_mode)
        shifted_atoms = apply_shift(atoms,shift)
    else:
        shifted_atoms = atoms.copy()

    # Check and prepare reference structure
    if reference_atoms is not None:
        check_reference_structure(shifted_atoms,reference_atoms,reference_symbols)
        visual_atoms = prepare_visual_structure(shifted_atoms,reference_atoms,reference_symbols)
    else:
        visual_atoms = shifted_atoms.copy()

    # Get folder name
    system_name = os.path.basename(os.path.dirname(file))
    # Output filename
    output_filename = os.path.join(output_folder,system_name + ".png")
    print(f"\nProcessing: {file}")
    print(f"Output: {output_filename}")

    # Plot
    plot_surface_views(visual_atoms,output_filename=output_filename,figsize=figsize,dpi=dpi,title_size=title_size,
                       font_size=font_size,font_family=font_family,font_weight=font_weight,element_colors=element_colors)