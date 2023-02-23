import static_objects
import foilmath
import pandas as pd
import os
import csv
import datetime



def format_title(items, cols=15):
    """Formats and writes column headers for the RIBO input file

    Args:
        items (list): list to be written to csv
        cols (int, optional): number of columns to fill, default 15
    
    Returns:
        list: header items with added blanks to fill the remaining columns
    """
    return items + (cols - len(items)) * ['']


def write_csv(filename, rows):
    """Removes targ.writerow and avoids redundant file opening/closing

    Args:
        filename (str): name of file to write to
        rows (list): content to write to file
    
    Returns:
        None
    """
    with open(filename, 'a', newline='') as csvfile:
        target = csv.writer(csvfile, delimiter='\t', lineterminator=os.linesep)
        for row in rows:
            target.writerow(row)


def main():
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


    # filename
    filename = foilmath.foil["filename"]


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
