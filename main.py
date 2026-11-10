import os #System

from load import load_atoms, get_reference_structure
from inputs import choose_shift_mode, get_reference_settings
from shift import get_structure_shift,apply_shift
from plotting import plot_surface_views, prepare_visual_structure

#Define the main function to run imported functions
def main():

    # Optional reference surface for consistent substrate visualisation.
    # Ensure the reference and input structures have compatible cell dimensions, cell orientation, and ordering of the selected substrate atoms.
    # The reference is for visualisation.

    # Reference structure settings
    reference_symbols = ("Ni",) #This can be ignored or changed to None unless an element(s) is to be specified
    reference_folder = "Reference" #This can be ignored or changed to None unless a folder is to be specified
    reference_folder, reference_symbols = get_reference_settings(reference_symbols,reference_folder)

    # Load external reference structure if required
    reference_atoms = (get_reference_structure(reference_folder, repeat=(1, 1, 1)) if reference_folder is not None else None)

    # Find structure files
    structure_files = []

    for root, dirs, files in os.walk("."):

        # Exclude the reference folder and its contents
        if reference_folder is not None:
            reference_path = os.path.abspath(reference_folder)
            current_path = os.path.abspath(root)

            if os.path.commonpath((reference_path, current_path)) == reference_path:
                dirs.clear()
                continue

        # Prefer CONTCAR over POSCAR
        if "CONTCAR" in files:
            structure_files.append(os.path.join(root, "CONTCAR"))
        elif "POSCAR" in files:
            structure_files.append(os.path.join(root, "POSCAR"))

    if not structure_files:
        raise FileNotFoundError("No POSCAR or CONTCAR files were found outside the reference folder.")
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
        "C": "black"
        }

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

        # Prepare visual structure using the external reference, if supplied
        if reference_atoms is not None:
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

#Entry point/switch to run function
if __name__ == "__main__":
    #Load the main function
    main()