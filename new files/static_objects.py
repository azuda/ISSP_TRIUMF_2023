import os
import pandas as pd


temp=2300         #global temperature
mass=8            #mass (8 for 8Li)
Nmax=1000         #number of histories for the Source card
ionizer=5.956     #ionizer?


dic = {"Mass":mass,"T (K)":temp,
           "Source Headers (T)":["type","Mass","T (K)","Alpha","nx","ny","nz",
                             "x","y","z","R","L","sigma","theta","phi"],
            "Tally Headers":["S","Nmax","Tmax","Tpmax"],
            "Nmax":Nmax
        }

def format_title(items, cols=15):
    return items + (cols - len(items)) * ['']

def target_container():
    '''This was a file supplied the when compared, contained the target container information for the RIBO input file.'''
    ### Why does the original use pandas here?
    file = "\\new files\static\exterior.txt"
    path = os.getcwd()+file
    return pd.read_csv(path, sep='\t',header=0,comment='*')


def top_of_foil_edge():
    '''This appears to be the distance from 0,0 (the center of the foil) to the cut of the d-shaped foil'''
    ### How will this function work with other shaped foils? Is this static content?
    file = "\\new files\static\foilcut.txt"
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
    cell_gaps = '4	-1	9	-11	-8 	0									' ## these are the metrics for row 4 which indicates to the right of the first end cap, left of the second foil       #**** Later this needs to be altered to include the cap + foil
    count = 5
    for gap in range(1,foil_quantity):
        cell_gaps += f'\n{first_cell_gap["row"]}	{first_cell_gap["s1"]}	{first_cell_gap["s2"]}	{first_cell_gap["s3"]}	{first_cell_gap["s4"]}	{first_cell_gap["s5"]}									'
        first_cell_gap["row"] = first_cell_gap["row"] + 1 # This increments the row of each cell
        first_cell_gap["s2"] = first_cell_gap["s2"] + 2 # This increments the surfaces to represent the foils
        first_cell_gap["s3"] = first_cell_gap["s3"] - 2 # This increments the surfraces to represent the foils
        count += 1
    # There should be one final row to the cell gaps added but im not quite sure what that line should look like right now
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

print(cell_gaps(10))