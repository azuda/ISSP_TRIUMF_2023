import os
import pandas as pd


temp = 2300         # global temperature
mass = 8            # mass (8 for 8Li)
Nmax = 1000         # number of histories for the Source card
ionizer = 5.956     # ionizer?


dic = {"Mass":mass,"T (K)":temp,
           "Source Headers (T)":["type","Mass","T (K)","Alpha","nx","ny","nz",
                                "x","y","z","R","L","sigma","theta","phi"],
            "Tally Headers":["S","Nmax","Tmax","Tpmax"],
            "Nmax":Nmax
        }

shapes = {
        "d_list": ['D','d','D-shaped','d-shaped'],
        "s_list": ['symm','Symm'],
        "h_list": ['Donut','donut','doughnut','Doughnut','ring','Ring'],
        "lc_list": ['C-Long','c-long','c-longitudinal','C-Longitudinal'], #CERN longitudinal
        "lt_list": ['T-Long','t-long','t-longitudinal','T-Longitudinal'], #TRIUMF longitudinal (no u-shaped container?)
        "slab_list": ['D','d','D-shaped','d-shaped','symm','Symm','Donut','donut','doughnut','Doughnut','ring','Ring','C-Long','c-long','c-longitudinal','C-Longitudinal','arc'],
        "weird": ['symm','Symm','Donut','donut','doughnut','Doughnut','ring','Ring'],
        "c_list": ['coil','Coil','cylinder','Cylinder','tube','Tube']
        }


def format_title(items, cols=15):
    return items + (cols - len(items)) * ['']


def target_container():
    '''This was a file supplied the when compared, contained the target container information for the RIBO input file.'''
    ### Why does the original use pandas here?
    file = "\\Create_ribo_file\static\exterior.txt"
    path = os.getcwd()+file
    return pd.read_csv(path, sep='\t',header=0,comment='*')


def top_of_foil_edge():
    '''This appears to be the distance from 0,0 (the center of the foil) to the cut of the d-shaped foil'''
    ### How will this function work with other shaped foils? Is this static content?
    file = "\\Create_ribo_file\static\foilcut.txt"
    path = os.getcwd()+file
    return pd.read_csv(path, sep='\t',header=0,comment='*')


def target_container_endcaps():
    '''This will be the container endcaps'''
    ### Do we need to include the end caps if we are evenly spacing the foils as if the end caps don't exist
    ### Does the RIBO input file need to see the existance of the caps to run the simulation?
    pass


# def foil_edges():
#     '''
#     In this function, we can call a function that will create the foils based on the input parameters when calling the function
#     This function is going to call another function do the math on how many foils to create
#     Then this function will call the foil creation function and return the a long string for the RIBO input file
#     '''
#     ###If shape is _____ do _______
#     math = quantity of foils
#     long_string = ''
#     for line of math
#         create row of long string for foil
#         long_string += line
#     return long_string


def cells_target_container():
    file = "\\new files\cells\ext-cell.txt"
    path = os.getcwd()+file
    return pd.read_csv(path, sep='\t',header=0,comment='*')

def cells_foil_shape(foil_shape):
    """This function creates the first rows of the cell file, the first 2 are static composing the container and the rest are the foils"""
    first_cells = [format_title([1,1,-2,-6,-4,5]), format_title([2,-3,-7,6,0,0])]
    if foil_shape in shapes['d_list']:
        first_cells.append(format_title([3,-1,9,-10,8,0]))
        first_cells.append(format_title([4,-1,9,-11,-8,0]))
        return first_cells
    elif foil_shape == 'pizza_shape':
        return 'not formatted yet' ### we need this information
    else:
        return 'Please enter a valid foil shape'

def cell_gaps(foil_quantity, row=5, s1=-1, s2 =12, s3=-13, s4=-8, s5=0):
    """This function will generate the cell gaps for the foil shape starting with the second foil, the first foil is produced in the cells_foil_shape function
    to be able to acurately generate the gaps we needed to generate the first foil in the cells_foil_shape function in the for loop it is foil_quantity-1 because
    the first foil is generated in the cells_foil_shape function"""
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

    for gap in range(1, foil_quantity-1):
        cell['row'] += 1
        cell['s2'] += 2
        cell['s3'] -= 2
        cell_gaps.append(format_title([cell['row'], cell['s1'], cell['s2'], cell['s3'], cell['s4'], cell['s5']]))
    last_row = [cell['row']+1, cell['s1'], cell['s2']+2, -10, cell['s4'], cell['s5']]
    cell_gaps.append(format_title(last_row))
    return cell_gaps

def source():
    '''This function will format the source portion of the RIBO input'''
    ###Is this static information? If so lets create a .txt file and put it there
    return format_title(["T", mass, temp, 180, 0, 1, 0, 0.953, 3.498, 0, 0.258, 4.916, 0.5, 90, 90])


def tally():
    return format_title([7, 1000, 1000, 10])


def test():
    cols = 15
    dic = {"Mass":mass,"T (K)":temp,
            "Source Headers (T)":["type","Mass","T (K)","Alpha","nx","ny","nz",
                                "x","y","z","R","L","sigma","theta","phi"],
            "Tally Headers":["S","Nmax","Tmax","Tpmax"],
            "Nmax":Nmax
        }
    dic["Tally Headers"] = dic["Tally Headers"]+(cols-len(dic["Tally Headers"]))*['']
    dic["Source Headers (T)"] = dic["Source Headers (T)"]+(cols-len(dic["Source Headers (T)"]))*['']
    return dic


