import os
import csv
import init

def write_csv(filename, rows):
    with open(filename, 'a', newline='') as csvfile:
        target = csv.writer(csvfile, delimiter='\t', lineterminator=os.linesep)
        for row in rows:
            target.writerow(row)
    
def to_csv(file):
    file.to_csv(init.filename, mode='a', index=False, header=False, sep='\t', float_format='%.9f')

def write_footer(input_values):
    write_csv(init.file_name(input_values), [
        init.full_blanks,
        init.format_title(["Source"]),
        init.dic["Source Headers (T)"],
        init.sc_card,
        init.full_blanks,
        init.format_title(["Tally"]),
        init.dic["Tally Headers"],
        init.t_card
    ])