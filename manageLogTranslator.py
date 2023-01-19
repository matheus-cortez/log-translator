import pandas as pd # data manipulation
import numpy as np # data manipulation
import re # for checking if a string matches certain formats
import io # transforming strings to a '.csv'-like format, so we can read it to a dataframe (table)

import warnings # stop displaying some unnecessary messages
warnings.filterwarnings('ignore')

# class initialization
class manageLogTranslator:

    # class initialization
    def __init__(self):
        pass

    # applies .strip() with undesired characters to the df
    def removeDfUndesiredCharacters(self, df):
        undesired_characters = [',','[','{','}',']','"','\'']

        for undesired_character in undesired_characters:
            df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
            df = df.applymap(lambda x: x.strip(undesired_character) if isinstance(x, str) else x)
        
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        return df


    # Reads a generic .xlsx file
    def readRealItemsTable(self, filename):
        items_table = pd.read_excel(filename, sheet_name=None)
        return items_table

    # From our items spreadsheet, selects the important tabs (Items, Voucher Exchange, Skins and Bundles)
    def cleanRealItemsTable(self, real_items_table):
        real_items_table["Items"] = real_items_table["Consumables"][["ID", "Log Name", "English"]]

        real_items_table["Items"] = real_items_table["Items"].append(real_items_table["Attack"], ignore_index = True)
        real_items_table["Items"] = real_items_table["Items"].append(real_items_table["Defense"], ignore_index = True)
        real_items_table["Items"] = real_items_table["Items"].append(real_items_table["Resources"], ignore_index = True)
        real_items_table = real_items_table["Items"].dropna(how="all") # drops rows with no information at all
        
        real_items_table = self.removeDfUndesiredCharacters(real_items_table)
        
        return real_items_table


    # this function has tons of work arounds due to the necessity of working with NaN's and its limitations.
    # many python loops were used, as well as constantly using .fillna("") and .replace("",np.nan) in order to apply some functions
    # which do not work correctly with NaN's in the dataframe. 
    def readMyItems(self,my_items):

        # transform a string to csv-like
        data = io.StringIO(my_items)

        # this block is necessary in order to read rows with blank lines. reading directly by pd.read_csv(data) would
        # eliminate all blank lines
        my_items = pd.read_csv(data,skip_blank_lines=False,header=0,sep='Th3r3IsN0S3p4r@t0r')
        first_row = my_items.columns[0]
        my_items.loc[-1]=first_row
        my_items.index = my_items.index + 1  # shifting index
        my_items.sort_index(inplace=True)
        my_items.rename(columns={first_row:0},inplace=True)
        my_items.reset_index(drop=True,inplace=True)
        
        # applying .strip() to the whole dataframe
        my_items = my_items.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        

        # starting list variables to be used later in this function
        removable_blank_rows = []
        uselessrows=[]

        my_items["isRowBlank"]=0

        # transforming float items to str
        my_items = my_items.fillna("")
        my_items = my_items.applymap(lambda x: str(int(x)) if isinstance(x, float) else x)
        my_items = my_items.replace("",np.nan)
        
        # single blank rows will be removed. 2 or more blank rows in sequence will be considered a single blank row. 
        for i in range(0,len(my_items)-1):
            #print(my_items[0][i])
            if type(my_items[0][i])!=str:
                my_items["isRowBlank"][i]=1 # bad coding. this should be improved
                if type(my_items[0][i+1])!=str:
                    removable_blank_rows.append(i+1)
                else:
                    removable_blank_rows.append(i)
                    
        #remove last blank line
        if type(my_items[0][len(my_items)-1])!=str:
            removable_blank_rows.append(len(my_items)-1)
            
        #removing undesired blank lines (single lines or more than 2 lines in sequence)
        my_items = my_items.drop(removable_blank_rows)
        my_items.reset_index(drop=True,inplace=True)
        
        #cleans our dataframe
        my_items = self.removeDfUndesiredCharacters(my_items)

        #adding the columns which we will use to distinguish what is the name to be searched
        my_items['Log Name'] = np.nan
        my_items['Total'] = np.nan

        for i in range(0,len(my_items)):
            # all the non-NaN elements are strings, so if it's a float number, it's NaN
            if type(my_items[0][i])==float:
                pass

            # If it's a string:
            else:
            #If it starts with a date & time in the log form: it's ok, but it will have nan as total
                condition1 = bool(re.match("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9]", my_items[0][i][0:19]))
                condition2 = bool(re.match("[0-9][0-9]:[0-9][0-9]:[0-9][0-9]", my_items[0][i][0:8]))
                if condition1 | condition2:
                    my_items['Log Name'][i] = my_items[0][i]

                # If it have only one ':' : it is ok, since it is most likely only 1 item
                elif len(my_items[0][i].split(':'))==2:
                    my_items['Log Name'][i] = my_items[0][i].split(':')[0]#.split()
                    my_items['Total'][i] = my_items[0][i].split(':')[1]#.split()

                else:
                    my_items['Log Name'][i] = my_items[0][i]


        my_items = self.removeDfUndesiredCharacters(my_items)

        #if the input first line is blank it will input an Unnamed row, so we need to remove that
        if my_items[0][0]=="Unnamed: 0":
           uselessrows.append(0)

        #Remove blank lines that were characters such as {} [] "" ,
        for i in range(0,len(my_items)):
            if (my_items[0][i]==""):
                uselessrows.append(i)

        my_items = my_items.drop(uselessrows)
        my_items.reset_index(drop=True,inplace=True)
        
        #restarting list variable
        uselessrows = []

        #this block makes viable using inputs such as the one below
        # "id_item": x
        # "total": y
        for i in range(1,len(my_items)):
            if (my_items["Log Name"][i-1]=="id_item") & (my_items["Log Name"][i] == "total"):
                my_items["Log Name"][i-1] = my_items["Total"][i-1]
                my_items["Total"][i-1] = my_items["Total"][i]
                uselessrows.append(i)
                                      
            else:
                if i>1: 
                    condition1 = my_items["Log Name"][i-2]=="id_item"
                    condition2 = my_items["Log Name"][i] == "total"
                    condition3 = my_items["isRowBlank"][i-1]==1
                    if condition1 & condition2 & condition3:
                        my_items["Log Name"][i-2] = my_items["Total"][i-2]
                        my_items["Total"][i-2] = my_items["Total"][i]
                        uselessrows.append(i-1)
                        uselessrows.append(i)

        my_items = my_items.drop(uselessrows)
        my_items.reset_index(drop=True,inplace=True)
        
        my_items = my_items.drop([0,"isRowBlank"], axis=1)
        
        my_items = self.removeDfUndesiredCharacters(my_items)
        my_items = my_items.fillna("")
        my_items = my_items.applymap(lambda x: str(int(x)) if isinstance(x, float) else x)
        my_items = my_items.replace("",np.nan)

        return my_items


    # takes the whole information from the spreadsheet and inserts in the input dataframe. 
    # output columns : ID, language, log name and total 
    def getMyItemsFullTable(self, my_items, real_items_table):
        
        my_items["ID"] = np.nan
        my_items["English"] = np.nan
        my_items=my_items[["ID","Log Name","Total","English"]]
        
        # list for the items which did not match in our real_items_table
        non_identified_items = []
        
        # should probably review those conditions below, they may not be necessary as long
        # as the columns can be compared directly, but it should not be a problem.
        
        # select rows which are numeric (NaN or number) in real_items_table's ID
        first_condition = pd.to_numeric(real_items_table["ID"], errors='coerce').notnull()
        # select rows without NaN in real_items_table's ID
        second_condition = real_items_table["ID"].notna()
        #change real_items_table rows which are exclusively numbers to become integer
        real_items_table.loc[first_condition & second_condition,"ID"] = real_items_table[first_condition & second_condition]["ID"].astype(int)
        integer_id_values = real_items_table[first_condition & second_condition]["ID"].astype(int).astype(str)
        
        for i in range(0,len(my_items)):
            # if we have a match with the Log Name column of real_items_table
            if my_items["Log Name"][i] in real_items_table["Log Name"].values:
                row_in_real_items_table = real_items_table["Log Name"][real_items_table["Log Name"]==my_items["Log Name"][i]].index[0]
                my_items["ID"][i] = real_items_table["ID"][row_in_real_items_table]
                my_items["English"][i] = real_items_table["English"][row_in_real_items_table]
                
            # if we have a match with the ID column of real_items_table
            elif (integer_id_values.isin([my_items["Log Name"][i]]).sum()>0):
                row_in_real_items_table = real_items_table["ID"][real_items_table["ID"].astype(str)==str(int(my_items["Log Name"][i]))].index[0]
                
                my_items["ID"][i] = my_items["Log Name"][i]
                my_items["Log Name"][i] = real_items_table["Log Name"][row_in_real_items_table]
                my_items["English"][i] = real_items_table["English"][row_in_real_items_table]
                
            # if we have no match
            else:
                non_identified_items.append(my_items["Log Name"][i])
                
            #removing NaN from list
            non_identified_items = [x for x in non_identified_items if str(x) != 'nan']
        
        my_items = my_items.replace('NaN',np.nan)
        
        #this may not be necessary, but it doesn't hurt
        my_items = self.removeDfUndesiredCharacters(my_items)
        
        
        return my_items, non_identified_items

    def returnCautionMessage(self, non_identified_items):
        message = ""      
        message = message + '* Note: For this particular translation, the elements with no match in the spreadsheet were:'
        message = message + '\n\n'
        if len(non_identified_items) == 0:
            message = message + '   None. All items had a corresponding match.'
            message = message + '\n\n'
        else:
            n = 1
            for i in non_identified_items:
                message = message +'   '+ str(n) + ') ' + str(i)
                message = message + '\n'
                n = n+1
            message = message +'\n'
        #message = message + '\n'
        message = message +'==========================================='
        message = message +'\n'
        message = message +'* Translation:'
        message = message +'\n'
        message = message +'\n'
        
        return message

    def getPlayerFrontendLanguage(self, my_items):
        my_items = my_items.fillna("") # transform NaN to a blank string
        my_items = my_items.applymap(lambda x: str(int(x)) if isinstance(x, float) else x) # transform float to str
        #my_items.strip('"')
        
        #translated_items = self.returnCautionMessage(non_identified_items)
        translated_items=""
        
        for i in range(0,len(my_items)):
            item_id = my_items["ID"][i]
            log_name = my_items["Log Name"][i]
            total = my_items["Total"][i]
            english = my_items["English"][i]
            
            '''if type(total) == str:
                total = total.strip()
            else:
                total = str(int(total))'''
            
            if total != "":
                total = ': ' + total
                
                
            if english == "":
                if item_id == "": 
                    #print(translated_items)
                    translated_items = translated_items + log_name  + total + '\n'
                    #if (log_name == total) == "": # nao sera necessario
                    #    translated_items = translated_items + '\n'
                else:
                    translated_items = translated_items + item_id + total + '\n'
            else:
                translated_items = translated_items + english + total + '\n'
                
        return translated_items


    #testando novo metodo
    def getPlayerBackendLanguage(self, my_items):
        my_items = my_items.fillna("")
        my_items = my_items.applymap(lambda x: str(int(x)) if isinstance(x, float) else x) # transform float to str

        #translated_items = self.returnCautionMessage(non_identified_items)
        translated_items=""

        uselessrows = []

        for i in range(0,len(my_items)):
            item_id = my_items["ID"][i]
            log_name = my_items["Log Name"][i]
            total = my_items["Total"][i]
            english = my_items["English"][i]

            if total != "":
                total = ': ' + total

            '''if (i != (len(my_items)-1)) & (log_name == 'id_item') & (my_items["Log Name"][i+1] == 'num'):
                                                    log_name = total
                                                    total = my_items["ID"][i+1]
                                                    uselessrows.append[i+1]
                                                    i = i+2'''

            
            # If ID is blank
            if item_id == "":
                # if Log Name is blank
                #if log_name == "":
                #    #print a blank line
                #    translated_items = translated_items + '\n'
                #else:
                #    if total != "":
                #        total = ': ' + total
                translated_items = translated_items + log_name + total + '\n'
                
            else:
                #if type(total)!=str:
                #    total = str(int(total))
                    
                #item_id=str(int(item_id))
                #if log_name != "": 
                #    item_id = item_id + " "
                   
                translated_items = translated_items + (item_id + ' '+ log_name).strip() + total + '\n'
                
        return translated_items