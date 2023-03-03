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
            # etc: 'etc'
        }

def foil_math(foil):
    ''''''
    #in microns
    foilThickness = foil['thickness']/10000
    #placeholder this will change accordingly
    foilAmount = foil['foil_quantity'] # + 1
    #target chamber itself is 3.4cm 
    containerLength = foil['length']
    foilSpace = foilThickness*foilAmount
    gap = (containerLength - foilSpace)/foilAmount
    return gap, foilAmount
    ### In here we are going to do the foil math, based on thickness relative to the container we will determine the size of the gaps
    #gap equals number of foils times 0.0025, take that subtract from container length
    #divide remaining space by number of foils to get how much the gap needs to be
    #so that the space is even between all foils
    

def foil_surface_output():
    '''Create and add the surfaces to display on the RIBO input file'''

    foilThickness = foil['thickness']/10000 # Get foil thickness in cm
    temperature = foil['temp'] # Get the temperature in kelvins (K)
    
    # rc is temporary until i figure out how to calculate number
    rc = 1

    startContainer = -foil['length'] / 2 # Get the z coodrinate of the start of the container
    endContainer = foil['length'] / 2 # Get the z coordinate of the end of the container

    surfaces = []
    gap, foilAmount = foil_math(foil) # Get the gap and foil amount from foil_math

    currentPosition = startContainer + foilThickness # Set the current position to the start of the container plus the gap

    f_or_g = 0 # This determines if the next surface is a foil or a gap, 0 is foil, 1 is gap


    # The container st

    for x in range(8, foilAmount * 2 + 8): # While the current position is less than the end of the container
        # Create the foil surface
        line = [x, rc , temperature,
                    0,0,0, #x**2,y**2,z**2
                    0,0,0, #xy,xz,yz
                    0,1,0, #x,y,z
                    currentPosition, #C
                    '','']   #extra tabs (format seems important)
        surfaces.append(line)
        # print(line)
        if f_or_g == 0:
            currentPosition += foilThickness # Add the foil thickness to the current position
            f_or_g = 1
        else:
            currentPosition += gap # Add the foil gap to the current position
            f_or_g = 0
    print(surfaces)
    return surfaces
        

        

    
    


if __name__ == "__main__":
    # main()
    table = None # Testing
    foil_surface_output(foil, table)
