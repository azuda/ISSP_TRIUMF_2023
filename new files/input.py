def get_foil_information()
    foil = 
    {
        foil_quantity : 0
        foil_shape : 'd-shape'
        etc : 'etc'
    }
    ###This container should contain all variable information (Maybe static information as well, easier to generate here?) of a foil.
    ### we will use this function data to create the foils by calling it in main, and sending it to static_objects.py
    foil.foil_quantity = input("How many foils would like to make? default is 0: ")
    return foil

def get_anything_else()
    ### Do we need anything else?
    pass




if __name__ == '__main__':
    main()