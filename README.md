# bulk-csv-compare

## Requirements
* Python 3 - https://www.python.org/downloads/

## Pre-requisites
1. Create a folder named 'before' and 'after' inside the bulk-csv-compare folder if they does not exist already.
2. Before the blade flip, export the chat histories into the 'before' folder. I'd recommend naming the file the same name as the chatroom, e.g. "Chatroom 48"
3. After the blade flip, export the chat histories into the 'after' folder using the same name used for the chatroom you used before, e.g. "Chatroom 48".

In the end your directories should look something like this.
```
  .
    ├── main.py
    ├── before                # the exported chat histories BEFORE the blade flip 
    │   ├── Chatroom 48.csv          
    │   ├── Chatroom 100.csv         
    │   └── Chatoom 101.csv                
    ├── after                # the exported chat histories AFTER the blade flip      
    │   ├── Chatroom 48.csv          
    │   ├── Chatroom 100.csv         
    │   └── Chatoom 101.csv    
    ├── results.csv
    └── ...
```
## To run in Windows
1. Open directory in Windows Command Prompt 
2. Run ```py main.py```

## To run in Mac OS
1. Open directory in MacOS Terminal
2. Run ```python3 main.py```

## Flat compare
The script implementation in the **main branch** does a flat compare (checks whether two csv files are exact matches). A results.csv file is generated with the results of each chatroom passing or failing the chat history sync.

## Smarter compare
The script implementation in the **2-folder-parse branch** parses through all the lines in each csv files and creates a dict entry for each message for before and after file. Any messages missing from the /after/file.csv file is printed out onto the console. A results.csv file is generated with the results of each chatroom passing or failing the chat history sync.
