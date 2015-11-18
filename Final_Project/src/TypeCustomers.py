# Miriam Baumann, 2015-11-16
# Loads and cleans a dataframe in the form of an excel file.

# Importing Libraries
import pandas as pd
import xlsxwriter
import numpy as np
import sys
import statsmodels.api as sm
import matplotlib.pyplot as plt

#Defining the variables
Salesdf = sys.argv[1]
sheetname = sys.argv[2]

def main():

	Salesdata = load_data (dataframe = Salesdf, sheet = sheetname)
	print(Salesdata.head())
	
	CleanedData = clean_data(Salesdata)
	print(CleanedData.head())

	Returning_df = downsample_data(CleanedData, Returning)
	print(Returning_df.head())

def load_data (dataframe, sheet):
    '''This function loads an excel dataframe in a specified sheet'''
    #Loads the excel data using pandas 
    data = pd.read_excel(dataframe, sheetname)
    
    #Returning the data
    return data
	

def clean_data(dataframe):
	'''Cleaning the dataframe and adding a new column of Sales in Canadian dollars'''
	# Renaming the columns 
	dataframe.columns = [['Exchange_Rate', 'Customer', 'Field', 'Date_of_Order', 'Total_Sales', 'Year_of_First_Order', 'New_or_Returning']]
    # Replacing the empty values in the Exchange Rate column with 1 and setting the index to Date_of_Order
	Sales_df= dataframe[['Exchange_Rate', 'Customer', 'Field', 'Date_of_Order', 'Total_Sales', 'Year_of_First_Order', 'New_or_Returning']].replace([None], [1]).set_index('Date_of_Order')
    # Creating a new column in the data set, which puts all sales amounts in Canadian dollars. 
	Sales_df['Sales_in_CAD'] = Sales_df['Exchange_Rate'] * Sales_df['Total_Sales']
	
	return Sales_df
	
def downsample_data(dataframe1, Type):
	'''Downsampling the dataframe to containg only column necessary for plotting'''
	# Getting the columns New or Returning and Sales in CAD with the Date of Order to get the amount of sales over time 
	data = dataframe1[['New_or_Returning', 'Sales_in_CAD']]
	ReturningT = data.groupby(['New_or_Returning']).get_group('Type')
	
	return ReturningT
	
main()
	
	
	
	
	
	
	
	