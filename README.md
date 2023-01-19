<h1><p align = "center">Log Translator</p></h1>

## 1) Context
This was my first personal project, which happened to solve real problem regarding a recurring task that I had to do in a previous professional experience. This project basically uses Python for both data manipulation and creating a Graphical User Interface (GUI) with PySimpleGUI, and can be run by simply running the logTranslatorGUI.py file **or** by running an executable file.

The purpose of this program is to provide an automatic solution to the time consuming task of translating a list of back-end log elements, which used to be done by copying element by element, searching in a spreadsheet and pasting its translation. 

It was taken into consideration making the 'project' as **easily maintainable as possible**, as well as **least complex as possible**.

It takes a **list of log elements** as **input** and **translate them to either Human Language or Report Format** (currently only English) **as output**

All the instructions regarding how to use this solution are available for the User in the program interface.

## 2) Loading the Log Translator
We have two options: You could either load it through Python itself, or by running an .exe file. Below, you will find instructions on how to do both:

## 2.1) Through Python itself
Any environment containing Python and the `pip` package system should be able to run the program:

```bash 
pip install -r requirements.txt
python logTranslatorGUI.py
```

## 2.2) Creating an .exe file
This program can be easily run by running an .exe file.
Basically, we use a `pip` package called `pyinstaller` which has the purpose of turning Python scripts into a .exe. Once we have it installed, all we have to do is run the following code in the root directory of our project:

```bash 
pip install pyinstaller`
pyinstaller --noconsole -F logTranslatorGUI.py manageLogTranslator.py
```

> '`--noconsole`' guarantees that no console (cmd) will be opened with the .exe execution

> '`-F`' guarantees that both scripts specified will be turned into a single file.

## 3) Examples

### 3.1) Practical examples of back-end logs used as Inputs in our program:

The logs that the User needed to translate could come in three different formats, and they are now able to simply copy and paste those in any of those formats achieving the same result with the translation.  

<p align="center">
  <img src="https://github.com/matheus-cortez/log-translator/blob/main/Images/1%20-%20Instructions%20Button%20(Input%20Format%20Examples).png" width="300">
</p>

### 3.1) Output example 1: translating our back-end logs to Human Language

<p align="center">
  <img src="https://github.com/matheus-cortez/log-translator/blob/main/Images/5%20-%20Translation%20(Human%20Language%2C%20Format%201).png">
</p>

<p align="center">
  <img src="https://github.com/matheus-cortez/log-translator/blob/main/Images/7%20-%20Translation%20(Human%20Language%2C%20Format%202).png">
</p>

### 3.2) Output example 2: translating our logs to the Report Format:

<p align="center">
  <img src="https://github.com/matheus-cortez/log-translator/blob/main/Images/6%20-%20Translation%20(Report%20Format%2C%20Format%201).png">
</p>

<p align="center">
  <img src="https://github.com/matheus-cortez/log-translator/blob/main/Images/8%20-%20Translation%20(Report%20Format%2C%20Format%202).png">
</p>

## 4) Additional features that could have been implemented
1. Adding **languages other than English** to the dropdown menu. I didn't implement this because at the time it wasn't really necessary to translate the log elements to another language.
2. Not being dependent for the User to download the Spreadsheet whenever it was updated.
3. Ideally, this should be a Web App with login authentication so that only authorized people can access our program.

## 5) How does it work?
This solution consists of 2 Python scripts:
* '**manageLogTranslator.py**': It's the essential part of this project, it uses all functions which will be detailed later in this file. The 'Item list sample.xlsx' spreadsheet is processed, and based on that, it takes an input (the list of log elements) and provides an output - the translated logs in the User's desired format. All this program requires to run optimally is to download the Spreadsheet again whenever it is updated. 
* '**logTranslatorGUI.py**': It's responsible for the Graphic User Interface (GUI) that have been seen in the images above. A GUI is necessary, but it doesn't necessarily have to be this one, it was just a quick implementation on how this program could work. It allows the 'manageLogTranslator.py' to be successfuly run by the User in an user-friendly way. 

## 6) Positive outcomes from this project implementation

1. **Users spent less time having the effort of translating logs**. If a user spent 7 minutes to translate a long list of packages, he will now spend about 15 seconds by simply pasting the list of elements and clicking to translate. About 30 times faster!

2. **Users no longer lost their line of thought**. With this simple solution, they can now fully focus on relevant tasks.

## 7) Data processing methods: manageLogTranslator.py in detail

You can find more information regarding the `manageLogTranslator.py` file in the <a href="https://github.com/matheus-cortez/log-translator/tree/main/docs">docs folder</a>.