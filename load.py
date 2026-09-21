import os #System
from ase.io import read #ASE environment

def find_structure(folder):
    #Locate CONTCAR first and then POSCAR otherwise
    contcar = os.path.join(folder, "CONTCAR")
    poscar = os.path.join(folder, "POSCAR")

    #Return the file location as a string
    if os.path.isfile(contcar):
        return contcar
    elif os.path.isfile(poscar):
        return poscar
    else:
        return None

#Load atoms from CONTCAR/POSCAR
def load_atoms(structure_file, repeat=(1, 1, 1)):

    if structure_file is None:
        return None

    print(f"Reading: {structure_file}")
    atoms = read(structure_file) #Collect the atomic data

    if repeat != (1, 1, 1):
        atoms = atoms.repeat(repeat) #Multiply by a certain number of dimensions

    return atoms