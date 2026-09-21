import os #System
import glob #File locations

from load import load_atoms
from inputs import choose_shift_mode
from shift import get_structure_shift,apply_shift
from plotting import plot_surface_views

# Find structure files
contcars = glob.glob("**/CONTCAR*", recursive=True)
structure_files = contcars + [file for file in glob.glob("**/POSCAR*", recursive=True)
    if not any(os.path.dirname(file) == os.path.dirname(c) for c in contcars)]
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
    shift = get_structure_shift(atoms,shift_mode)
    atoms = apply_shift(atoms,shift)

    # Get folder name
    system_name = os.path.basename(os.path.dirname(file))
    # Output filename
    output_filename = os.path.join(output_folder,system_name + ".png")
    print(f"\nProcessing: {file}")
    print(f"Output: {output_filename}")

    # Plot
    plot_surface_views(atoms,output_filename=output_filename,figsize=figsize,dpi=dpi,title_size=title_size,
                       font_size=font_size,font_family=font_family,font_weight=font_weight,element_colors=element_colors)