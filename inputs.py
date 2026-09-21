#Global variables
_current_mode = None

#Collect an integer where possible
def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter an integer.")

#Select how the shift will happen
def choose_shift_mode():
    """
    Modes:

        1: Same shift for ALL images in ALL systems
        2: Manual shift for EACH image
        3: Same shift for ALL images in EACH system
        4: No shift
    """

    global _current_mode

    if _current_mode is not None:
        return _current_mode

    while True:

        print("\nSelect shift mode:")

        print("1: SAME shift for ALL structures")
        print("2: MANUAL shift for EACH structure")
        print("3: NO shift to ANY structure")

        mode = get_int("Enter mode (1/2/3): ")

        if mode in [1, 2, 3]:

            confirm_mode = input(f"Confirm mode {mode}? (y/n): ").lower()

            if confirm_mode == "y":
                _current_mode = mode
                return mode

        print("Invalid selection. Please try again.\n")
