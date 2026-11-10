#User inputs

import os #Operating system

#Global variables
_current_mode = None

#Collect an integer where possible
def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter an integer.")

#Used to accept a result
def confirm(prompt="Accept this result/outcome?"):
    while True:
        ans = input(f"{prompt} (y/n): ").strip().lower()
        if ans in ("y", "n"):
            return ans == "y"
        print("Please enter 'y' or 'n'.")

#Select how the shift will happen
def choose_shift_mode():
    """
    Modes:

        1: Same shift for ALL images in ALL systems
        2: Manual shift for EACH image
        3: No shift
    """

    global _current_mode

    if _current_mode is not None:
        return _current_mode

    while True:

        print("\nSelect shift mode:")
        print("1: SAME shift for ALL structures")
        print("2: MANUAL shift for EACH structure")
        print("3: NO shift")

        mode = get_int("Enter mode (1/2/3): ")

        if mode not in (1, 2, 3):
            print("Invalid selection. Enter 1, 2, or 3.\n")
            continue

        if confirm():
            _current_mode = mode
            return mode

        print("Invalid selection. Please try again.\n")

#Check if there is a reference folder and if the user wants to apply a reference structure
def get_reference_settings(reference_symbols, reference_folder="Reference"):
    while True: #If the conditions are not met, then restart the loop
        reference_mode = get_int(
            "Select reference mode:\n"
            "1: No reference\n"
            "2: Use external reference folder\n"
            "Enter 1 or 2: "
        )

        if reference_mode not in (1, 2):
            print("Invalid selection. Enter 1 or 2.")
            continue

        if reference_mode == 1: #No reference structure to be applied
            if confirm():
                return None, None

        elif reference_mode == 2: #Use the surface specified in a reference folder
            if reference_symbols is None or not reference_symbols:
                print("Reference symbols must be specified for mode 2.")
                continue

            if not reference_folder or not os.path.isdir(reference_folder): #Check that the folder exists in the first place, or otherwise the loop restarts
                print(f"Reference folder not found: {reference_folder}.")
                continue

            if confirm():
                return reference_folder, reference_symbols

        else:
            print("Invalid selection. Enter 1 or 2.")