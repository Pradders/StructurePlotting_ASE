import os #System
import matplotlib.pyplot as plt #Plotting

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