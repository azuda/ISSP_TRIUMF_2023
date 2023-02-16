import numpy as np
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
    return foil
    pass


if __name__ == '__main__':
    main()
