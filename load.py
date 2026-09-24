import os #System
from collections import Counter #Counting function
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

#Check that the reference structure contains the requested elements and that the number of reference atoms matches the NEB structure.
def check_reference_structure(atoms, reference_atoms, reference_symbols):

    #Check that reference symbols were provided.
    if not reference_symbols:
        raise ValueError("Reference_symbols must contain at least one element symbol.")

    #Check that every requested reference element exists in the reference structure.
    reference_counts = Counter(reference_atoms.get_chemical_symbols())

    for symbol in reference_symbols:

        if reference_counts[symbol] == 0: #Should contain at least one symbol
            raise ValueError(f"Reference structure does not contain the requested element '{symbol}'.")

    #Check that the NEB structure contains the same number of reference atoms as the supplied reference structure.
    atoms_counts = Counter(atoms.get_chemical_symbols())

    for symbol in reference_symbols: #Provide data about the missing elements
        if atoms_counts[symbol] != reference_counts[symbol]:
            raise ValueError(
                f"Reference mismatch for '{symbol}': "
                f"reference contains {reference_counts[symbol]} atoms, "
                f"but the NEB structure contains {atoms_counts[symbol]}.")

#Find and load a reference structure. CONTCAR is preferred over POSCAR, but either valid file is usable.
def get_reference_structure(folder,repeat=(1,1,1)):

    for filename in ("CONTCAR", "POSCAR"): #Reads CONTCAR first before POSCAR
        path = os.path.join(folder, filename)
        if os.path.isfile(path):
            try:
                return load_atoms(path,repeat)
            except Exception:
                print(f"Could not load reference structure: {path}")

    #Return None if neither structure could be loaded.
    return None