import numpy as np
import pandas as pd
import csv
import os
import math

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
