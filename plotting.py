#Plotting tools

import os #System
import matplotlib.pyplot as plt #Plotting
from matplotlib.colors import is_color_like
import numpy as np #Numerical analysis

from load import check_reference_structure

#ASE environment
from ase.visualize.plot import plot_atoms
from ase.data.colors import jmol_colors
from ase.data import atomic_numbers, chemical_symbols #Valid chemical elements

def get_atom_colors(atoms,element_colors=None):

    # Validate user-defined colours, if provided
    if element_colors is not None:

        # Check each supplied element and its corresponding colour
        for symbol, colour in element_colors.items():

            # Check that the supplied element symbol is valid
            if symbol not in chemical_symbols[1:]:
                raise ValueError(f"Invalid chemical element symbol in element_colors: '{symbol}'.")

            # Check that the supplied colour is valid
            if not is_color_like(colour):
                raise ValueError(f"Invalid colour for element '{symbol}': {colour}.")

    #Initialise color array/dictionary
    colors = {}
    #Check each atom in the structure to collect elements
    for i, atom in enumerate(atoms):
        #Use user-defined colors (highest priority)
        if element_colors is not None and atom.symbol in element_colors:
            colors[i] = element_colors[atom.symbol]
        #Fallback to Jmol defaults if necessary
        else:
            colors[i] = jmol_colors[atomic_numbers[atom.symbol]]

    #print(colors) #Print color list if desired

    return colors

# Prepare a visual copy of a structure using the reference substrate representation.
def prepare_visual_structure(atoms, reference_atoms, reference_symbols):

    # Validate reference symbols
    if isinstance(reference_symbols, str) or not reference_symbols: #This check ensures that the string is located within the tuple/array
        raise ValueError("Reference symbols must contain at least one element symbol.")

    for symbol in reference_symbols:
        if symbol not in chemical_symbols[1:]:
            raise ValueError(f"Invalid reference chemical element symbol: '{symbol}'.")

    # Identify reference atoms in both structures
    current_symbols = atoms.get_chemical_symbols()
    reference_structure_symbols = reference_atoms.get_chemical_symbols()

    # Identify atoms belonging to the reference substrate in both structures.
    current_indices = {symbol: [i for i, atom_symbol in enumerate(atoms.get_chemical_symbols()) if atom_symbol == symbol] for symbol in reference_symbols}
    reference_indices = {symbol: [i for i, atom_symbol in enumerate(reference_atoms.get_chemical_symbols()) if atom_symbol == symbol] for symbol in reference_symbols}

    # No matching reference atoms in the input structure.
    if not any(current_indices.values()):
        print(f"Warning: No atoms matching {reference_symbols} found. Plotting original structure without reference.")
        return atoms.copy()

    # Check reference compatibility.
    check_reference_structure(atoms, reference_atoms, reference_symbols)
    visual_reference = reference_atoms.copy()

    #Get fractional coordinates inside the unit cell.
    current_scaled = atoms.get_scaled_positions(wrap=False)
    reference_scaled = reference_atoms.get_scaled_positions(wrap=True)

    cell = atoms.get_cell()

    # Find one common periodic translation for the whole structure.
    best_shift = np.zeros(3)
    best_distance = np.inf   

    for x_shift in (-1, 0, 1):

        for y_shift in (-1, 0, 1):

            total_distance = 0.0

            for symbol in reference_symbols:

                for reference_index, current_index in zip(
                    reference_indices[symbol],
                    current_indices[symbol]):

                    # Current atom with a common periodic translation.
                    candidate = current_scaled[current_index].copy()
                    candidate[0] += x_shift
                    candidate[1] += y_shift

                    # Difference from the corresponding reference atom.
                    difference = candidate - reference_scaled[reference_index]

                    # Convert to Cartesian distance.
                    distance = np.linalg.norm(difference @ cell)

                    total_distance += distance**2

            # Keep the common translation giving the smallest total distance for all reference atoms.
            if total_distance < best_distance:
                best_distance = total_distance
                best_shift = np.array([x_shift, y_shift, 0.0])

    # Apply the selected periodic translation to the reference substrate.
    reference_scaled += best_shift
    visual_reference.set_cell(cell)
    visual_reference.set_scaled_positions(reference_scaled)

    # Collect only the atoms that are NOT part of the reference substrate.
    non_reference_indices = [i for i, symbol in enumerate(atoms.get_chemical_symbols()) if symbol not in reference_symbols]

    visual_adsorbates = atoms[non_reference_indices]

    # Combine reference substrate with the non-reference atoms.
    visual_atoms = visual_reference + visual_adsorbates

    return visual_atoms

#Plot top and side views
def plot_surface_views(atoms,output_filename,figsize=(12, 6),dpi=300,title_size=24,font_size=24,font_family="Times New Roman",
                       font_weight="bold",element_colors=None,top_title="Top View",side_title="Side View"):

    #Atomic colors
    atom_colors = get_atom_colors(atoms,element_colors=element_colors)

    #Plotting parameters
    plt.rcParams.update({"font.size": font_size,"font.family": font_family,"font.weight": font_weight})

    #Subplots
    fig, axes = plt.subplots(1,2,figsize=figsize)

    #Top view
    plot_atoms(atoms,ax=axes[0],rotation="0x,0y,0z",show_unit_cell=0,colors=atom_colors)
    #Titles
    axes[0].set_title(top_title,fontsize=title_size,fontweight=font_weight)
    axes[0].set_axis_off()

    #Side view
    plot_atoms(atoms,ax=axes[1],rotation="270x,0y,0z",show_unit_cell=0,colors=atom_colors)
    #Titles
    axes[1].set_title(side_title,fontsize=title_size,fontweight=font_weight)
    axes[1].set_axis_off()

    #Layout
    plt.tight_layout()

    #Directory
    output_directory = os.path.dirname(output_filename)

    if output_directory:
        os.makedirs(output_directory,exist_ok=True)

    #Saving a figure
    fig.savefig(output_filename,dpi=dpi,bbox_inches="tight")

    print(f"Saved: {output_filename}\n")

    # Close figure
    plt.close(fig)