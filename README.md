# Interlay - Practice your Koine Greek Translation Skills! 


Interlay is a simple Bible application that will display the SBLGNT text of the new testament and give you the ability to type in your own translation in a box below to save as simple text files. It is a tool to make it easy to type in translations as you venture through translating the Greek New Testament.

The application is not complicated and it does not look complicated either:



<img width="802" alt="image" src="https://github.com/endelofaustin/Interlay/assets/53027219/f94f9495-aa5a-4aee-89c7-82a3d40d1087">




The application is simple to use. You choose a book by clicking where the word IJohn appears. 
You select the book of the bible you want to write a translation for. then you will type in the citation chapter is a number and verse. For a range of verses use start-end. Chapter 1 and 1-3 would give you I John 1:1-3. 



Then in the bottom pane you can see where it says type your translation. This is where you type whatever you want. When you click save it will save the words that you have in the text box as a text file in the translation directory. The translation will be titled book.chapter.verse_range.txt. 


## Getting Started ##

In order to run the application you will need to install python and pip.



And then you will have to start a python virtual environment with the following command:

python3 -m venv venv



This will run python3 code that uses a venv (virtual environment) and creates a directory called venv for the libraries you need for a venv. 



Then you will have to run the following command:

source /venv/bin/activate

This will activate your virtual environment. 



If you need to stop the virtual environment for some reason you will have to run this command:

deactivate



Once you have pip installed you will need to install the requirements.txt.


With your virtual environment running 
Install your dependencies with this command

pip install -r requirements.txt



To run the application run in a pyhton virtual environment:
python main.py

## Android App For Phones:

To get the app running on your phone you will need to follow the following steps.

1. You will need to go to the directory of your app on your computer and run the following android build command using buildozer.

buildozer -v android debug 

This will build the apk in your bin directory i.e. -----> present_working_directory_of_app/bin/app.apk

Then in order to run on an adroid phone I have been upploading the apk to my google drive and activating / installing it from my device. 

In order to do that make you you enable installing unknown apps in the settings of your adroid phone. 

At some point I may venture down the route for Ios but at this time I have not began that endeavor. 



After this you should be good to go! 
