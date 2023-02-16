from static_objects import shapes
import numpy as np



def get_foil_options():
    foil = {
            "quantity": 10,
            "shape": 'd-shape',
            "filename": "path/to/file",
            "temp": 2300,
            "height": 0.525,
            "thickness": 25,
            "rotation": 0,
            "ionizer": 5.956
            # etc: 'etc'
        }
    ###This container should contain all variable information (Maybe static information as well, easier to generate here?) of a foil.
    ### we will use this function data to create the foils by calling it in main, and sending it to static_objects.py



    foil.quantity = input("Enter number of foils to use: (default 10)")
    return foil


def get_anything_else(foil):
    ### Do we need anything else?
    ### Since some dictionary values and keys aren't always used
    ### Add it when it is needed, main focus is d-shape and pizza/symm

    if foil.shape not in shapes.d_list:
        if foil.shape in shapes.h_list:
            pass
        elif foil.shape == "horseshoe":
            foil["r1"] = 0.9144 #exterior radius
            foil["r2"] = 0.3644 #interior radius
            foil["th"] = np.pi/4 #angle of cut line
            foil["m"] = 1 #slope of line for the cutout
            pass
        elif foil.shape in shapes.s_list:
            foil["th"] = np.pi/4 #angle of cut line
            foil["m"] = 1 #slope of line for the cutout
            pass
        elif foil.shape == "cern":
            pass

        # adjust the dictionary according to the shape that is selected, may need to
        # add or remove key/value from dictionary as some won't be used

    ## if statements to check foil shape under here probably

    return foil



# if __name__ == '__main__':
#     main()