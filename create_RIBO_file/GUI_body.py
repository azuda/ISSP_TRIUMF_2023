import PySimpleGUI as sg
import gui_inputs
import os
import requests
from datetime import datetime

weather_URL = "https://api.openweathermap.org/data/2.5/weather?"
flare = "*" * 40
CITY = "Vancouver"
API_KEY = '08fbd137e25ad066aedc009ccb1c2084'
URL = weather_URL + "q=" + CITY + "&appid=" + API_KEY
response = requests.get(URL)
now = datetime.now()
current_time = now.strftime("%H:%M:%S")

if int(now.strftime("%H")) < 12:
    time_message =  f"Good morning {os.getlogin()}!"
elif int(now.strftime("%H")) < 16:
    time_message =  f"Good afternoon {os.getlogin()}!"
elif int(now.strftime("%H")) < 24:
    time_message =  f"Good evening {os.getlogin()}!"

if response.status_code == 200:
    data = response.json()
    main = data['main']
    temparature = round(main['temp'] - 273.15, 1)
    low = round(main['temp_min'] - 273.15, 1)
    high = round(main['temp_max'] - 273.15, 1)
    feels_like = round(main['feels_like'] - 273.15, 1)
    report = data['weather']

weather_statement =(
        f"----------{CITY}----------\n"
        f"Temperature: {temparature}C\n"
        f"Low: {low}C\n"
        f"High: {high}C\n"
        f"Feels like: {feels_like}C\n"
        f"Report: {report[0]['description']}\n"
)

def has_invalid_characters(filename):
    invalid_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for char in invalid_chars:
        if char in filename:
            return True
    return False


def process_input(input_values):
    output = ''
    check = []
    for i in range(7):
        if input_values[i] != '':
            check.append(i)
    for inputted in check:
        if inputted == 0:
            output += f"Foil Shape: {input_values[0]}\n"
        if inputted == 1:
            output += f"Number of Foils: {input_values[1]}\n"
        if inputted == 2:
            output += f"Filename: {input_values[2]}\n"
        if inputted == 3:
            output += f"input4: {input_values[3]}\n"
        if inputted == 4:
            output += f"input5: {input_values[4]}\n"
        if inputted == 5:
            output += f"input6: {input_values[5]}\n"
        if inputted == 6:
            output += f"input7: {input_values[6]}\n"
    if input_values[7]:
        output += f"Directory: {input_values[7]}\n"
    return output


def run():
    input_values = ["" for i in range(8)]
    shape_options = ['D(default)', 'Pizza']
    layout = [[sg.Text(f'{time_message}')],
              [sg.Text(weather_statement)],
              [sg.Text('shape:'), sg.Combo(shape_options, key='input1', default_value="D(default)", pad=((78, 0), (0, 0)))],
              [sg.Text('number of foils:'), sg.InputText(key='input2', pad=((29, 0), (0, 0)))],
              [sg.Text('filename:'), sg.InputText(key='input3', pad=((65, 0), (0, 0)))],
              [sg.Text('Input 4:'), sg.InputText(key='input4', pad=((74, 0), (0, 0)))],
              [sg.Text('Input 5:'), sg.InputText(key='input5', pad=((74, 0), (0, 0)))],
              [sg.Text('Input 6:'), sg.InputText(key='input6', pad=((74, 0), (0, 0)))],
              [sg.Text('Input 7:'), sg.InputText(key='input7', pad=((74, 0), (0, 0)))],
              [sg.Text('Parameters:')],
              [sg.Multiline(size=(61, 10), key='output')],
              [sg.Text('Select directory to save output:'), sg.FolderBrowse(key='directory')],
              [sg.Submit(), sg.Cancel('Finalize')]]
    window = sg.Window('My Window', layout)

    while True:
        event, values = window.read()
        if event in (None, 'Finalize'):
            break

        if event == 'Submit':
            input_values[0] = values['input1']
            input_values[1] = values['input2']
            input_values[2] = values['input3']
            input_values[3] = values['input4']
            input_values[4] = values['input5']
            input_values[5] = values['input6']
            input_values[6] = values['input7']
            input_values[7] = values['directory']
            if input_values[0] == 'D(default)':
                input_values[0] = 'D'
                foil = gui_inputs.validate(input_values)
            elif input_values[0] == 'Pizza':
                input_values[0] = 'symm'
                foil = gui_inputs.validate(input_values)
            output = process_input(input_values)
            output += (
                f"Foil Thickness: {foil['thickness']/10000}\n"
                f"Target Container Length: {foil['length']}\n"
            )
            if len(input_values[2]) >= 20:
                output = "ERROR: Filename too long!"
            elif has_invalid_characters(input_values[2]):
                output = "ERROR: Invalid character in filename!"
            window['output'].update(output)
    window.close()
    return input_values
            