import ion as ion
import shapes as sp
import targetStuff as ts
import numpy as np
import csv
import os

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
    
    sc_ty = ts.source_tally(mass,temp,Nmax)
    
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
        ext = ts.exterior('./exterior-CERN.txt')
        end = 8       #surface on which to end simulation
        length = 1    #really width but this is for iterations
        thickness = 2 #resetting values to ensure CERN specs
        number = 199
        
    else:
        ext = ts.exterior("./exterior.txt")
        if shape != 'ion':
            ext.loc[0,'C'] = r1**2              #resetting the radius of the main cylindrical surface (S1, idx 0)
        ext.loc[6,'C'] = ionizer            #resetting ionizer length (S7, idx 6)
        end = 7  #surface on which to end simulation
    
    ext.loc[:,'T (K)'] = temp           #resetting all temperatures to user defined value
    
    if shape in h_list:
        cellx = ts.exterior("./ext-cell-h.txt")
    elif shape in lc_list:
        cellx = ts.exterior('./ext-cell-CERN.txt')
    elif shape == 'ion':
        cellx = ts.exterior('./ext-cell-ion.txt')
    else: 
        cellx = ts.exterior("./ext-cell.txt")
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
        foil_specs = ts.slabs(length,thickness,number,sep=sep,hsep=hsep,squish=squish,arc=arc)
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
                surf,cell = sp.symm(ext,cellx,foil_specs)
                sc_card = ["T",sc_ty["Mass"],sc_ty["T (K)"],180,0,0,1,0,0,0,r1,length,0.5,0,90]
            else: #horseshoe/doughnut shape
                surf,cell = sp.horse(ext,cellx,foil_specs,hsep=hsep)
                sc_card = ["T",sc_ty["Mass"],sc_ty["T (K)"],180,0,0,1,0,0,0,r1,length,0.5,0,90]
        elif shape in lc_list: #CERN specs (longitudinal)
            surf,cell = sp.cern(ext,cellx,foil_specs)
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
            surf,cell = sp.dfoil(ext,cellx,foil_specs)
        else: #d-shaped
            #y*sin(T)+x*cos(T)-0.525 = 0
            #y*sin(T)+x*cos(T) = 0.525
            xx = np.cos(rotate)
            yy = np.sin(rotate)
            surf = [8,1,temp,0,0,0,0,0,0,xx,yy,0,height,'','']
            ext.loc[len(ext)] = surf
            
            surf,cell = sp.dfoil(ext,cellx,foil_specs)
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
        foil_specs = ts.tubes(length,r1,r2,thickness,number,sep_loc=sep_loc,sep=sep) 
        surf,cell = sp.cyl(ext,foil_specs,sep_loc=sep_loc,sep=sep)

    
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