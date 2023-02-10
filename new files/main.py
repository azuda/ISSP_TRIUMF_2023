import static_objects
import pandas as pd
import os
import csv

def format_title(items, cols=15):
    return items + (cols - len(items)) * ['']


def main():
    '''
    This functions purpose is to take the user input, like what type of create what thickness etc and send those variables to neccessary
    places to create the proper amount of foils.
    Next we will the necessary functions to create the RIBO input file -- Not quite sure how we format that yet.
    '''

    tar_cont = static_objects.target_container()
    surf_head_list = format_title(['#','rc','T (K)','x2','y2','z2','xy','xz','yz','x','y','z','C'])
    cell_header = format_title(["number",'S1','S2','S3','S4','S5'])
    full_blanks = format_title([])

    ## This writes the Surfaces card
    with open('./test.txt', 'w', newline='') as csvfile:
        targ = csv.writer(csvfile, delimiter='\t',lineterminator=os.linesep)
        targ.writerow(format_title(["Surfaces"]))   
        targ.writerow(surf_head_list)                 
    tar_cont.to_csv("./test.txt",mode='a',index=False,header=False,sep='\t',float_format='%.9f')

        ## Missing Surfaces Data

    ## This appends the additional data
    with open('./test.txt', 'a', newline='') as csvfile:
        targ = csv.writer(csvfile,delimiter='\t',lineterminator=os.linesep)
        dic = static_objects.test()
        sc_card = static_objects.source()
        t_card = static_objects.tally()

        ## Missing Source and Tally Data

        targ.writerow(full_blanks)
        targ.writerow(format_title(["Cells"]))
        targ.writerow(cell_header)
        targ.writerow(full_blanks)
        targ.writerow(format_title(["Source"]))
        targ.writerow(dic["Source Headers (T)"])
        targ.writerow(sc_card)
        targ.writerow(full_blanks)
        targ.writerow(format_title(["Tally"]))
        targ.writerow(dic["Tally Headers"])
        targ.writerow(t_card)
    
if __name__ == "__main__":
    main()

