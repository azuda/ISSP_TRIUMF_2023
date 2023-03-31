import datetime
import gui_inputs
import static_objects
import foilmath
import pandas as pd


def file_name(input_values):
    date_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    if (input_values[2] == '') and (input_values[7] == ''):
        filename = f'{date_str}.txt'
    if input_values[2] != '':
        if input_values[7] == '':
            filename = f'{input_values[2]}.txt'
        elif input_values[7] != '':
            filename = f'{input_values[7]}/{input_values[2]}.txt'
    if input_values[7] != '':
        if input_values[2] == '':
            filename = f'{input_values[7]}/{date_str}.txt'
        elif input_values[2] != '':
            filename = f'{input_values[7]}/{input_values[2]}.txt'
    return filename

def format_title(items, cols=15):
    return items + (cols - len(items)) * ['']


tar_cont = static_objects.target_container()
surf_head_list = format_title(
    ['#', 'rc', 'T (K)', 'x2', 'y2', 'z2', 'xy', 'xz', 'yz', 'x', 'y', 'z', 'C'])
cell_header = format_title(["number", 'S1', 'S2', 'S3', 'S4', 'S5'])
full_blanks = format_title([])


dic = static_objects.test()
sc_card = static_objects.source()
t_card = static_objects.tally()

def cell_gaps(foil):
    cell_gaps = foilmath.cell_gaps(foil)
    return cell_gaps

def initial_cells(foil):
    initial_cells = static_objects.cells_foil_shape(foil['shape'])
    initial_cells_frame = pd.DataFrame(initial_cells)
    return initial_cells_frame

def foil_surf_frame(input_values, foil):
    check = gui_inputs.validate(input_values)
    if input_values[1]:
        check['quantity'] = int(input_values[1])
    foil_surf_frame = pd.DataFrame(foilmath.foil_surface_output(foil))
    return foil_surf_frame

def defaults():
    default_args = {
        'mode': 'a',
        'index': False,
        'header': False,
        'sep': '\t',
        'float_format': '%.9f'
    }
    return default_args