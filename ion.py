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