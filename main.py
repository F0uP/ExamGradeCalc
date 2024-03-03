import parser.csvparser
from calculator.calculator import Calculator
from generator.gen import markdown_generator
import PySimpleGUI as sg
import os
import subprocess


def get_file_path():
    layout = [[sg.Text('Please select the csv file you want to use')], 
              [sg.Input(key="file_path"), sg.FileBrowse(file_types=[("CSV Files", "*.csv")])], 
              [sg.Text("Name of the exam:"), sg.InputText("OS23/24", key="exam_name")],
              [sg.Cancel(), sg.OK()]]
    window = sg.Window('File Selector', layout)
    event, values = window.read()
    window.close()
    return event, values

def get_point_border():
    sz = (10, 10, 10, 10, 10, 10, 10, 10, 10, 10)
    t = (1.0, 1.3, 1.7, 2.0, 2.3, 2.7, 3.0, 3.3, 3.7, 4.0)
    k = 0.9
    r1 = [ sg.Text(t[x], key='T'+str(x), size=(int(sz[x]*k),1) ) for x in range(len(t)) ]
    r2 = [ sg.Input(key='I'+str(x), size=(sz[x],1) ) for x in range(len(t)) ]
    layout = [[sg.Text('Please enter the point border')],
              [r1],[r2],
                [sg.Checkbox('Calculate Border Automatically', default=False, key="auto")],
                [sg.Checkbox('Border values are percentage values', default=False, key="percentage")],
              [sg.Cancel(), sg.OK()]]
    window = sg.Window('Point Border', layout)
    event, values = window.read()
    window.close()
    return event, values

def get_pass_percentage():
    layout = [[sg.Text('Please enter the pass percentage')], 
              [sg.InputText("50")], 
              [sg.Cancel(), sg.OK()]]
    window = sg.Window('Pass Percentage', layout)
    event, values = window.read()
    window.close()
    return event, values

def get_output_file_path():
    layout = [[sg.Text('Please select the output file path')], 
              [sg.Input(), sg.FileSaveAs(file_types=[("All Files", "*.*"), ("HTML Files", "*.html"), ("Markdown Files", "*.md"), ("PDF Files", "*.pdf")])], 
              [sg.Cancel(), sg.OK()]]
    window = sg.Window('Output File Selector', layout)
    event, values = window.read()
    window.close()
    return event, values

def error_popup(error_message):
    sg.popup(error_message)
    

def ask_user_for_path() -> str:
    while True:
        event, values = get_file_path()
        if event == "Cancel" or event == None:
            return None
        if values == None or values["file_path"] == "" or values["exam_name"] == "":
            error_popup("No file was selected")
        else:
            return values
        
def ask_user_for_point_border() -> int:
    while True:
        event, values = get_point_border()
        values : dict = values
        if event == "Cancel" or event == None:
            return None, None, None, None
        if values == None or "" in list(values.values()) and not values["auto"]:
            error_popup("No point border was selected and the automatic calculation was not selected")
        else:
            if values["auto"]:
                return None, True, values["percentage"]
            else:
                try:
                    point_border = [float(x[1]) for x in values.items() if x[0][0] == "I"]
                    return point_border, values["auto"], values["percentage"]
                except ValueError:
                    error_popup("The point border must be a float/number")
                    continue
        
def ask_user_for_pass_percentage() -> int:
    while True:
        event, values = get_pass_percentage()
        if event == "Cancel" or event == None:
            return None
        if values == None or values[0] == "":
            error_popup("No pass percentage was entered")
        else:
            return int(values[0])

def ask_user_for_output_file_path() -> str:
    while True:
        event, values = get_output_file_path()
        if event == "Cancel" or event == None:
            return None
        if values == None or values[0] == "":
            error_popup("No folder was selected")
        else:
            return values[0]

def main():
    values = ask_user_for_path()
    if values == None:
        return
    else:
        file_path = values["file_path"]
        exam_name = values["exam_name"]
    point_border, auto, percentage = ask_user_for_point_border()
    if point_border == None and not auto:
        return
    if auto:
        pass_percentage = ask_user_for_pass_percentage()
    else:
        pass_percentage = 50
        point_border.reverse()
    output_file_path = ask_user_for_output_file_path()
    if output_file_path == None:
        return
        
    sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF, background_color='white', time_between_frames=100)
    
    # Call the csvparser module
    parsed_data = parser.csvparser.parse_csv(file_path=file_path)
    
    calculator = Calculator(df=parsed_data, pass_percentage=pass_percentage, point_border=point_border, percentage_border=percentage)
    average_points = calculator.calc_average_points()
    grade_list = calculator.calc_all_persons_grade()
    
    if not os.path.exists(output_file_path):
        open(output_file_path, "w+").close()
        
    sep = "/"
    file_path = output_file_path.replace(os.sep, sep).split(sep)
    filename = file_path.pop()
    path = os.sep.join(file_path)
    file_type = filename.split(".")[-1]
        
    
    gen = markdown_generator(df=parsed_data, path=path, grade_list=grade_list, exam_name=exam_name, name=filename)
    gen.write_points_with_grades()
    gen.write_averages(average_points)
    gen.write_point_border(calculator.point_border)
    gen.write_grade_distro_graphic()
    
    if file_type == "md":
        gen.save_as_markdown()
    elif file_type == "pdf":
        gen.save_as_pdf()
    else:
        gen.save_as_html()
        
    subprocess.Popen(r'explorer /select,' + path + os.sep + filename)
    
main()