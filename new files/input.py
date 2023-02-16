from static_objects import shapes
import numpy as np

<<<<<<< HEAD
def get_foil_information():
    d_list = ['D','d','D-shaped','d-shaped']
    s_list = ['symm','Symm']
    h_list = ['Donut','donut','doughnut','Doughnut','ring','Ring']
    foil = {
            "foil_quantity": 10, #how many foils will be used in the simulation
            "foil_shape": 'd-shape', #which foil will be created
            "target-file": "path_of_file", 
            "length": 3.4, #main tube length in cm
            "temp": 2300, #temperature
            "foil-height": 0.525, #height of foil from origin
            "thickness": 25, #foil thickness in micron
            "foil-rotation": 0, #rotation of foils
            "ionizer": 5.956, #ionizer length
            "mass": 8, 
            "gradient": None, #temperature gradient used for ionizer
            "NMax": 1000,
            "sep": 0,
            "hsep": 0,
            "squish": 1
=======


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
>>>>>>> 2c11a42d2856e52d3bfbb72629e6df4069043866
            # etc: 'etc'
        }
    ###This container should contain all variable information (Maybe static information as well, easier to generate here?) of a foil.
    ### we will use this function data to create the foils by calling it in main, and sending it to static_objects.py
<<<<<<< HEAD
    foil_shape = input("Which shape would you like to create the input file for? ")
    if foil_shape in d_list or s_list or h_list:
        foil['foil_shape'] = foil_shape

    foil['target-file'] = input("Please enter the file path for the target file: ")

    foil_quanity = input("How many foils would like to make? default is 10: ")
    if foil_quanity:
        foil['foil_quantity'] = int(foil_quanity)

    target = foil['target-file'].split('/')
    if len(target[-1]) > 20:
        return
    return foil

def get_anything_else():
    ### Do we need anything else?
    ### Since some dictionary values and keys aren't always used
    ### Add it when it is needed, main focus is d-shape and pizza/symm
    foil = get_foil_information()
    # print(foil)
    d_list = ['D','d','D-shaped','d-shaped']
    s_list = ['symm','Symm']
    h_list = ['Donut','donut','doughnut','Doughnut','ring','Ring']
    c_list = ['coil','Coil','cylinder','Cylinder','tube','Tube']
    if foil['foil_shape'] not in d_list:
        if foil['foil_shape'] in h_list:
=======



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
>>>>>>> 2c11a42d2856e52d3bfbb72629e6df4069043866
            foil["r1"] = 0.9144 #exterior radius
            foil["r2"] = 0.3644 #interior radius
            foil["th"] = np.pi/4 #angle of cut line
            foil["m"] = 1 #slope of line for the cutout
            pass
<<<<<<< HEAD
        elif foil['foil_shape'] in s_list:
            foil["th"] = np.pi/4 #angle of cut line
            foil["m"] = 1 #slope of line for the cutout
            pass
        elif foil['foil_shape'] == "cern":
            #in case there are ever the need for adjustment of the foil
            #feel free to add stuff in here if cern ever changes their foil
            pass
        elif foil['foil_shape'] in c_list:
            #any measurements/factors unique to cylindrical foil can be added in here
=======
        elif foil.shape in shapes.s_list:
            foil["th"] = np.pi/4 #angle of cut line
            foil["m"] = 1 #slope of line for the cutout
            pass
        elif foil.shape == "cern":
>>>>>>> 2c11a42d2856e52d3bfbb72629e6df4069043866
            pass

        # adjust the dictionary according to the shape that is selected, may need to
        # add or remove key/value from dictionary as some won't be used

    ## if statements to check foil shape under here probably

    return foil

<<<<<<< HEAD
=======


>>>>>>> 2c11a42d2856e52d3bfbb72629e6df4069043866
# if __name__ == '__main__':
#     main()