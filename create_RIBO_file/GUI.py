import pandas as pd
import gui_inputs
import GUI_body as gui
from csv_writer import write_csv, write_footer
import init



def main():
    '''
    This functions purpose is to take the user input, like what type of create what thickness etc and send those variables to neccessary
    places to create the proper amount of foils.
    Next we will the necessary functions to create the RIBO input file -- Not quite sure how we format that yet.
    '''

    input_values = gui.run()
    foil = gui_inputs.validate(input_values)
    kwargs = {}
    kwargs.update(init.defaults())

    # This writes the Surfaces card
    write_csv(init.file_name(input_values), [init.format_title(["Surfaces"]), init.surf_head_list])
    init.tar_cont.to_csv(init.file_name(input_values), **kwargs)
    init.foil_surf_frame(input_values, foil).to_csv(init.file_name(input_values), **kwargs)

    # This writes the Cells card
    write_csv(init.file_name(input_values), [init.full_blanks, init.format_title(["Cells"]), init.cell_header])
    init.initial_cells(foil).to_csv(init.file_name(input_values), **kwargs)
    cell_frame = pd.DataFrame(init.cell_gaps(foil))
    cell_frame.to_csv(init.file_name(input_values), **kwargs)

    # This appends the additional data
    write_footer(input_values)


if __name__ == '__main__':
    main()