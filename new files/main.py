import static_objects
import foilmath
import pandas as pd
import os
import csv



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
    # initialize statics
    tar_cont = static_objects.target_container()
    surf_head_list = static_objects.format_title(['#', 'rc', 'T (K)', 'x2', 'y2', 'z2', 'xy', 'xz', 'yz', 'x', 'y', 'z', 'C'])
    cell_header = static_objects.format_title(["number", 'S1', 'S2', 'S3', 'S4', 'S5'])
    full_blanks = static_objects.format_title([])

    # static values for Cells, Source, and Tally cards
    dic = static_objects.test()
    sc_card = static_objects.source()
    t_card = static_objects.tally()
    cell_gaps = static_objects.cell_gaps(10)  ## Send in the foil quantity to get the amount of cell gaps neccessary
    formatted_gap = cell_gaps.split('\n')


    # get foil locations / info
    foil_surf_frame = pd.DataFrame(foilmath.foil_surface_output()) 


    # get filename
    filename = foilmath.foil["filename"]


    # write the Surfaces card
    write_csv(filename, [static_objects.format_title(["Surfaces"]), surf_head_list])
    tar_cont.to_csv(filename, mode='a', index=False, header=False, sep='\t', float_format='%.9f')
    foil_surf_frame.to_csv(filename,mode='a',index=False,header=False,sep='\t',float_format='%.9f')

    # Missing Surfaces Data

    # Cells header
    write_csv(filename, [full_blanks, static_objects.format_title(["Cells"]), cell_header])

    for line in formatted_gap:
        write_csv(filename, [[cell.replace('"', '')
        for cell in line.split('\t')]])

    # append additional data
    write_csv(filename, [
        full_blanks,
        static_objects.format_title(["Source"]),
        dic["Source Headers (T)"],
        sc_card,
        full_blanks,
        static_objects.format_title(["Tally"]),
        dic["Tally Headers"],
        t_card
    ])



if __name__ == "__main__":
    main()
