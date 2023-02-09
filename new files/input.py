def get_foil_information():
    foil = {
            "foil_quantity": 470,
            "foil_shape": 'd-shape',
            "target-file": "filelocation",
            "temp": 2300,
            "foil-height": 0.525,
            "thickness": 25,
            "foil-rotation": 0,
            "ionizer": 5.956
            # etc: 'etc'
        }
    ###This container should contain all variable information (Maybe static information as well, easier to generate here?) of a foil.
    ### we will use this function data to create the foils by calling it in main, and sending it to static_objects.py
    foil.foil_quantity = input("How many foils would like to make? default is 470: ")
    return foil

def get_anything_else(foil):
    ### Do we need anything else?
    if foil.foil_shape != "d-shape":
        print("foil shape list")
        foil.foil_shape = input("What shape from above would you like to use?")
        # adjust the dictionary according to the shape that is selected, may need to
        # add or remove key/value from dictionary as some won't be used
    ## if statements to check foil shape under here probably
    return foil
    pass




if __name__ == '__main__':
    main()