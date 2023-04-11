import numpy as np
import math
import inputs


def foil_area(foil):
    d_list = ['D','d','D-shaped','d-shaped'] #list of shapes that are D-shaped
    if foil["shape"] in d_list:
        return d_shape_area(foil)

def d_shape_area(foil): 

    density   = 16.69 # Density of tantalum in g/cm3
    thick_cm  = foil['thickness']*1e-4 #convert thickness to cm
    r1    = foil['radius'] #radius of foil
    height = foil['height'] #height of foil
    sep = foil['sep'] #length of region between cylinders in cm
    
    
    ##note: 'height' is d in source equation (see https://en.wikipedia.org/wiki/Circular_segment)
    slice_area  = r1**2 * (np.arccos(1 - (r1-height)/r1)) - (height) * np.sqrt(r1**2 - height**2) #area of the piece of cut foil
    AREA = np.pi*r1**2 - slice_area # area of the foil without the cutout
    tot_surface_area = AREA * 2      #total surface area (not including the thin edges
    mass = AREA * thick_cm * density #actual mass used
    
    #create dictionary of values to report
    things = {
        'Area':AREA,
        'Total Area':tot_surface_area,
        'Mass':mass
    }
    return things

def pizza_area(foil):
    thick_cm  = foil['thickness']*1e-4 #convert thickness to cm
    density   = 16.69 # Density of tantalum in g/cm3

    r1 = foil['radius']
    th = np.pi / 4  # th = foil['th']
    m = 1 # m = foil['m']

    # !!! Both of 'th' and 'm' should not be hard coded, they should be values inside of 'foil' dictionary. However, they have not
    # Been added to the dictionary yet. I will add them in later.


    b = r1 * np.cos(th) - r1 * np.sin(th) * abs(m)
    # b is the x intercept of the two lines in the cutout

    A = (0, b)
    B = (r1 * np.sin(th), r1 * np.cos(th))
    C = (0, r1)

    triangle = 0.5 * abs(A[0] * (B[1] - C[1]) + B[0] * (C[1] - A[1]) + C[0] * (A[1] - B[1]))

    # segment above chord
    segm = 0.5*r1**2 * (th-np.sin(th))
    circle = np.pi*r1**2

    AREA = circle - triangle - segm
    tot_surface_area = AREA * 2 # Area without the thin edges
    mass = AREA * thick_cm * density #actual mass used

    things = {
        'Area': AREA,
        'Total Area': tot_surface_area,
        'Mass': mass
    }
    return things

if __name__ == "__main__":
    foil = inputs.validate()
    print(foil)
    print(d_shape_area(foil))