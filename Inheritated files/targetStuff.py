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