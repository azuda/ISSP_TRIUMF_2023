import static_objects
import pandas as pd
import os
import csv
import datetime
import foilmath



def format_title(items, cols=15):
    return items + (cols - len(items)) * ['']


def write_csv(filename, rows):
    """
    This functions helps remove the previous "targ.writerow" and opening the file twice by reducing
    the repeated lines of code. It still opens the file more than once but the code is not repeated.
    """
    with open(filename, 'a', newline='') as csvfile:
        target = csv.writer(csvfile, delimiter='\t', lineterminator=os.linesep)
        for row in rows:
            target.writerow(row)


def main():
    '''
    This functions purpose is to take the user input, like what type of create what thickness etc and send those variables to neccessary
    places to create the proper amount of foils.
    Next we will the necessary functions to create the RIBO input file -- Not quite sure how we format that yet.
    '''
    # Set variables
    tar_cont = static_objects.target_container()
    surf_head_list = format_title(
        ['#', 'rc', 'T (K)', 'x2', 'y2', 'z2', 'xy', 'xz', 'yz', 'x', 'y', 'z', 'C'])
    cell_header = format_title(["number", 'S1', 'S2', 'S3', 'S4', 'S5'])
    full_blanks = format_title([])

    # Variables for static values of Cells, Source, and Tally cards
    dic = static_objects.test()
    sc_card = static_objects.source()
    t_card = static_objects.tally()
    cell_gaps = static_objects.cell_gaps(10)  ## Send in the foil quantity to get the amount of cell gaps neccessary
    formatted_gap = cell_gaps.split('\n')


    # Get foil locations/information

    foil_surf_frame = pd.DataFrame(foilmath.foil_surface_output()) 
    

    # Set up filename
    date_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'{date_str}.txt'


    # This writes the Surfaces card
    write_csv(filename, [format_title(["Surfaces"]), surf_head_list])
    tar_cont.to_csv(filename, mode='a', index=False,
                    header=False, sep='\t', float_format='%.9f')

    foil_surf_frame.to_csv(filename,mode='a',index=False,header=False,sep='\t',float_format='%.9f')

    # Missing Surfaces Data

    # Cells Header
    write_csv(filename, [full_blanks, format_title(["Cells"]), cell_header])

    for line in formatted_gap:
        write_csv(filename, [[cell.replace('"', '')
        for cell in line.split('\t')]])

    # This appends the additional data
    write_csv(filename, [
        full_blanks,
        format_title(["Source"]),
        dic["Source Headers (T)"],
        sc_card,
        full_blanks,
        format_title(["Tally"]),
        dic["Tally Headers"],
        t_card
    ])


if __name__ == "__main__":
    main()
