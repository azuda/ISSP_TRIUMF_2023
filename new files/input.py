from static_objects import shapes
import numpy as np
import argparse



def get_foil_options():
    """Function to get all foil options from user input using argparse

    Returns:
        dict: options for foil and related args
    """

    # get all options from user input
    parser = argparse.ArgumentParser(description="foil options")
    parser.add_argument("--shape", type=str, default="d-shaped", help="foil shape")
    parser.add_argument("--quantity", type=int, default=10, help="number of foils")
    parser.add_argument("--filename", type=str, default="./test.txt", help="path to output file")
    parser.add_argument("--temp", type=int, default=2300, help="temperature in Kelvin")
    parser.add_argument("--height", type=float, default=0.525, help="height of foil in cm")
    parser.add_argument("--thickness", type=float, default=25, help="thickness of foil in microns")
    parser.add_argument("--rotation", type=float, default=0, help="rotation of foil in degrees")
    parser.add_argument("--ionizer", type=float, default=5.956, help="length of ionizer in cm")
    # add more args as needed

    # parse args and return as a dict
    args = parser.parse_args()
    return vars(args)


def get_anything_else(foil):
    ### Do we need anything else?
    ### Since some dictionary values and keys aren't always used
    ### Add it when it is needed, main focus is d-shape and pizza/symm

    if foil.shape not in shapes.d_list:
        if foil.shape in shapes.h_list:
            pass

        elif foil.shape == "horseshoe":
            foil["r1"] = 0.9144     # exterior radius for horseshoe / cylinder
            foil["r2"] = 0.3644     # interior radius for horseshoe / cylinder
            foil["th"] = np.pi/4    # angle of cut line for horseshoe / symm
            foil["m"] = 1           # slope of cut line for horseshoe / symm

        elif foil.shape in shapes.s_list: # this can be cleaned up
            foil["th"] = np.pi/4
            foil["m"] = 1
            
        elif foil.shape == "cern":
            pass

        # adjust the dictionary according to the shape that is selected, may need to
        # add or remove key/value from dictionary as some won't be used

    ## if statements to check foil shape under here probably

    return foil



# if __name__ == '__main__':
#     main()