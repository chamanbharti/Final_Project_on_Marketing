# Miriam Baumann, 2015-11-16
# This script loads an excel dataframe related to Sales and Type of customer. 
# It cleans, and downsamples the data to make two seperate tables; one representing 
# only new customers, the other representing returning customers. The script then 
# creates a figure with two subplots representing the aforementioned groups over time.

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

savename = sys.argv[3]

def main():

	Salesdata = load_data (dataframe = Salesdf, sheet = sheetname)
	
	CleanedData = clean_data(Salesdata)

	Type_R = downsample_data(CleanedData)
	
	Type_N = downsample_data1(CleanedData)
	
	plotting = plot(Type_R.Date_of_Order, Type_R.Sales_in_CAD, Type_N.Date_of_Order, Type_N.Sales_in_CAD, savename)
	print (plotting)

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
	
def downsample_data(dataframe1):
	'''Downsampling the dataframe to containg only columns necessary for plotting'''
	# Getting the columns New or Returning and Sales in CAD with the Date of Order to get the amount of sales over time 
	data = dataframe1[['New_or_Returning', 'Sales_in_CAD']]
	#Creating a seperate dataframe with just returning customers
	Returning_C = data.groupby(['New_or_Returning']).get_group('Returning ').reset_index()
	
	return Returning_C
	
def downsample_data1(dataframe1):	
	# Getting the columns New or Returning and Sales in CAD with the Date of Order to get the amount of sales over time 
	data = dataframe1[['New_or_Returning', 'Sales_in_CAD']]
	# Creating a seperate dataframe with just New customers
	New_C = data.groupby(['New_or_Returning']).get_group('New').reset_index()
	
	return New_C
	
def plot(data1column, data1column2, data2column, data2column2, plotname):
	'''This function creates 2 scatter plot of two different variables over time, 
	and saves the figure'''
	# Making a plot to compare Sales from New and Returning customers over time
	
	plt.figure(figsize = (15,10))
	
	#Making the fist subplot
	plt.subplot(2,1,1)
	plt.plot(data1column, data1column2, 'ro')
	plt.ylim(-500, 50000)
	plt.ylabel(data1column2.name)
	plt.title ('Sales to Returning Customers over Time')
	
	#Making the fist subplot
	plt.subplot(2,1,2)
	plt.plot(data2column, data2column2, 'go')
	plt.ylim(-500, 50000)
	plt.ylabel(data2column2.name)
	plt.title ('Sales to New Customers over Time')
	
	#Saving the plot to a new file 
	plt.savefig(plotname)
	
	
main()
	
	