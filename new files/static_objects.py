import os
import pandas as pd

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

def cell_gaps():
    '''this function will format the cell gaps by calling a function and doing some math'''
    ###This function will need to format data to look like lines 39 to 49 by generating gaps based
    ###on how many foils we are creating, this math should look something like target_container - consumed_space_from_foils / foil_quantity + 1 
    pass

def source():
    '''This function will format the source portion of the RIBO input'''
    ###Is this static information? If so lets create a .txt file and put it there
    pass

def tally():
    ###I'm not really sure what this does or how to generate this information.
    pass
