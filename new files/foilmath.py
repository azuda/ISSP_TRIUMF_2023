<<<<<<< HEAD
import input as ip
import numpy as np
=======
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
>>>>>>> 2b652ffc6af47e436c3f118bf6360642e9846288
from static_objects import shapes

def foil_math(foil):
    ''''''
    #in microns
    foilThickness = foil['thickness']/10000
    #placeholder this will change accordingly
    foilAmount = foil['quantity'] # + 1
    #target chamber itself is 3.4cm 
    containerLength = foil['length']
    foilSpace = foilThickness*foilAmount
    gap = (containerLength - foilSpace)/foilAmount
    return gap, foilAmount
    ### In here we are going to do the foil math, based on thickness relative to the container we will determine the size of the gaps
    #gap equals number of foils times 0.0025, take that subtract from container length
    #divide remaining space by number of foils to get how much the gap needs to be
    #so that the space is even between all foils
    
#ideally i think we should have all these variables outside of each if/elif be its own thing so we can split
#each functions for its own shape respectively instead of one large function
def foil_surface_output():
    '''Create and add the surfaces to display on the RIBO input file'''

<<<<<<< HEAD
    foil = ip.get_anything_else()

    foilThickness = foil['thickness']/10000 # Get foil thickness in cm
=======
    foilThickness = foil['thickness'] / 10000 # Get foil thickness in cm
>>>>>>> 2b652ffc6af47e436c3f118bf6360642e9846288
    temperature = foil['temp'] # Get the temperature in kelvins (K)
    
    # rc is temporary until i figure out how to calculate number
    rc = 1

    startContainer = -foil['length'] / 2 # Get the z coodrinate of the start of the container
    endContainer = foil['length'] / 2 # Get the z coordinate of the end of the container

    surfaces = []
    gap, foilAmount = foil_math(foil) # Get the gap and foil amount from foil_math

    currentPosition = startContainer + foilThickness # Set the current position to the start of the container plus the gap

    f_or_g = 1 # This determines if the next surface is a foil or a gap, 0 is foil, 1 is gap


    # The container st
    if foil['shape'] in shapes["d_list"]:
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
            return surfaces
    elif foil['shape'] in shapes["s_list"]:
        #this is all the stuff we need to calculate the two cuts we need for pizza
        #left and right indicates there the line is, left is the cut where it is left of the foil, whereas right is the right of the foil
        #refer to sketches/pizza-cells.jpeg
        b = foil['r1']*np.cos(foil['th']) - foil['r1']*np.sin(foil['th'])*abs(foil['m'])
        a1 = np.arctan(1/abs(foil['m']))  #current angles
        a2 = np.arctan(1/(-abs(foil['m'])))
        
        xx1 = np.sin(a1+foil['rotation'])    #rotated angles
        xx2 = np.sin(a2+foil['rotation'])   
        yy1 = np.cos(a1+foil['rotation'])
        yy2 = np.cos(a2+foil['rotation'])               
        p1 = b/np.sqrt(1+foil['m']**2)
        p2 = -b/np.sqrt(1+foil['m']**2)  #from ±b/sqrt(c_x**2 + c_y**2)

        left  = [7, rc, temperature,0,0,0,0,0,0,xx1,-yy1,0,p1,'',''] 
        right = [8, rc ,temperature,0,0,0,0,0,0,xx2,-yy2,0,p2,'','']

<<<<<<< HEAD
        surfaces.append(left)
        surfaces.append(right)
        for x in range(9, foilAmount * 2 + 9): # While the current position is less than the end of the container
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

    
# if __name__ == "__main__":
#     # main()
#     table = None # Testing
#     foil_surface_output()
=======
if __name__ == "__main__":
    # main()
    table = None # Testing
    foil_surface_output(foil, table)
>>>>>>> 2b652ffc6af47e436c3f118bf6360642e9846288
