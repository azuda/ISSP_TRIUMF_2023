import inputs as ip
import numpy as np
from static_objects import shapes, format_title

def foil_math(foil):
    '''
    Calculate the gap between foils and the number of foils using the foil thickness and the container length
    '''

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


def foil_surface_output(foil):
    '''Create and add the surfaces to display on the RIBO input file'''

    foilThickness = foil['thickness'] / 10000 # Get foil thickness in cm
    temperature = foil['temp'] # Get the temperature in kelvins (K)

    rc = 1 # Roughness Coefficient

    startContainer = -foil['length'] / 2 # Get the z coodrinate of the start of the container
    endContainer = foil['length'] / 2 # Get the z coordinate of the end of the container

    surfaces = []

    # The foil surfaces start at 8 and go up from there because the first 7 are the container surfaces
    # The foil surfaces are added to the surfaces list. Only the surface above the foils and both end caps are added
    if foil['shape'] in shapes["d_list"]:
        surfaces.append([8, rc , temperature, # This is the surface above the foils
                        0,0,0, #x**2,y**2,z**2
                        0,0,0, #xy,xz,yz
                        1,0,0, #x,y,z
                        foil['height'], #C 
                        '',''])   #extra tabs 

        surfaces.append([9, rc , temperature,   # End cap
                        0,0,0, #x**2,y**2,z**2
                        0,0,0, #xy,xz,yz
                        0,0,1, #x,y,z
                        startContainer, #C
                        '',''])   #extra tabs (format seems important))
        surfaces.append([10, rc , temperature, # End cap
                        0,0,0, #x**2,y**2,z**2
                        0,0,0, #xy,xz,yz
                        0,0,1, #x,y,z
                        endContainer, #C
                        '',''])   #extra tabs
        row_number = 11  

    elif foil['shape'] in shapes["s_list"]:
        b = foil['r1']*np.cos(foil['th']) - foil['r1']*np.sin(foil['th'])*abs(foil['m'])
        a1 = np.arctan(1/abs(foil['m']))  #current angles
        a2 = np.arctan(1/(-abs(foil['m'])))
        xx1 = np.sin(a1+foil['rotation'])    #rotated angles
        xx2 = np.sin(a2+foil['rotation'])   
        yy1 = np.cos(a1+foil['rotation'])
        yy2 = np.cos(a2+foil['rotation'])               
        p1 = b/np.sqrt(1+foil['m']**2)
        p2 = -b/np.sqrt(1+foil['m']**2) 
        left  = [8, 1, temperature,0,0,0,0,0,0,xx1,-yy1,0,p1,'',''] 
        right = [9, 1, temperature,0,0,0,0,0,0,xx2,-yy2,0,p2,'','']
        surfaces.append(left)
        surfaces.append(right)


        surfaces.append([10, rc , temperature,   # End cap
                        0,0,0, #x**2,y**2,z**2
                        0,0,0, #xy,xz,yz
                        0,0,1, #x,y,z
                        startContainer, #C
                        '',''])   #extra tabs (format seems important))
        surfaces.append([11, rc , temperature, # End cap
                            0,0,0, #x**2,y**2,z**2
                            0,0,0, #xy,xz,yz
                            0,0,1, #x,y,z
                            endContainer, #C
                            '',''])   #extra tabs (format seems important))
        row_number = 12
    

    gap, foilAmount = foil_math(foil) # Get the gap and foil amount from foil_math

    currentPosition = startContainer + foilThickness # Set the current position to the start of the container plus the gap

    f_or_g = 1 # This determines if the next surface is a foil or a gap, 0 is foil, 1 is gap
    # we start with a foil

    # Begin the process of adding the foils and gaps to the surfaces list
    # The amount of foils added will be determined by the gaps between the foils and the container length
    #       - the gaps between the foils will be determined by the foil thickness and the foil amount
    while round(currentPosition, 9) < endContainer: # While the current position is less than the end of the container
        
        # Create the foil surface
        line = [row_number, rc , temperature,
                    0,0,0, #x**2,y**2,z**2
                    0,0,0, #xy,xz,yz
                    0,0,1, #x,y,z
                    currentPosition, #C
                    '','']   #extra tabs (format seems important)
        surfaces.append(line)
        
        if f_or_g == 0:
            currentPosition += foilThickness # Add the foil thickness to the current position
            f_or_g = 1 # Set the next surface to be a gap
        else:
            currentPosition += gap # Add the foil gap to the current position
            f_or_g = 0 # Set the next surface to be a foil
        
        row_number += 1
    return surfaces

def cell_gaps(foil, row=5, s1=-1, s2 =13, s3=-14, s4=-8, s5=0):
    """This function will generate the cell gaps for the foil shape starting with the second foil, the first foil is produced in the cells_foil_shape function
    to be able to acurately generate the gaps we needed to generate the first foil in the cells_foil_shape function in the for loop it is foil_quantity-1 because
        the first foil is generated in the cells_foil_shape function"""
    if foil['shape'] in shapes["d_list"]:
        cell = {
            'row' : row,
            's1' : s1,
            's2' : s2,
            's3' : s3,
            's4' : s4,
            's5' : s5
        }
        first_row = [row, s1, s2, s3, s4, s5]
        cell_gaps = [format_title(first_row)]



        for gap in range(1, foil['quantity'] - 2):
            cell['row'] += 1
            cell['s2'] += 2
            cell['s3'] -= 2

            cell_gaps.append(format_title([cell['row'], cell['s1'], cell['s2'], cell['s3'], cell['s4'], cell['s5']]))

        last_row = [cell['row']+1, cell['s1'], cell['s2']+2, -10, cell['s4'], cell['s5']]
        cell_gaps.append(format_title(last_row))
        
    elif foil['shape'] in shapes["s_list"]:
        cell = {
            'row' : 3,
            's1' : -1,
            's2' : 12,
            's3' : -13,
            's4' : 8,
            's5' : 11
        }
        first_row = [3, -1, 10, -11, -8, 11]
        cell_gaps = [format_title(first_row)]

        last = 0 
        for x in range(4, foil['quantity'] * 3 + 1): # - 2
            last = x
            if x % 3 == 1:
                cell_gaps.append(format_title([x, cell['s1'], cell['s2'], cell['s3'], cell['s4'], -cell['s5']]))
            elif x % 3 == 2:
                cell_gaps.append(format_title([x, cell['s1'], cell['s2'], cell['s3'], cell['s4'], cell['s5']]))
            elif x % 3 == 0:
                cell_gaps.append(format_title([x, cell['s1'], cell['s2'], cell['s3'], -cell['s4'], -cell['s5']]))
                cell['s2'] += 2
                cell['s3'] -= 2

        last_row = [
                    [last + 1, cell['s1'], cell['s2'], -11, cell['s4'], -cell['s5']],
                    [last + 2, cell['s1'], cell['s2'], -11, cell['s4'], cell['s5']],
                    [last + 3, cell['s1'], cell['s2'], -11, -cell['s4'], -cell['s5']]
                ]
        cell_gaps += [format_title(x) for x in last_row]

    return cell_gaps

