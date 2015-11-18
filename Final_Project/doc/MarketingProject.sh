# Miriam Baumann, 2015-11-17
# This script explains how the two python scripts are called through Git Bash, and how arguments 
# are passed to the python scripts. 

Python script 1: Ads.py
# This script creates and saves the first figure and prints a table of the regression analysis for both subplots into Bash.

For this script, 5 input arguments are required in the following order: 
1 : name of the first dataframe you want to import with the filepath (this should be the sales data)
2 : the sheetname where your data is located (of your first dataframe)

3 : name of the second dataframe you want to import with the filepath (this should be the ads data)
4 : the sheetname where your data is located (of your second dataframe)

5 : the name you want to save your figure as (You should save it as a .pdf file)

Python script 2: TypeCustomer.py
# This script creates and saves the second figure. 

For this script, 3 input arguments are required in the following order: 
1 : name of the dataframe you want to import with the filepath (will most likely be the same dataframe as the first dataframe imported in script 1)
2 : the sheetname where your data is located in the dataframe

3: the name you want to save your figure as (Again, you should save it as a .pdf file)


In GitBash, the arguments are called by typing: 

python <scripname> followed by all of the required input arguments in the correct order. 