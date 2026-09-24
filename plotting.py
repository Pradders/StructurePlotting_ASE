import os #System
import matplotlib.pyplot as plt #Plotting
import numpy as np #Numerical analysis

#ASE environment
from ase.visualize.plot import plot_atoms
from ase.data.colors import jmol_colors
from ase.data import atomic_numbers

def get_atom_colors(atoms,element_colors=None):

    colors = {}

    for i, atom in enumerate(atoms):

        # User-defined colour
        if (element_colors is not None and atom.symbol in element_colors):

            colors[i] = element_colors[atom.symbol]

        # Jmol default
        else:
            colors[i] = jmol_colors[atomic_numbers[atom.symbol]]

    return colors

#Prepare a visual copy of an NEB image so that the selected reference atoms use the same periodic representation as the reference structure.
def prepare_visual_structure(atoms, reference_atoms, reference_symbols):

    visual_reference = reference_atoms.copy()

    #Get fractional coordinates inside the unit cell.
    current_scaled = atoms.get_scaled_positions(wrap=False)
    reference_scaled = reference_atoms.get_scaled_positions(wrap=True)

    cell = atoms.get_cell()

    #Keep track of the occurrence number of each element.
    #This allows the reference structure to contain more than
    #one type of substrate atom.
    reference_indices = {}
    current_indices = {}

    for symbol in reference_symbols:

        reference_indices[symbol] = [
            i for i, atom_symbol
            in enumerate(reference_atoms.get_chemical_symbols())
            if atom_symbol == symbol]

        current_indices[symbol] = [
            i for i, atom_symbol
            in enumerate(atoms.get_chemical_symbols())
            if atom_symbol == symbol]

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

            # Keep the common translation giving the smallest
            # total distance for all reference atoms.
            if total_distance < best_distance:

                best_distance = total_distance
                best_shift = np.array([x_shift, y_shift, 0.0])


    # Apply the SAME periodic translation to the entire structure.
    reference_scaled += best_shift
    visual_reference.set_cell(cell)
    visual_reference.set_scaled_positions(reference_scaled)

    # Collect only the atoms that are NOT part of the reference substrate.
    non_reference_indices = [
        i for i, symbol in enumerate(atoms.get_chemical_symbols())
        if symbol not in reference_symbols]

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

    print(f"Saved: {output_filename}")

    # Close figure
    plt.close(fig)