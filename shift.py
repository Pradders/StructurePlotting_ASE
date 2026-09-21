import os #System
import numpy as np #Numerical analysis
import matplotlib.pyplot as plt #Plotting
#ASE environment
from ase.io import write
from ase.data import atomic_numbers, covalent_radii

from inputs import get_int #import external functions

#Global variables
_current_shift = None

#Find the highest radius to perform the shift
def max_radius(atoms):
    symbols = atoms.get_chemical_symbols() #collect the elemental symbols

    radii = [covalent_radii[atomic_numbers[s]] for s in symbols] #Collect the radii
    diameter = 2*max(radii) #Calculate the diameter

    return diameter

#Create a temporary preview of the structure. The temporary image is deleted after inspection.
def view_cleanup(atoms,filename="temp_view.png",pause=True):
    # Write temporary image
    write(filename,atoms,format="png",rotation="0x,0y,0z",show_unit_cell=1)

    # Read and display image
    img = plt.imread(filename)
    fig = plt.figure()
    plt.imshow(img)
    plt.axis("off")
    plt.show(block=False)

    # Allow manual inspection
    if pause:
        input("Press Enter to close the figure...")

    # Close figure
    plt.close(fig)

    # Remove temporary file
    try:
        os.remove(filename)
    except OSError:
        pass

#Manual shift based on multiples of the diameter corresponding to the maximum covalent radius
def build_shift(atoms, get_int):
    #Start as a vector of zeroes
    shift = np.zeros(3)

    # Maximum atomic diameter
    d = max_radius(atoms)

    # Preview
    print("\nPreviewing structure.")
    view_cleanup(atoms)

    print(f"\nManual shift using max_radius = f{d:.3f} Å")

    # User-defined shifts
    nx = get_int("Shift in x (multiples of diameter, negative = left, positive = right): ")
    ny = get_int("Shift in y (multiples of diameter, negative = down, positive = up): ")
    # Convert multiples into Cartesian shift
    shift[0] = nx * d
    shift[1] = ny * d

    return shift

#Apply a translation to an atomic structure. The original structure is not modified.
def apply_shift(atoms, shift):
    atoms_translate = atoms.copy()
    atoms_translate.translate(shift)
    atoms_translate.wrap()
    return atoms_translate

def get_structure_shift(atoms,mode,system_shift=None):

    global _current_shift

    #Universal shift
    if mode == 1:

        if _current_shift is None:
            _current_shift = build_shift(atoms,get_int)

        return _current_shift

    #Manual shift
    elif mode == 2:

        return build_shift(atoms,get_int)

    #Same shift across each system
    elif mode == 3:

        return np.zeros(3)

    return np.zeros(3)