# SIMPLE SERVER QUERY APP

This is an application that queries a list of servers provided in a text file; and returns information on application success rates per application version in a json file output 

## Usage
A good place to start is to install the packages in the requirements.txt in your local or virtual env `pip install -r requirements.txt`. [This is opational]

To run this application, pass in the file name in the command line `python main.py <file_name>`; where `<file_name>` is the txt file containing the list of servers at the project root. This will output a json file to the project root

The file name is left as arbitrary to allow the user to use their own txt files