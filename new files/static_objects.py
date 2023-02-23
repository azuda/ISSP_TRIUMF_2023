from foilmath import foil
import os
import pandas as pd



temp = foil["temp"]          # global temperature
mass = foil["mass"]          # mass (8 for 8Li)
Nmax = foil["nmax"]          # number of histories for Source card
ionizer = foil["ionizer"]    # ionizer?


dic = {"Mass":mass,
        "T (K)":temp,
        "Source Headers (T)":["type","Mass","T (K)","Alpha","nx","ny","nz", "x","y","z","R","L","sigma","theta","phi"],
        "Tally Headers":["S","Nmax","Tmax","Tpmax"],
        "Nmax":Nmax
        }

# target geometry shapes
shapes = {
        "d_list": ['D','d','D-shaped','d-shaped'],
        "s_list": ['symm','Symm', 'symmetrical', 'Symmetrical'],
        "h_list": ['Donut','donut','doughnut','Doughnut','ring','Ring'],
        "lc_list": ['C-Long','c-long','c-longitudinal','C-Longitudinal'], #CERN longitudinal
        "lt_list": ['T-Long','t-long','t-longitudinal','T-Longitudinal'], #TRIUMF longitudinal (no u-shaped container?)
        "slab_list": ['D','d','D-shaped','d-shaped','symm','Symm','Donut','donut','doughnut','Doughnut','ring','Ring','C-Long','c-long','c-longitudinal','C-Longitudinal','arc'],
        "weird": ['symm','Symm','Donut','donut','doughnut','Doughnut','ring','Ring'],
        "c_list": ['coil','Coil','cylinder','Cylinder','tube','Tube']
        }


def format_title(items, cols=15):
    """Formats and writes column headers for the RIBO input file

    Args:
        items (list): list to be written to csv
        cols (int, optional): number of columns to fill, default 15
    
    Returns:
        list: header items with added blanks to fill the remaining columns
    """

    return items + (cols - len(items)) * ['']


def target_container():
    """Reads and returns the supplied target container information

    Returns:
        Pandas DataFrame: target container information
    """

    file = "\\new files\static\exterior.txt"
    path = os.getcwd()+file
    return pd.read_csv(path, sep='\t',header=0,comment='*')


def top_of_foil_edge():
    """Distance from foil origin (0, 0) to the cut line of D-shaped foil

    Returns:
        Pandas DataFrame: surface information for distance from origin to edge
    """

    file = "\\new files\static\foilcut.txt"
    path = os.getcwd()+file
    return pd.read_csv(path, sep='\t',header=0,comment='*')


def target_container_endcaps(asdf):
    """Container endcaps surface information?

    Args:
        __name__ (_type_): _description_
    
    Returns:
        __type__: _description_
    """
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
    pass


def cell_gaps(foil_quantity):
    '''this function will format the cell gaps by calling a function and doing some math'''
    ###This function will need to format data to look like lines 39 to 49 by generating gaps based
    ###on how many foils we are creating, this math should look something like target_container - consumed_space_from_foils / foil_quantity + 1
    first_cell_gap = {
        'row' : 5, ## 3 static cells come before this row
        's1' : -1, ## I don't remember what this surface is???? belwow top of 
        's2' : 12, ##to the right of the end cap
        's3' : -13, ##to the left of the second foil
        's4' : -8, ## below foil cut surface
        's5' : 0 ## this isn't used but it's there
    }
    cell_gaps = '4\t-1\t9\t-11\t-8\t0\t\t\t\t\t\t\t\t\t' ## these are the metrics for row 4 which indicates to the right of the first end cap, left of the second foil       #**** Later this needs to be altered to include the cap + foil
    count = 5
    for gap in range(1,foil_quantity):
        cell_gaps += f'\n{first_cell_gap["row"]}\t{first_cell_gap["s1"]}\t{first_cell_gap["s2"]}\t{first_cell_gap["s3"]}\t{first_cell_gap["s4"]}\t{first_cell_gap["s5"]}\t\t\t\t\t\t\t\t\t'
        first_cell_gap["row"] = first_cell_gap["row"] + 1 # This increments the row of each cell
        first_cell_gap["s2"] = first_cell_gap["s2"] + 2 # This increments the surfaces to represent the foils
        first_cell_gap["s3"] = first_cell_gap["s3"] - 2 # This increments the surfraces to represent the foils
        count += 1
    # There should be one final row to the cell gaps added but im not quite sure what that line should look like right now
    last_cell_gap = {
         'row' : foil_quantity + 4,
         's1' : -1,
         's2' : first_cell_gap['s2'],
         's3' : -10,
         's4' : -8,
         's5' : 0
    }
    cell_gaps += f'\n{last_cell_gap["row"]}\t{last_cell_gap["s1"]}\t{last_cell_gap["s2"]}\t{last_cell_gap["s3"]}\t{last_cell_gap["s4"]}\t{last_cell_gap["s5"]}\t\t\t\t\t\t\t\t\t'
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


