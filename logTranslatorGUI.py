import PySimpleGUI as sg
# import pandas as pd
from manageLogTranslator import manageLogTranslator

manageLogTranslator = manageLogTranslator() #initializes manageLogTranslator.py

sg.theme('DarkAmber')   # Sets the color theme

default_output_string = "** This is the output field. Your translated elements will show up here **\n\nRemember: If you wish to output a blank line, you should input 2 or more blank lines sequentially.\n\n"
default_output_string += "Examples of Outputs:\n\nHuman Language:\nIron Sword: 1\n[Date & time - optional] [Item in Chosen Language]: [total]\n\n"
default_output_string += "Report Format:\n2023-01-01 16:50:50 950212 sword_1_1: 1\n[Date & time - optional] [ID] [Log_name]: [total]"

# the layout specifies how the elements will be arranged in the interface
layout = [
    [sg.Text('Please select the \'Item list sample.xlsx\' spreadsheet.\nOnce your file has been selected, please tap the submit button below. Note: your file must have the \'.xlsx\' extension.')],
    [sg.Input('./Item list sample.xlsx'), sg.FileBrowse(file_types=(("Excel Files", "*.xlsx"),)), sg.Button("Submit")],
    [sg.Frame(layout=[
        [sg.Button('Start Here'), sg.Button('Syntax Details'), sg.Button('Input Format Examples')]], title='Program Instructions:',title_color='red',relief=sg.RELIEF_SUNKEN),
    sg.Frame(layout=[
            [sg.Radio('Human Language', "RADIO1", default=True, size=(20,1)), sg.Radio('Report Format', "RADIO1")]], title='Desired Output:',title_color='red', relief=sg.RELIEF_SUNKEN),
    sg.Frame(layout=[
        [sg.DropDown(['English'], readonly=True, key="dropdown_language",default_value="English",size=(15,1))]], title='Desired Human Language Output:',title_color='red', relief=sg.RELIEF_SUNKEN)],
    [sg.Multiline(default_text='** This is the input field. Clear the text and insert your elements here **', size=(70, 25), key='my_items'), # originally was size =(70,30)
        sg.Multiline(default_text=default_output_string, size=(70, 25), key='translated_items')], # originally was size = (70,30)
    [sg.Button("Translate"), sg.Button("Clear text")]
        
    ]


# Creates the Window element (the interface itself)
window = sg.Window('Logs Translator (Alpha Version)', layout)

#initializes variables which will be used in the loop below
filename_position = 0
report_radio_position = 2
human_radio_position = 1
read_successful = 0

# Will run until a fatal error appears, or if the player closes the program
while True:

    event, values = window.read() # Event Loop to process "events" and get the "values" of the inputs

    if event == sg.WIN_CLOSED: # if player closes window or clicks cancel
        break # close the program

    # verifies which radio button is active
    report_radio = values[report_radio_position]
    human_radio = values[human_radio_position]

    # instruction popup
    if event == "Start Here":
        sg.popup(
                "\n Please make sure that the latest version of the spreadsheet has been selected and the Submit button has been pressed.",
                "  1) Item ID's and Log Names from Consumables, Attack, Defense and Resources are all eligible to be translated. You can mix all of those in the same input, as long as each line only contains one of those elements;",
                "  2) The translation is based on which Radio Button is selected;",
                "  3) By tapping the Translate button, the left field content will be processed, and its output will appear in the right field;",
                "  4) By tapping Clear Text, the content from both fields will be erased;",
                "  5) If the Spreadsheet format such as the column names and tab names used in the program are changed, the program will most likely stop working;",
                "  6) Currently, only the English language is available;",
                "  7) If something that you do makes the program crash, raises an error or behave weird, avoid doing it :) although it is normal for an error message to show up when closing the program.",
            title="Start Here")

    # instruction popup
    elif event == "Syntax Details":
        sg.popup(
            "  * Note 1: During the input processing, all blank lines will be removed from the output, except for 2 or more blank lines in a row: those will be considered a single blank line;",
            "  * Note 2: All '[', ']', ''', '\"', '{', and '}' will be removed from the lines start and ending;" ,
            "  * Note 3: Lines containing ':' will have the element at the left of the ':' searched in the spreadsheet. Lines containing more than one ':' won't be processed;",
            "  * Note 4: All occurances with no match will be output the same way as they were input;",
            "  * Note 5: All blank lines between sequential \"id_item\" and \"total\" will be deleted. An input such as this one: \n\n[\n  {\n    \"id_item\": 950207,\n\n    \"total\": 40\n  }\n]\n\nWill be simply processed such as this line:\n\n950207: 40\n",
            #"\nValid list input example:\n\n2023-01-01 12:56:27\npotion_2_1: 5\n950206: 5\n\npotion_2_2: 1 + 2 => 3",
        title="Syntax Details")

    # instruction popup
    elif event == "Input Format Examples":
        sg.popup(
            "\nExample 1 (ID: total_of_items):\n950209: 40\n950210: 6\n950211: 10\n",
            "\nExample 2 (Log Name: total_items_before_change + received_item_amount => total_of_items):\nsword_1_2: 40 + 20 => 60\nshield_3_4: 0 + 1 => 1\nore_3: 10 + 3 => 13\n",
            "\nExample 3 (Between brackets, id_item: ID; total: total_of_items):\n[\n{\n\"id_item\": 950209,\"total\": 40\n},\n{\n\"id_item\": 950210,\n\"total\": 6\n}\n]",
        title="Input Format Examples")
            
    # clears content
    elif event == "Clear text":
        window['my_items'].Update("")
        window['translated_items'].Update(default_output_string)

    # reads the spreadsheet specified
    elif event == 'Submit':
        try:

            filename = values[filename_position] # reads the filename specified
            real_items_table = manageLogTranslator.readRealItemsTable(filename) # reads the excel file as a dataframe

            try:
                real_items_table = manageLogTranslator.cleanRealItemsTable(real_items_table) # cleans/organizes the dataframe
                read_successful = 1 # reading was successful. will be checked later and will allow the translate button to proceed
            except Exception as e: # if there is an error during the file processing
                sg.popup('Please check if the correct file has been submit. Error during the file processing.\n\n' + str(e), title="Error")
                read_successful = 0 # reading went wrong. will be checked later and won't allow the translate button to proceed

        except Exception as e: # if there is an error during the reading
            read_successful = 0
            sg.popup('Please check if the correct file has been submit. Error during the file reading.\n\n' + str(e),title="Error")


    # translate the input to the output based on the parameters specified
    elif event == "Translate":
        #reads the input as a string
        my_items_list=values['my_items']

        if read_successful == 0:
            sg.popup('The spreadsheet hasn\'t been successfuly submit yet or there was an error during its reading process. It is only possible to proceed once it have been successfuly submitted.',title="Error")
        elif my_items_list == "": # don't process anything if there is no input
            pass
        else:
            my_items = manageLogTranslator.readMyItems(my_items_list)

            # rembember to make sure that the processing excepts in case of the wrong spreadsheet have been read
            try: 
                my_items_processed,non_identified_items = manageLogTranslator.getMyItemsFullTable(my_items, real_items_table)
            except Exception as  e:
                sg.popup('To the dev: Error during the getMyItemsFullTable() function',title="Error")

            caution_message = manageLogTranslator.returnCautionMessage(non_identified_items)

            if human_radio == True:
                translated_items = manageLogTranslator.getPlayerFrontendLanguage(my_items_processed)
                
            elif report_radio == True:
                translated_items = manageLogTranslator.getPlayerBackendLanguage(my_items_processed)

            window["translated_items"].Update(caution_message + translated_items)

window.close()


# using tab example
#if event == "trying this": # if there exists a button named 'trying this'
#    tab1_layout =  [[sg.T("string content for tab 1")]]
#
#    tab2_layout = [[sg.T('This is inside tab 2')],[sg.In(key='in')]]
#
#    newlayout=[[sg.TabGroup([[sg.Tab('Tab 1', tab1_layout), sg.Tab('Tab 2', tab2_layout)]])]]
#    newevent,newvalues = sg.Window('window name',newlayout).read()