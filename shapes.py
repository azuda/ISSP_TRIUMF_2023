import numpy as np
import pandas as pd
import surface as sfs

#notes
#dfoil() and symm() are our main focus

def dfoil(ext,cellx,foil_specs):
    #for classic D-shaped foils
    surf,surf_count,sep_surfs = sfs.slab_surf(ext,foil_specs)
    #surf: the dataframe of the surfaces
    #surf_count: the number of surfaces in the exterior geometry
    #sep_surf: surface numbers of separation (not applicable here)
    
    cols = 15
    cell_count = (cellx.shape[0])       #how many cells in the exterior list
    fill = cellx.shape[1]               #cells to fill with surfaces (typically 5+1 for number)
    cell_blank_num = cols-fill          #blank cells (typically 15-6=9)
    cell_blanks = cell_blank_num*['']

    #setting up correct length for cell headers for dataframe
    for ii in range(1,cell_blank_num+1):
        cellx[str(ii)] = np.nan
    cell_head_list = cellx.columns.values.tolist()
    
    c_num = cell_count + 1    #cell number
    
    f_cell = []
    if foil_specs["Foil Space"] != foil_specs["Length"]:
        end1 = surf_count - 1     #surface number of the first endcap
        end2 = surf_count         #surface number of the last endcap
        foil1 = surf_count + 1    #surface number of the outer edge of the first foil
        foil2 = surf_count + 2    #surface number of the outer edge of the last foil
        sf =  foil1 + 2           #current surface number (to use for looping)
        surfs = (surf.shape[0])   #total number of surfaces (so we stop making cells when we run out of surfaces)

        #this is true for the squish parameter != 0
        #NOTE: everything here shifts back two
        height = surf_count - 2
        #so we can use this function for the arc version of it as well
        if foil_specs["Arc"] == True:
            height = -height
            #this makes "below height" outside the ellipsoid (cylinder's face)
            #and "above height" inside the ellipsoid
        #space above height; add spaces in on either side of the foils
        line = [c_num,
                       -1,             #inside main cylinder
                       end1,           #first endcap
                       -end2,          #last endcap
                       height]         #above height

        while len(line) < fill:
            line.append(0)
        line = line + cell_blank_num*[np.nan]
        f_cell.append(line)
        c_num += 1 
        
        line = [c_num,
                       -1,             #inside main cylinder
                       end1,           #first endcap
                       -foil1,         #first foil
                       -height]        #below height
        while len(line) < fill:
            line.append(0)
        line = line + cell_blank_num*[np.nan]
        f_cell.append(line)
        c_num += 1 
        
        line = [c_num,
                       -1,             #inside main cylinder
                       end2,           #last endcap
                       -foil2,         #last foil
                       -height]        #below height
        while len(line) < fill:
            line.append(0)
        line = line + cell_blank_num*[np.nan]
        f_cell.append(line)
        c_num += 1 
        
    else:
        f_first = surf_count + 1  #surface number of the outer edge of the first endcap
        sf =  f_first+2           #current surface number (to use for looping)
        surfs = (surf.shape[0])   #total number of surfaces (so we stop making cells when we run out of surfaces)

        height = surf_count
        if foil_specs["Arc"] == True:
            height = -height
            #this makes "below height" outside the ellipsoid (cylinder's face)
            #and "above height" inside the ellipsoid
        line = [c_num,
                       -1,            #inside main cylinder
                       f_first,       #first endcap
                       -(f_first+1),  #last endcap
                       height]        #above height

        while len(line) < fill:
            line.append(0)
        line = line + cell_blank_num*[np.nan]
    
        f_cell.append(line)
        c_num += 1 
    
    line = [c_num,
                   -1,         #inside main cylinder
                   f_first,    #first endcap
                   -sf,        #first foil edge
                   -height]    #below height
    sf+=1
    c_num+=1
    
    while len(line) < fill:
        line.append(0)
    line = line + cell_blank_num*[np.nan]
    f_cell.append(line)

    #main loop for cells
    while sf+1 < surfs:
        line = [c_num,
                -1,    #fixed
                sf,   #one
                -(sf+1),  #the other
                -height] #fixed 

        while len(line) < fill:
            line.append(0)
        line = line + cell_blank_num*[np.nan]
        f_cell.append(line)
        sf += 2
        c_num += 1
    
    #last one: last foil edge to last endcap
    line = [c_num,
            -1,          #inside main cylinder
            sf,         #last foil edge
            -(f_first+1),   #last endcap
            -height] #below height 

    while len(line) < fill:
        line.append(0)
    line = line + cell_blank_num*[np.nan]
    f_cell.append(line)

    f_cell = pd.DataFrame(f_cell,columns=cell_head_list)
    cell = pd.concat([cellx,f_cell])
    return surf,cell

def cern(ext,cellx,foil_specs):
    surf,surf_count,sep_surf = sfs.long_surf(ext,foil_specs)
    #surf: the dataframe of the surfaces
    #surf_count: the number of surfaces in the exterior geometry
    #sep_surf: surface numbers of separation (not applicable here)
    
    cols = 15
    cell_count = (cellx.shape[0])       #how many cells in the exterior list
    fill = cellx.shape[1]               #cells to fill with surfaces (typically 5+1 for number)
    cell_blank_num = cols-fill          #blank cells (typically 15-6=9)
    cell_blanks = cell_blank_num*['']
    
    #headers for cell card
    for ii in range(1,cell_blank_num+1):
        cellx[str(ii)] = np.nan
    cell_head_list = cellx.columns.values.tolist()
    
    c_num = cell_count + 1    #cell number
    f_first = surf_count + 3  #surface number of the outer edge of the first foil
    sf =  f_first             #current surface number (to use for looping)
    surfs = (surf.shape[0])   #total number of surfaces (so we stop making cells when we run out of surfaces)

    top   = 11  #surface number of the top edge of the foils
    base  = 9   #surface number of the inside of the U-shaped base
    
    front = 18  #surface number where foils start (lengthwise)
    back  = 19  #surface number where foils end (lengthwise)
    
    left  = 12  #surface number of the left side of the U-shaped container
    right = 13  #surface number of the left side of the U-shaped container
    
    #outside the box
    line = [c_num,    #cell number
            -top,     #below top of U-shaped container
            base,     #above base of U-shaped container
            front,    #between gaps in target chamber
            -back,
            left,     #right of left container edge
            -f_first  #left of first foil
           ]
    
    c_num += 1
    while len(line) < fill:
        line.append(0)
    line = line + cell_blank_num*[np.nan]
    f_cell = [line] 
    

    #main loop for cells
    while sf+1 < surfs:
        line = [c_num,    #cell number
                -top,     #below top of U-shaped container
                base,     #above base of U-shaped container
                front,    #between gaps in target chamber
                -back,
                sf,       #right of first foil
                -(sf+1)   #left of second foil
               ]

        while len(line) < fill:
            line.append(0)
        line = line + cell_blank_num*[np.nan]
        f_cell.append(line)
        sf += 2
        c_num += 1
    
    #last one: last foil edge to last endcap
    line = [c_num,    #cell number
            -top,     #below top of U-shaped container
            base,     #above base of U-shaped container
            front,    #between gaps in target chamber
            -back,
            sf,     #right of last foil
            -right  #left of container edge
           ]

    while len(line) < fill:
        line.append(0)
    line = line + cell_blank_num*[np.nan]
    f_cell.append(line)

    f_cell = pd.DataFrame(f_cell,columns=cell_head_list)
    cell = pd.concat([cellx,f_cell])
    return surf,cell
    
def cyl(ext,cellx,foil_specs,sep_loc='Single',sep=0):
    #for the concentric cylinders (mimicking a spiral)
    #can't actually use a spiral as its equation is not quadric
    surf,surf_count = sfs.cyl_surf(ext,foil_specs,sep_loc=sep_loc,sep=sep)
    #surf: the dataframe of the surfaces
    #surf_count: the number of surfaces in the exterior geometry
    
    cols = 15
    cell_count = (cellx.shape[0])       #how many cells in the exterior list
    fill = cellx.shape[1]               #cells to fill with surfaces (typically 5+1 for number)
    cell_blank_num = cols-fill          #blank cells (typically 15-6=9)
    cell_blanks = cell_blank_num*['']
    
    #headers for cell card    
    for ii in range(1,cell_blank_num+1):
        cellx[str(ii)] = np.nan
    cell_head_list = cellx.columns.values.tolist()
    
    c_num = cell_count + 1      #cell number
    first_end = surf_count + 1  #surface number of the first endcap
    last_end  = surf_count + 2  #surface number of the last endcap
    surfs = (surf.shape[0])     #total number of surfaces (so we stop making cells when we run out of surfaces)

    sf = surf_count + 3         #use in loop (reset in the if statement) 
    
    f_cell = []
    
    if sep != 0:
        first_sep = surf_count + 3
        last_sep  = surf_count + 4
        sf =  surf_count + 5             #current surface number (to use for looping)
        line = [c_num,
                -1,          #inside main cylinder
                first_sep,   #end of first section of cylinders
                -last_sep,   #start of second section of cylinders
               ]
        while len(line) < fill:
            line.append(0)
        line = line + cell_blank_num*[np.nan]
        f_cell.append(line)
        
        c_num += 1
        sf += 1
        #main loop
        while sf+1 <= surfs: 
            #R2 is at the end, not near the beginning
            #so we can go straight to the end without having to stop and grab R2
            #left side
            line = [c_num,
                    first_endcap,   #first endcap
                    -first_sep,     #first edge where the separation gap starts
                    -sf,            #inside exterior cylinder
                    sf+1,           #outside interior cylinder
                   ]

            while len(line) < fill:
                line.append(0)
            line = line + cell_blank_num*[np.nan]
            f_cell.append(line)
            
            c_num += 1
            
            #right side
            line = [c_num,
                    last_sep,       #second edge where the separation gap ends
                    -last_endcap,   #last endcap
                    -sf,            #inside exterior cylinder
                    sf+1,           #outside interior cylinder
                   ]

            while len(line) < fill:
                line.append(0)
            line = line + cell_blank_num*[np.nan]
            f_cell.append(line)
            
            c_num += 1
            sf += 2

        
    else:   
        #main loop
        while sf+1 <= surfs:
            line = [c_num,
                    first_endcap,   #two endcaps
                    -last_endcap,
                    -sf,            #inside exterior cylinder
                    sf+1,           #outside interior cylinder
                   ]

            while len(line) < fill:
                line.append(0)
            line = line + cell_blank_num*[np.nan]
            f_cell.append(line)
            sf += 2
            c_num += 1
        
    f_cell = pd.DataFrame(f_cell,columns=cell_head_list)
    cell = pd.concat([cellx,f_cell])
    return surf,cell    

def symm(ext,cellx,foil_specs): 
#creates cells for the pizza/symmetrical shape
    surf,surf_count,sep_surf = sfs.slab_surf(ext,foil_specs)
    #surf: the dataframe of the surfaces
    #surf_count: the number of surfaces in the exterior geometry
    #sep_surf: surface numbers of separation (not applicable here)
    
    cols = 15                           #how many columns in the final input file
    cell_count = (cellx.shape[0])       #how many cells in the exterior list
    fill = cellx.shape[1]               #cells to fill with surfaces (typically 5+1 for number)
    cell_blank_num = cols-fill          #blank cells (typically 15-6=9)
    cell_blanks = cell_blank_num*['']
    #headers for cell card
    for ii in range(1,cell_blank_num+1):
        cellx[str(ii)] = np.nan
    cell_head_list = cellx.columns.values.tolist()
    
    left,right = surf_count-1,surf_count  #surface numbers of the pizza-shaped cutout
    c_num = cell_count + 1                #cell number
    f_first = surf_count + 1              #surface number of the outer edge of the first endcap
    sf =  f_first+2                       #current surface number (to use for looping)
    surfs = (surf.shape[0])               #total number of surfaces 
                                          #so we stop making cells when we run out of surfaces
    #list to become dataFrame of cells
    f_cell = []
    
    #cutout: across the whole target chamber length
    line = [c_num,
                   -1,           #inside main cylinder
                   f_first,      #first endcap
                   -(f_first+1), #last endcap
                   -left,right]
    while len(line) < fill:
        line.append(0)
    line = line + cell_blank_num*[np.nan]
    f_cell.append(line)
    c_num += 1
    
    #this next 'line' only gets the section mirroring the cutout (central portion); we need to get the sides too
    #see ./Sketches/Pizza-Cells.jpeg for rationale for left, centre, right
    #central portion
    line = [c_num,
                   -1,          #inside main cylinder
                   f_first,     #first endcap
                   -sf,         #first foil edge
                   left,-right] #under cutout
    #RIBO requires the cells to have the same number of surface numbers
    #it uses 0 as a placeholder when cells have fewer surfaces than others in the list
    while len(line) < fill:
        line.append(0)
    line = line + cell_blank_num*[np.nan]
    f_cell.append(line)
    c_num += 1
    
    #left portion
    line = [c_num,
                   -1,          #inside main cylinder
                   f_first,     #first endcap
                   -sf,         #first foil edge
                   left,right]  #left portion
    
    while len(line) < fill:
        line.append(0)
    line = line + cell_blank_num*[np.nan]
    f_cell.append(line)
    c_num += 1
    
    #right portion
    line = [c_num,
                   -1,          #inside main cylinder
                   f_first,     #first endcap
                   -sf,         #first foil edge
                   -left,-right]#right portion
    
    while len(line) < fill:
        line.append(0)
    line = line + cell_blank_num*[np.nan]
    f_cell.append(line)
    c_num += 1
    sf+=1
    
    #main loop for cells
    #REPEAT COMMENT:
        #the first cell in the loop only gets the section mirroring of the cutout 
        #we need to get the sides too
    while sf+1 <= surfs:
        #central portion
        line = [c_num,
                -1,       #target cylinder
                sf,       #one surface
                -(sf+1),  #the other
                left,-right] 

        while len(line) < fill:
            line.append(0)
        line = line + cell_blank_num*[np.nan]
        f_cell.append(line)
        c_num += 1
        
        #left portion
        line = [c_num,
                -1,
                sf,
                -(sf+1),
                left,right]
        while len(line) < fill:
            line.append(0)
        line = line + cell_blank_num*[np.nan]
        f_cell.append(line)
        c_num += 1
        
        #right portion
        line = [c_num,
                -1,
                sf,
                -(sf+1),
                -left,-right]
        while len(line) < fill:
            line.append(0)
        line = line + cell_blank_num*[np.nan]
        f_cell.append(line)
        c_num += 1
        #-----------
        sf += 2
    
    #last set: last foil edge to last endcap
    #central portion
    line = [c_num,
            -1,           #inside main cylinder
            sf,           #last foil edge
            -(f_first+1), #last endcap
            left,-right]  

    while len(line) < fill:
        line.append(0)
    line = line + cell_blank_num*[np.nan]
    f_cell.append(line)
    
    c_num += 1
    
    #left portion
    line = [c_num,
            -1,            #inside main cylinder
            sf,            #last foil edge
            -(f_first+1),  #last endcap
            left,right]  

    while len(line) < fill:
        line.append(0)
    line = line + cell_blank_num*[np.nan]
    f_cell.append(line)
    
    c_num += 1
    
    #right portion
    line = [c_num,
            -1,            #inside main cylinder
            sf,            #last foil edge
            -(f_first+1),  #last endcap
            -left,-right]  

    while len(line) < fill:
        line.append(0)
    line = line + cell_blank_num*[np.nan]
    f_cell.append(line)

    #converting to dataframe
    f_cell = pd.DataFrame(f_cell,columns=cell_head_list)
    #joining all cells
    cell = pd.concat([cellx,f_cell])
    return surf,cell
    
def horse(ext,cellx,foil_specs,hsep=0):
    #doughnut/horseshoe shape
    #Note: Within the hsep gap, it uses horseshoe shape. Outside of that, it uses the doughnut shape
    surf,surf_count,sep_surf = sfs.slab_surf(ext,foil_specs,hsep=hsep)
    #surf: the dataframe of the surfaces
    #surf_count: the number of surfaces in the exterior geometry
    #sep_surf: surface numbers of separation (horseshoe start and end)
    
    cols = 15                           #how many columns in the final input file
    cell_count = (cellx.shape[0])       #how many cells in the exterior list
    fill = cellx.shape[1]               #cells to fill with surfaces (typically 5+1 for number)
    cell_blank_num = cols-fill          #blank cells (typically 15-6=9)
    cell_blanks = cell_blank_num*['']
    
    #headers for cell card
    for ii in range(1,cell_blank_num+1):
        cellx[str(ii)] = np.nan
    cell_head_list = cellx.columns.values.tolist()
    
    c_num = cell_count + 1    #cell number
    f_first = surf_count + 1  #surface number of first endcap
    f_last  = surf_count + 2  #surface number of last endcap
    left  = surf_count - 2    #surface number of left line in horseshoe cutout
    right = surf_count - 1    #surface number of right line in horseshoe cutout
    r2 = surf_count           #surface number of interior cylinder
    #note: surf_count is the number of surfaces in the exterior.txt file, but the main function has added some
        #  so the final value is 10 (as of 11/14)
    sf = f_first + 2          #current surface number (to use for looping)
    surfs = surf.shape[0]     #total number of surfaces (so we stop making cells when we run out of surfaces)
    
    f_cell = []
    #Three large cells! 
        #The one that goes outside the main cylinder 
        #The one that goes inside the interior cylinder (spans target chamber length)
        #The one that describes the cutout of horseshoes
    line = [c_num,
            1,                #outside the exterior cylinder
            -(f_first),  #left of first endcap
            (f_last)    #right of last endcap
           ]
    c_num+=1
    while len(line) < fill:
        line.append(0)
    line = line + cell_blank_num*[np.nan]
    f_cell.append(line)
    
    line = [c_num,
            -surf_count,      #inside the interior cylinder
            (f_first),        #first endcap
            -(f_last)         #last endcap
           ]
    c_num+=1
    while len(line) < fill:
        line.append(0)
    line = line + cell_blank_num*[np.nan]
    f_cell.append(line)
    
    line = [c_num,
            -1,                           #inside the main cylinder
            surf_count,                   #outside the interior cylinder
            sep_surfs[0],-sep_surfs[1],   #surfaces of the innermost doughnuts
            -(left),right                 #straight edges of the horseshoe shape
           ]
    c_num+=1
    while len(line) < fill:
        line.append(0)
    line = line + cell_blank_num*[np.nan]
    f_cell.append(line)
    
    #main loop for cells
    while sf <= sep_surfs[0]:
        line = [c_num,
                -1,           #in exterior cylinder
                sf,           #one slab surface
                -(sf+1),      #the other
                surf_count]   #outside interior cylinder

        while len(line) < fill:
            line.append(0)
        line = line + cell_blank_num*[np.nan]
        f_cell.append(line)
        sf += 2
        c_num += 1
        
    while sf < sep_surfs[1]: #for all the horseshoe ones (since we've already defined the cutout space)
        #like the pizza/symm shape, we need to to three cells for each here.
        #central
        line = [c_num,
                -1,           #in exterior cylinder
                sf,           #one slab surface
                -(sf+1),      #the other
                left,-right,  #central portion
                surf_count]   #outside interior cylinder

        while len(line) < fill:
            line.append(0)
        line = line + cell_blank_num*[np.nan]
        f_cell.append(line)
        c_num += 1
        
        #left
        line = [c_num,
                -1,           #in exterior cylinder
                sf,           #one slab surface
                -(sf+1),      #the other
                left,right,   #left portion
                surf_count]   #outside interior cylinder

        while len(line) < fill:
            line.append(0)
        line = line + cell_blank_num*[np.nan]
        f_cell.append(line)
        c_num += 1
        
        #right
        line = [c_num,
                -1,           #in exterior cylinder
                sf,           #one slab surface
                -(sf+1),      #the other
                -left,-right, #right portion
                surf_count]   #outside interior cylinder

        while len(line) < fill:
            line.append(0)
        line = line + cell_blank_num*[np.nan]
        f_cell.append(line)
        c_num += 1
        
        sf += 2
    #back to the doughnuts   
    while sf+1 < surfs:
        line = [c_num,
                -1,           #in exterior cylinder
                sf,           #one slab surface
                -(sf+1),      #the other
                surf_count]   #outside interior cylinder

        while len(line) < fill:
            line.append(0)
        line = line + cell_blank_num*[np.nan]
        f_cell.append(line)
        sf += 2
        c_num += 1
        
    #last one (uses last endcap)
    line = [c_num,
                -1,           #in exterior cylinder
                sf,           #one slab surface
                -f_last,      #the other
                surf_count]   #outside interior cylinder

    while len(line) < fill:
        line.append(0)
    line = line + cell_blank_num*[np.nan]
    f_cell.append(line)
    
    #converting to dataframe
    f_cell = pd.DataFrame(f_cell,columns=cell_head_list)
    #joining all cells
    cell = pd.concat([cellx,f_cell])
    return surf,cell
    
