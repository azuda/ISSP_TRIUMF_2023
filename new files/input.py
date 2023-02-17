from static_objects import shapes
import numpy as np
<<<<<<< HEAD
from main import main


def get_foil_information():
    foil = {
        "foil_quantity": 10,
        "foil_shape": 'd-shape',
        "target-file": "filelocation",
        "temp": 2300,
        "foil-height": 0.525,
        "thickness": 25,
        "foil-rotation": 0,
        "ionizer": 5.956
        # etc: 'etc'
    }
    # This container should contain all variable information (Maybe static information as well, easier to generate here?) of a foil.
    # we will use this function data to create the foils by calling it in main, and sending it to static_objects.py
    foil.foil_quantity = input(
        "How many foils would like to make? default is 10: ")
    return foil


def get_anything_else(foil):
    # Do we need anything else?
    # Since some dictionary values and keys aren't always used
    # Add it when it is needed, main focus is d-shape and pizza/symm
    if foil.foil_shape != "d-shape":
        if foil.foil_shape == "donut":
            pass
        elif foil.foil_shape == "horseshoe":
            foil["r1"] = 0.9144  # exterior radius
            foil["r2"] = 0.3644  # interior radius
            foil["th"] = np.pi/4  # angle of cut line
            foil["m"] = 1  # slope of line for the cutout
            pass
        elif foil.foil_shape == "symm":
            foil["th"] = np.pi/4  # angle of cut line
            foil["m"] = 1  # slope of line for the cutout
            pass
        elif foil.foil_shape == "cern":
            pass
        # adjust the dictionary according to the shape that is selected, may need to
        # add or remove key/value from dictionary as some won't be used
    # if statements to check foil shape under here probably
=======
import argparse



def get_foil_options():
    """Gets all foil options from user input using argparse

    Returns:
        dict: options for foil and related args
    """

    # get all options from user input
    parser = argparse.ArgumentParser(description="foil options")
    parser.add_argument("--quantity", type=int, default=10, help="number of foils")
    parser.add_argument("--shape", type=str, default="d-shaped", help="foil shape")
    parser.add_argument("--filename", type=str, default="./test.txt", help="path to output file")
    parser.add_argument("--length", type=float, default=3.4, help="target length in cm")
    parser.add_argument("--temp", type=int, default=2300, help="temperature in Kelvin")
    parser.add_argument("--height", type=float, default=0.525, help="height of foil from origin in cm")
    parser.add_argument("--thickness", type=float, default=25, help="foil thickness in microns")
    parser.add_argument("--rotation", type=float, default=0, help="foils rotation in degrees")
    parser.add_argument("--ionizer", type=float, default=5.956, help="ionizer length in cm")
    parser.add_argument("--mass", type=int, default=8, help="mass of ion")
    parser.add_argument("--gradient", type=float, default=None, help="temperature gradient for ionizer")
    parser.add_argument("--nmax", type=int, default=1000, help="number of histories for Source card")
    parser.add_argument("--sep", type=float, default=0, help="length of region between cylinders in cm")
    parser.add_argument("--hsep", type=float, default=0, help="length of region for horseshoe / donut")
    parser.add_argument("--squish", type=float, default=1, help="percent of target length to house foils")

    # parse args and insert into dict
    args = parser.parse_args()
    foil = vars(args)

    return foil


def get_anything_else():
    """Modify the dictionary returned by get_foil_options() to add or remove keys + values as needed

    Returns:
        dict: modified dictionary containing foil options and other args
    """

    foil = get_foil_options()

    # if not d-shaped
    if foil["shape"] not in shapes["d_list"]:
        # donut / ring
        if foil["shape"] in shapes["h_list"]:
            foil["r1"] = 0.9144         # exterior radius for horseshoe / cylinder
            foil["r2"] = 0.3644         # interior radius for horseshoe / cylinder
            foil["th"] = np.pi / 4      # angle of cut line for symm / horseshoe
            foil["m"] = 1               # slope of cut line for symm / horseshoe
        # symm
        elif foil["shape"] in shapes["s_list"]:
            foil["th"] = np.pi / 4
            foil["m"] = 1
        elif foil.shape == "cern":
            pass

    # adjust the dictionary according to the shape that is selected
    # may need to add keys + values as needed
    # remove unnecessary keys + values

    return foil


def validate():
    """Validates args from get_foil_options() and get_anything_else()
    """
    foil = get_anything_else()

    # validate foil shape
    all_shapes = []
    for key in shapes:
        all_shapes.extend(shapes[key])
    if foil["shape"] not in all_shapes:
        raise ValueError("Invalid foil shape")

    # 20 character limit for filename
    target = foil["filename"].split('/')
    if len(target[-1]) > 20:
        raise ValueError("File name must be less than 20 characters")

    # validate target length using quantity + length + squish somehow
    # validate foil geometry using height + thickness + rotation somehow

>>>>>>> main
    return foil


<<<<<<< HEAD
if __name__ == '__main__':
    main()
=======

# print(validate())
>>>>>>> main
