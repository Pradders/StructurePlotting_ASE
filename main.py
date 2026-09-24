import os #System
import glob #File locations

from load import load_atoms, get_reference_structure, check_reference_structure
from inputs import choose_shift_mode
from shift import get_structure_shift,apply_shift
from plotting import plot_surface_views, prepare_visual_structure

# Find structure files
#contcars = glob.glob("**/CONTCAR*", recursive=True)
#structure_files = contcars + [file for file in glob.glob("**/POSCAR*", recursive=True)
#    if not any(os.path.dirname(file) == os.path.dirname(c) for c in contcars)]
#print(f"Found {len(structure_files)} structure files.")

# Optional reference structure used to keep the substrate representation consistent across different systems.
# Use reference_folder = None to analyse structures without an external reference.
# Else, direct the variable to the folder containing the relevant CONTCAR/POSCAR file.
reference_folder = "Reference"
#reference_folder = None

include_reference = True

# Find structure files
structure_files = [
    file for file in glob.glob("**/CONTCAR*", recursive=True)
    if reference_folder is None or os.path.basename(os.path.dirname(file)) != reference_folder
    ] + [
    file for file in glob.glob("**/POSCAR*", recursive=True)
    if (reference_folder is None or os.path.basename(os.path.dirname(file)) != reference_folder)
    and not any(
        os.path.dirname(file) == os.path.dirname(c)
        for c in glob.glob("**/CONTCAR*", recursive=True)
    )
    ]
print(f"Found {len(structure_files)} structure files.")

# Elements that belong to the reference substrate
reference_symbols = ("Ni",)

if reference_folder is not None:
    reference_atoms = get_reference_structure(
        reference_folder,
        repeat=(1, 1, 1)
    )
else:
    reference_atoms = None

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