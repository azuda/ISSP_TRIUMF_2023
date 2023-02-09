# functions for handling exterior target stuff

import pandas as pd



def exterior_read(ext_file, index_col=None):
    """Reads in exterior surfaces and cells from txt file.

    Args:
        ext_file (str): file path to txt file.
        index_col (int, str, optional): option for pandas.read_csv(). Defaults to None.

    Returns:
        ext (pandas dataframe): contents of txt file as a pandas dataframe.
    """
#to read in text files for the exterior surfaces cells 
#i.e., the geometry of the target chamber, ionizer, etc. (not including foils)
    ext = pd.read_csv(ext_file,sep='\t',header=0,index_col=index_col,comment='*')

    return ext



def exterior_cells(shape, ionizer=5.956, temp=2300):
    """Generates the exterior surface cells for the target chamber, ionizer, etc. (not including foils)

    Args:
        shape (str): target shape
        ionizer (int, optional): length of ionizer in cm. Defaults to 5.956.
        temp (int, optional): temperature in Kelvin. Defaults to 2300.
    
    Returns:
        cellx (pandas dataframe): exterior cells as a pandas dataframe.
    """

    # shapes dict with synonyms
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

    #Reading in basic universal surfaces and cells **********************************************
    surf_head_list = ['#','rc','T (K)','x2','y2','z2','xy','xz','yz','x','y','z','C', "Unnamed: 13","Unnamed: 14"]   #extra tabs (format seems important)]

    # if shape is CERN longitudinal, use different exterior surfaces
    if shape in shapes["lc_list"]:
        ext = exterior_read('./exterior-CERN.txt')
        end = 8       #surface on which to end simulation
        length = 1    #really width but this is for iterations
        thickness = 2 #resetting values to ensure CERN specs
        number = 199

    else:
        ext = exterior_read("./exterior.txt")
        if shape != 'ion':
            ext.loc[0,'C'] = r1**2              #resetting the radius of the main cylindrical surface (S1, idx 0)
        ext.loc[6,'C'] = ionizer            #resetting ionizer length (S7, idx 6)
        end = 7  #surface on which to end simulation

    ext.loc[:,'T (K)'] = temp           #resetting all temperatures to user defined value

    # loading the exterior cell for:
    # donut / ring
    if shape in shapes["h_list"]:
        cellx = exterior_read("./ext-cell-h.txt")
    # CERN longitudinal
    elif shape in shapes["lc_list"]:
        cellx = exterior_read('./ext-cell-CERN.txt')
    # ionizer
    elif shape == 'ion':
        cellx = exterior_read('./ext-cell-ion.txt')
    # default exterior cell
    else: 
        cellx = exterior_read("./ext-cell.txt")
    cellx.dropna(axis=1,inplace=True)   #drop NaNs

    return cellx


