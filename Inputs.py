import numpy as np
import pandas as pd
import csv
import os
import math

def exterior(ext_file,index_col=None):
#to read in text files for the exterior surfaces cells 
#i.e., the geometry of the target chamber, ionizer, etc. (not including foils)
    ext = pd.read_csv(ext_file,sep='\t',header=0,index_col=index_col,comment='*')
    return ext

def slabs(length,thickness,number,sep=0,hsep=0,squish=1,arc=False):
#Slab Spec Organization
    #note: length (cm), thickness (µm)
    #squish will be (0,1]
    #see main() for explanation of all parameters
    foil_specs = {
        "Length":length,
        "First Endcap":-length/2*squish,
        "Last Endcap":length/2*squish,
        "Thickness":thickness*1e-4, #converting to cm
        "Number":number,
        "Foil Space":length*squish,
        "Gap":(length*squish-(number*thickness*1e-4)-sep)/(number+1),
        'Hsep':hsep,
        'Arc':arc
        }
    return foil_specs

def tubes(length,r1,r2,thickness,number,sep_loc='Single',sep=0):
#Tube Spec Organization
    #length (cm)
    #r1 & r2 are outer and inner radii, respectively (cm)
    #thickness (µm)
    #number is number of concentric cylinders
    #sec_loc refers to the location of the separation between sections
        #Options are 'Single', {any of: 'Left', 'Side'}, {any of: 'Centre', 'Middle', 'Center'}
    #sep is the spacing between sections (if it exists) (cm)
    
    
    if sep != 0:
        if sep_loc in ['Centre','Center','Middle']:
            first_endcap = -length/2
            last_endcap  = length/2
            first_sep    = 0.0 - (sep/2)
            last_sep     = 0.0 + (sep/2)
        else: #Left / Side
            first_endcap = 0.0
            last_endcap  = length
            first_sep    = 0.0
            last_sep     = sep
    else:
        first_endcap = -length/2
        last_endcap  = length/2
        first_sep    = None
        last_sep     = None
    
    foil_specs = {
        "Length":length,
        "First Endcap":first_endcap,
        "Last Endcap":last_endcap,
        "First Sep":first_sep,
        "Last Sep":last_sep,
        "Thickness":thickness*1e-4, #converting to cm
        "R1":r1,
        "R2":r2,
        "Number":number,
        "Gap":(abs(r1-r2)-(number*thickness*1e-4)-sep)/number+1 
    }
    return foil_specs

def source_tally(mass,temp,Nmax):
#Use to create Source and Tally Cards
    cols = 15
    dic = {"Mass":mass,"T (K)":temp,
           "Source Headers (T)":["type","Mass","T (K)","Alpha","nx","ny","nz",
                             "x","y","z","R","L","sigma","theta","phi"],
           "Source Headers (B)":["type","Mass","T (K)","Alpha","nx","ny","nz",
                             "x","y","z","Lx","Ly","Lz","theta","phi"],
           "Source Headers (P)":["type","Mass","T (K)","Alpha","nx","ny","nz",
                             "x","y","z"],
            "Tally Headers":["S","Nmax","Tmax","Tpmax"],
            "Nmax":Nmax
           }
    #including the correct number of blank entries
    dic["Source Headers (B)"] = dic["Source Headers (B)"]+(cols-len(dic["Source Headers (B)"]))*['']
    dic["Source Headers (T)"] = dic["Source Headers (T)"]+(cols-len(dic["Source Headers (T)"]))*['']
    dic["Source Headers (P)"] = dic["Source Headers (P)"]+(cols-len(dic["Source Headers (P)"]))*['']
    dic["Tally Headers"] = dic["Tally Headers"]+(cols-len(dic["Tally Headers"]))*['']
    return dic


def slab_surf(ext,foil_specs,hsep=0):
#Creates foil surfaces along z-axis for slab-shaped geometries
#Use these surfaces in conjunction with specially-defined, geometry-specific surfaces to create cells
    surf_head_list = ['#','rc','T (K)','x2','y2','z2','xy','xz','yz','x','y','z','C',
                  "Unnamed: 13","Unnamed: 14"]   #extra tabs (format seems important)]
    
    surf_count = (ext.shape[0])
    num = surf_count + 1 #surface number; for looping
    rc  = ext["rc"][0]
    T_K = ext["T (K)"][0]
    pos = foil_specs["First Endcap"]+foil_specs["Gap"] #position
    #I've added the gap in since the loop will start with the first surface past the endcap
    #that's also why the odd_even counter starts even
    odd_even = 0 #even for foil, odd for gap

    f_surf = []

    if foil_specs["Foil Space"] != foil_specs["Length"]:
        #add the endcaps of the target as well as the foil ends
        #this is only called when the squish parameter is called 
        length = foil_specs["Length"]
        f_surf.append([num,rc,T_K,
                       0,0,0, #x**2,y**2,z**2
                       0,0,0, #xy,xz,yz
                       0,0,1, #x,y,z
                       -length/2, #C
                       '',''] )
        num += 1
        f_surf.append([num,rc,T_K,
                       0,0,0, #x**2,y**2,z**2
                       0,0,0, #xy,xz,yz
                       0,0,1, #x,y,z
                       length/2, #C
                       '',''] )
        num += 1
        
        surf_count += 2 
        #^for use in the cell generation function
        #not incremented after this since the value is for exterior surfaces 
    
    #need to add the first and last surfaces before starting!
    #since the cel generation functions make the cell with the space outside the foils first

    f_surf.append([num,rc,T_K,
                   0,0,0, #x**2,y**2,z**2
                   0,0,0, #xy,xz,yz
                   0,0,1, #x,y,z
                   foil_specs["First Endcap"], #C
                   '','']   #extra tabs (format seems important)
    ) 
    num += 1
    f_surf.append([num,rc,T_K,
                   0,0,0, #x**2,y**2,z**2
                   0,0,0, #xy,xz,yz
                   0,0,1, #x,y,z
                   foil_specs["Last Endcap"], #C
                   '','']   #extra tabs (format seems important)
    )
    num += 1

#Same loop multiple times 
#stopping at certain points to get the surface numbers of the beginning/end points of the horseshoe shapes
#If sep = 0 (aka no horseshoes), this will essentially run as one while loop ending at [last endcap - gap]
#"Couldn't you have just checked for pos being at a certain threshold?"
#It felt like a lot of unnecessary logic checks. Easier to copy/paste a couple times and add some code in between
    
    while pos < 0.0 - (hsep/2):
        line = [num,rc,T_K,
                0,0,0, #x**2,y**2,z**2
                0,0,0, #xy,xz,yz
                0,0,1, #x,y,z
                pos, #C
                '','']   #extra tabs (format seems important)
        f_surf.append(line)
        if odd_even % 2 == 0: #if the next surface is the other side of the foil
            pos += foil_specs["Thickness"]
        else: #if the next surface is the next foil
            pos += foil_specs["Gap"]
        num += 1
        odd_even += 1

    #Finding separation surface number 1
    #if the prev pos movement was to the other side of the surface, finish it off
    if odd_even % 2 == 1: 
        line = [num,rc,T_K,
                0,0,0, #x**2,y**2,z**2
                0,0,0, #xy,xz,yz
                0,0,1, #x,y,z
                pos, #C
                '','']   #extra tabs (format seems important)
        f_surf.append(line)
        pos += foil_specs["Gap"]
        
        num += 1
        odd_even += 1
    
    #all we're doing is collecting the last surface of the doughnuts
    sep_surfs = [num-1]
    
    #Continuing 
    while pos < 0.0 + (hsep/2):
        line = [num,rc,T_K,
                0,0,0, #x**2,y**2,z**2
                0,0,0, #xy,xz,yz
                0,0,1, #x,y,z
                pos, #C
                '','']   #extra tabs (format seems important)
        f_surf.append(line)
        if odd_even % 2 == 0: #if the next surface is the other side of the foil
            pos += foil_specs["Thickness"]
        else: #if the next surface is the next foil
            pos += foil_specs["Gap"]
        num += 1
        odd_even += 1
    
    #Finding separation surface number 2
    #if the prev pos movement was to the other side of the surface, go over one gap 
    #This is different than the previous, since we want the leftmost (innermost) edge of the slab
    if odd_even % 2 == 0: 
        line = [num,rc,T_K,
                0,0,0, #x**2,y**2,z**2
                0,0,0, #xy,xz,yz
                0,0,1, #x,y,z
                pos, #C
                '','']   #extra tabs (format seems important)
        f_surf.append(line)
        pos += foil_specs["Thickness"] #the other side of this foil :)
        
        num += 1
        odd_even += 1
       
    #taking the value of the first doughnut after the horseshoes
    sep_surfs.append(num-1)
    
    #Last continuation    
    while pos < foil_specs["Last Endcap"]-foil_specs["Gap"]:
        line = [num,rc,T_K,
                0,0,0, #x**2,y**2,z**2
                0,0,0, #xy,xz,yz
                0,0,1, #x,y,z
                pos, #C
                '','']   #extra tabs (format seems important)
        f_surf.append(line)
        if odd_even % 2 == 0: #if the next surface is the other side of the foil
            pos += foil_specs["Thickness"]
        else: #if the next surface is the next foil
            pos += foil_specs["Gap"]
        num += 1
        odd_even += 1
        
    if odd_even % 2 != 0: #if we're missing the other side of the last foil 
        #(DEBUG: not sure why this isn't already accounted for in the above loop)
        line = [num,rc,T_K,
                0,0,0, #x**2,y**2,z**2
                0,0,0, #xy,xz,yz
                0,0,1, #x,y,z
                pos, #C
                '','']   #extra tabs (format seems important)
        f_surf.append(line)
    
    #making a dataframe of the slab surfaces
    f_surf = pd.DataFrame(f_surf,columns=surf_head_list)
    
    #joining all surfaces 
    surf = pd.concat([ext,f_surf])
    
    return surf,surf_count,sep_surfs

def long_surf(ext,foil_specs,sep=0):
    #longitudinal surfaces (for CERN)
    surf_head_list = ['#','rc','T (K)','x2','y2','z2','xy','xz','yz','x','y','z','C',
                  "Unnamed: 13","Unnamed: 14"]   #extra tabs (format seems important)]
    surf_count = (ext.shape[0])
    num = surf_count + 1 #surface number
    rc  = ext["rc"][0]
    T_K = ext["T (K)"][0]
    pos = foil_specs["First Endcap"]+foil_specs["Gap"] #position
    #I've added the gap in since the loop will start with the first surface past the endcap
    #that's also why the odd_even counter starts even
    odd_even = 0 #even for foil, odd for gap

    f_surf = []

    #need to add the first and last ones before starting!
    #next stage makes the cell with the space outside the foils first

    f_surf.append([num,rc,T_K,
                   0,0,0, #x**2,y**2,z**2
                   0,0,0, #xy,xz,yz
                   0,1,0, #x,y,z
                   foil_specs["First Endcap"], #C
                   '','']   #extra tabs (format seems important)
    ) 
    num += 1
    f_surf.append([num,rc,T_K,
                   0,0,0, #x**2,y**2,z**2
                   0,0,0, #xy,xz,yz
                   0,1,0, #x,y,z
                   foil_specs["Last Endcap"], #C
                   '','']   #extra tabs (format seems important)
    )
    num += 1

#If sep = 0, this will essentially run as one while loop ending at [the endcap - gap]
#"Couldn't you have just checked for pos being at a certain threshold?"
#It felt like a lot of logic checks. Easier to copy/paste a couple times and add some code in between
    while pos < 0.0 - (sep/2):
        line = [num,rc,T_K,
                0,0,0, #x**2,y**2,z**2
                0,0,0, #xy,xz,yz
                0,1,0, #x,y,z
                pos, #C
                '','']   #extra tabs (format seems important)
        f_surf.append(line)
        if odd_even % 2 == 0: #if the next surface is the other side of the foil
            pos += foil_specs["Thickness"]
        else: #if the next surface is the next foil
            pos += foil_specs["Gap"]
        num += 1
        odd_even += 1
        

    #Finding separation surface number 1
    #if the prev pos movement was to the other side of the surface, finish it off
    if odd_even % 2 == 1: 
        line = [num,rc,T_K,
                0,0,0, #x**2,y**2,z**2
                0,0,0, #xy,xz,yz
                0,1,0, #x,y,z
                pos, #C
                '','']   #extra tabs (format seems important)
        f_surf.append(line)
        pos += foil_specs["Gap"]
        
        num += 1
        odd_even += 1
    
    sep_surfs = [num-1]
    
    #Continuing 
    while pos < 0.0 + (sep/2):
        line = [num,rc,T_K,
                0,0,0, #x**2,y**2,z**2
                0,0,0, #xy,xz,yz
                0,1,0, #x,y,z
                pos, #C
                '','']   #extra tabs (format seems important)
        f_surf.append(line)
        if odd_even % 2 == 0: #if the next surface is the other side of the foil
            pos += foil_specs["Thickness"]
        else: #if the next surface is the next foil
            pos += foil_specs["Gap"]
        num += 1
        odd_even += 1
    
    #Finding separation surface number 2
    #if the prev pos movement was to the other side of the surface, go over one gap 
    #This is different than the previous, since we want the leftmost (innermost) edge of the slab
    if odd_even % 2 == 0: 
        line = [num,rc,T_K,
                0,0,0, #x**2,y**2,z**2
                0,0,0, #xy,xz,yz
                0,1,0, #x,y,z
                pos, #C
                '','']   #extra tabs (format seems important)
        f_surf.append(line)
        pos += foil_specs["Thickness"] #the other side of this foil :)
        
        num += 1
        odd_even += 1
        
    sep_surfs.append(num-1)
    
    #Last continuation    
    while pos <= foil_specs["Last Endcap"]-foil_specs["Gap"]:
        line = [num,rc,T_K,
                0,0,0, #x**2,y**2,z**2
                0,0,0, #xy,xz,yz
                0,1,0, #x,y,z
                pos, #C
                '','']   #extra tabs (format seems important)
        f_surf.append(line)
        if odd_even % 2 == 0: #if the next surface is the other side of the foil
            pos += foil_specs["Thickness"]
        else: #if the next surface is the next foil
            pos += foil_specs["Gap"]
        num += 1
        odd_even += 1

    if odd_even % 2 == 0: #if we're missing the other side of the last foil
        line = [num,rc,T_K,
                0,0,0, #x**2,y**2,z**2
                0,0,0, #xy,xz,yz
                0,1,0, #x,y,z
                pos, #C
                '','']   #extra tabs (format seems important)
        f_surf.append(line)
        
    #make a dataframe of the slab surfaces
    f_surf = pd.DataFrame(f_surf,columns=surf_head_list)
    
    #join all surfaces 
    surf = pd.concat([ext,f_surf])
    
    return surf,surf_count,sep_surfs

def cyl_surf(ext,foil_specs,sep=0):
#surfaces for the concentric cylinders
    surf_head_list = ['#','rc','T (K)','x2','y2','z2','xy','xz','yz','x','y','z','C',
                  "Unnamed: 13","Unnamed: 14"]   #extra tabs (format seems important)]
    
    surf_count = (ext.shape[0])
    num = surf_count + 1 #surface number
    rc  = ext["rc"][0]
    T_K = ext["T (K)"][0]
    pos = foil_specs["R1"]+foil_specs["Thickness"] #Position: for looping. Defines radii
    #I have included the thickness since the loop will start with inner edge of the first surface
    #that's also why the odd_even counter starts odd
    #so the first iteration of the loop will set up the second iteration having the gap!
    odd_even = 1 #even for foil, odd for gap

    f_surf = []

    #need to add the first and last ones before starting!
    #cell generation functions make the cell with the space outside the foils first

    f_surf.append([num,rc,T_K,
                   0,0,0, #x**2,y**2,z**2
                   0,0,0, #xy,xz,yz
                   0,0,1, #x,y,z
                   foil_specs["First Endcap"], #C
                   '','']   #extra tabs (format seems important)
    ) 
    num += 1
    f_surf.append([num,rc,T_K,
                   0,0,0, #x**2,y**2,z**2
                   0,0,0, #xy,xz,yz
                   0,0,1, #x,y,z
                   foil_specs["Last Endcap"], #C
                   '','']   #extra tabs (format seems important)
    )
    num += 1
    
    #Separation Surfaces (if we want a space in the middle )
    if sep != 0: 
        f_surf.append([num,rc,T_K,
                       0,0,0,  #x**2,y**2,z**2
                       0,0,0, #xy,xz,yz
                       0,0,1, #x,y,z
                       foil_specs["First Sep"], #C
                       '','']   #extra tabs (format seems important)
        ) 
        num += 1
        f_surf.append([num,rc,T_K,
                       0,0,0,  #x**2,y**2,z**2
                       0,0,0, #xy,xz,yz
                       0,0,1, #x,y,z
                       foil_specs["Last Sep"], #C
                       '','']   #extra tabs (format seems important)
        ) 
        num += 1
    
    #going inwards from R1 to R2
    while pos >= foil_specs["R2"]:
        line = [num,rc,T_K,
                1,1,0, #x**2,y**2,z**2
                0,0,0, #xy,xz,yz
                0,0,0, #x,y,z
                pos**2, #C
                '','']   #extra tabs (format seems important)
        f_surf.append(line)
        if odd_even % 2 == 0: #if the next surface is the other side of the foil
            pos += foil_specs["Thickness"]
        else: #if the next surface is the next foil
            pos += foil_specs["Gap"]
        num += 1
        odd_even += 1

    #making dataframe of surfaces
    f_surf = pd.DataFrame(f_surf,columns=surf_head_list)
    
    #joining all surfaces 
    surf = pd.concat([ext,f_surf])
    
    return surf,surf_count


def symm(ext,cellx,foil_specs): 
#creates cells for the pizza/symmetrical shape
    surf,surf_count,sep_surf = slab_surf(ext,foil_specs)
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
    surf,surf_count,sep_surf = slab_surf(ext,foil_specs,hsep=hsep)
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
    
def dfoil(ext,cellx,foil_specs):
    #for classic D-shaped foils
    surf,surf_count,sep_surfs = slab_surf(ext,foil_specs)
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
    surf,surf_count,sep_surf = long_surf(ext,foil_specs)
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
    surf,surf_count = cyl_surf(ext,foil_specs,sep_loc=sep_loc,sep=sep)
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
    
def ion(ext,cellx,gradient):
    #for simulations of the ionizer by itself
    #gradient parameter is for approximating how temperature affects particles in the ionizer
    #this is only called if we're using a gradient 
    c_num = 2   #current cell number
    
    cols = 15
    cell_count = (cellx.shape[0])       #how many cells in the exterior list
    fill = cellx.shape[1]               #cells to fill with surfaces (typically 5+1 for number)
    cell_blank_num = cols-fill          #blank cells (typically 15-6=9)
    cell_blanks = cell_blank_num*['']

    for ii in range(1,cell_blank_num+1):
        cellx[str(ii)] = np.nan
    cell_head_list = cellx.columns.values.tolist()

    f_cell = []
    


    #making surfaces 
    for idx,kel in enumerate(gradient): 
        #kel = kelvin
        #making a duplicate ionizer tube surface with the new temp
        tube = [len(ext),1,kel,
                1,0,1,
                0,0,0
                -1.906,0,0,
                -0.8862,'','']
        ext.loc[len(ext)] = tube
        #creating boundary surfaces between diff temperatures in the gradient
        switch = [len(ext),1,kel,
                  0,0,0,
                  0,0,0,
                  0,1,0,
                  idx*(ionizer-1.04)/len(gradient),'','']
        ext.loc[len(ext)] = switch
    ext.loc[7,'T (K)'] = gradient[-1]
    surf = ext

    #making cells
    tube  = 8   #current tube surface number
    switch = 9  #current slab surface number (for marking the beginning and end of the gradient)

    #first one
    line = [c_num,
            -tube,   #first tube (hottest)
            6,       #first end of the ionizer
            -switch, #first switch surface 
           ]
    f_cell.append(line)
    c_num += 1
    tube  += 1
    switch += 1

    while tube <= 2*len(gradient):
        line = [c_num,
            -tube,   #current tube
            switch-1,#previous switch surface
            -switch, #current switch surface 
           ]
        while len(line) < fill:
            line.append(0)
        line = line + cell_blank_num*[np.nan]
        f_cell.append(line)
        c_num += 1
        tube  += 2  #these alternate; so each is +=2
        switch += 2

    f_cell = pd.DataFrame(f_cell,columns=cell_head_list)
    cell = pd.concat([cellx,f_cell])
    
    return surf,cell

def main(shape='d',           #See options for shape
         length=3.4,          #Main tube length (cm)
         thickness=25,        #Foil thickness (µm)
         number=470,          #Number of foils
         TARGET='test.txt',   #file path/name for target (e.g., './KW-10.t')
         temp=2300,           #global temperature
         mass=8,              #mass (8 for 8Li)
         Nmax=1000,           #number of histories for the Source card
         height=0.525,        #D-shaped
         rotate=0,            #rotation of foils 
         ionizer=5.956,       #ionizer length (cm)
         gradient=None,       #temperature gradient (K) to be used for the ionizer
         m=1,                 #slope of line for symmetrical cutout OR horseshoe design
         r1=0.9144,           #horseshoe OR cylinder exterior radius
         r2=0.3644,           #horseshoe OR cylinder interior radius
         th=np.pi/4,          #angle of symm/horse cut line (rel. to outer circle for symm, inner for horse)
         sep_loc='Single',    #cylinder: location of separation 
                                 #'Single','Left' or 'Side','Centre' or 'Center' or 'Middle'
         sep=0,               #length of region between cylinders
         hsep=0,              #length of region for horseshoes wrt doughnuts
         squish=1             #percentage of target length to house foils ('squish factor')
    ):
    
    filename = TARGET.split('/')
    if len(filename[-1]) > 20:
        print('File name is too long. RIBO will cut it off and bash scripts may not be able to find your files.')
        print('Please use a file name that is 20 characters or less.')
        return #exits before it does all this work for nothing
    
    sc_ty = source_tally(mass,temp,Nmax)
    
    #Options for shape
    d_list = ['D','d','D-shaped','d-shaped']
    s_list = ['symm','Symm']
    h_list = ['Donut','donut','doughnut','Doughnut','ring','Ring']
    lc_list = ['C-Long','c-long','c-longitudinal','C-Longitudinal'] #CERN longitudinal
    lt_list = ['T-Long','t-long','t-longitudinal','T-Longitudinal'] #TRIUMF longitudinal (no u shaped container?)
    slab_list  = d_list+s_list+h_list+lc_list+['arc']
    weird  = s_list+h_list
    
    c_list = ['coil','Coil','cylinder','Cylinder','tube','Tube']
    
    #Reading in basic universal surfaces and cells **********************************************
    surf_head_list = ['#','rc','T (K)','x2','y2','z2','xy','xz','yz','x','y','z','C',
                  "Unnamed: 13","Unnamed: 14"]   #extra tabs (format seems important)]
    
    if shape in lc_list:
        ext = exterior('./exterior-CERN.txt')
        end = 8       #surface on which to end simulation
        length = 1    #really width but this is for iterations
        thickness = 2 #resetting values to ensure CERN specs
        number = 199
        
    else:
        ext = exterior("./exterior.txt")
        if shape != 'ion':
            ext.loc[0,'C'] = r1**2              #resetting the radius of the main cylindrical surface (S1, idx 0)
        ext.loc[6,'C'] = ionizer            #resetting ionizer length (S7, idx 6)
        end = 7  #surface on which to end simulation
    
    ext.loc[:,'T (K)'] = temp           #resetting all temperatures to user defined value
    
    if shape in h_list:
        cellx = exterior("./ext-cell-h.txt")
    elif shape in lc_list:
        cellx = exterior('./ext-cell-CERN.txt')
    elif shape == 'ion':
        cellx = exterior('./ext-cell-ion.txt')
    else: 
        cellx = exterior("./ext-cell.txt")
    cellx.dropna(axis=1,inplace=True)   #drop NaNs
    
    cols = 15
    cell_count = (cellx.shape[0])       #how many cells in the exterior list
    fill = cellx.shape[1]               #cells to fill with surfaces (typically 5+1 for number)
    cell_blank_num = cols-fill          #blank cells (typically 15-6=9)
    cell_blanks = cell_blank_num*['']
    cell_real_head_list = cellx.columns.values.tolist() + cell_blanks  #for card
    
    #Setting up shape-related surfaces and cells **********************************************
    
    if shape in slab_list: 
        if shape == 'arc': arc = True
        else: arc = False
        foil_specs = slabs(length,thickness,number,sep=sep,hsep=hsep,squish=squish,arc=arc)
        if shape in weird:
            b = r1*np.cos(th) - r1*np.sin(th)*abs(m)
            a1 = np.arctan(1/abs(m))  #current angles
            a2 = np.arctan(1/(-abs(m)))
            
            xx1 = np.sin(a1+rotate)    #rotated angles
            xx2 = np.sin(a2+rotate)   
            yy1 = np.cos(a1+rotate)
            yy2 = np.cos(a2+rotate)               
            p1 = b/np.sqrt(1+m**2)
            p2 = -b/np.sqrt(1+m**2)  #from ±b/sqrt(c_x**2 + c_y**2)
            #recap = x_i*sin(a_i+rot) - y_i*cos(a_i+rot) = ±b/sqrt(m^2+1)
                #+b for positive m, -b for negative m
                #b is the x intercept ('top' of foils is +î)
            left  = [ext.shape[0]+1,temp,0,0,0,0,0,0,xx1,-yy1,0,p1,'',''] 
            right = [ext.shape[0]+2,temp,0,0,0,0,0,0,xx2,-yy2,0,p2,'',''] 
            ####^see desmos screenshot dec 1
            surfs = [left,right] 
            if shape in h_list:
                rad2  = [ext.shape[0]+3,1,temp,1,1,0,0,0,0,0,0,0,r2**2]
                surfs.append(rad2)
            for ii in surfs:      #adding these to our exterior surfaces dataframe
                ext.loc[len(ext)] = ii
            
            if shape in s_list: #symmetrical/pizza shape
                surf,cell = symm(ext,cellx,foil_specs)
                sc_card = ["T",sc_ty["Mass"],sc_ty["T (K)"],180,0,0,1,0,0,0,r1,length,0.5,0,90]
            else: #horseshoe/doughnut shape
                surf,cell = horse(ext,cellx,foil_specs,hsep=hsep)
                sc_card = ["T",sc_ty["Mass"],sc_ty["T (K)"],180,0,0,1,0,0,0,r1,length,0.5,0,90]
        elif shape in lc_list: #CERN specs (longitudinal)
            surf,cell = cern(ext,cellx,foil_specs)
            radius = np.sqrt(2)/2 #takes entire box and then some, see customsource-CERN.f for correction
            z_len   = 15
            sc_card = ["T",sc_ty["Mass"],sc_ty["T (K)"],180,
                       0,0,1, #nx
                       0,0,0, #x
                       radius,z_len,
                       0.5,0,90] #sigma, angles
        elif shape == 'arc':
            #x^{2}-1.8x+y^{2}-0.6y=-0.65
            arc = [8,1,temp,
                   1,1,0,       #x**2, y**2, z**2
                   0,0,0,       #xy, xz, yz
                   -1.8,-0.6,0, #x,y,z  
                   -0.65,'',''] #C
            ext.loc[len(ext)] = arc
            sc_card = ["T",sc_ty["Mass"],sc_ty["T (K)"],180,0,0,1,0,0,0,r1,length,0.5,0,90]
            surf,cell = dfoil(ext,cellx,foil_specs)
        else: #d-shaped
            #y*sin(T)+x*cos(T)-0.525 = 0
            #y*sin(T)+x*cos(T) = 0.525
            xx = np.cos(rotate)
            yy = np.sin(rotate)
            surf = [8,1,temp,0,0,0,0,0,0,xx,yy,0,height,'','']
            ext.loc[len(ext)] = surf
            
            surf,cell = dfoil(ext,cellx,foil_specs)
            sc_card = ["T",sc_ty["Mass"],sc_ty["T (K)"],180,0,0,1,0,0,0,r1,length,0.5,0,90]
    elif shape == 'ion': #just ionizer
        if gradient != None: #if there is a temp gradient
            surf,cell = ion(ext,cellx,gradient)
        else:
            surf,cell = ext,cellx
        sc_card = ["T",sc_ty["Mass"],sc_ty["T (K)"],180,
                   0,1,0,
                   0.953,(1.04+ionizer)/2,0, #x,y,z centre
                   0.258,ionizer-1.04, #R,L
                   0.5,90,90]
        #going to use .f file to get them to start on the end
        
    else: #concentric cylinders 
        foil_specs = tubes(length,r1,r2,thickness,number,sep_loc=sep_loc,sep=sep) 
        surf,cell = cyl(ext,foil_specs,sep_loc=sep_loc,sep=sep)

    
    #Source & Tally **********************************************      
    sc_type = sc_card[0] #pulling the first parameter so we get the right headers for the source card   
    sc_card = sc_card + (cols-len(sc_card))*[''] #adding the all-important blanks

    ty_card = [end,sc_ty["Nmax"],sc_ty["Nmax"],10] 
    #writing the whole tally card right here 
        #end = final surface to end simulation at
        #sc_ty["Nmax"] = max # of particles in simulation
        #sc_ty["Nmax"] = max time for the simulation (1s/primary)
        #10 = max time per particle (if you reach 10s, there's an issue)
    ty_card = ty_card + (cols-len(ty_card))*[''] #adding the all-important blanks
    
    #Writing File (Finally!)
    full_blanks = cols*['']
    with open(TARGET, 'w', newline='') as csvfile:
        targ = csv.writer(csvfile, delimiter='\t',lineterminator=os.linesep)
        targ.writerow(["Surfaces"]+ (cols-1)*[''])    #title
        surf_head_list[-2],surf_head_list[-1] = '','' #adding blanks
        targ.writerow(surf_head_list)                 #headers
    surf.to_csv(TARGET,mode='a',index=False,header=False,sep='\t',float_format='%.9f')
    #appending surfaces dataframe to target file
    with open(TARGET, 'a', newline='') as csvfile:
        #opening same file to write cell card
        targ = csv.writer(csvfile, delimiter='\t',lineterminator=os.linesep)
        targ.writerow(full_blanks) #a row of blanks between cards
        targ.writerow(["Cells"]+ (cols-1)*[''])   #title
        targ.writerow(cell_real_head_list)        #headers (already has blanks)
    cell.to_csv(TARGET,mode='a',index=False,header=False,sep='\t',float_format='%.9f')
    #appending cell dataframe to target file
    with open(TARGET, 'a', newline='') as csvfile:
        targ = csv.writer(csvfile, delimiter='\t',lineterminator=os.linesep)
        targ.writerow(full_blanks) #a row of blanks between cards
        targ.writerow(["Source"]+ (cols-1)*['']) #title
        #pulling the right headers
        if sc_type == 'B':
            targ.writerow(sc_ty["Source Headers (B)"])
        elif sc_type == 'T':
            targ.writerow(sc_ty["Source Headers (T)"])
        else:
            targ.writerow(sc_ty["Source Headers (P)"])
        targ.writerow(sc_card)                   #writing source card
        targ.writerow(full_blanks)               #a row of blanks between cards
        targ.writerow(["Tally"]+ (cols-1)*[''])  #title
        targ.writerow(sc_ty['Tally Headers'])    #headers
        targ.writerow(ty_card)                   #writing tally card
    #done!

main()