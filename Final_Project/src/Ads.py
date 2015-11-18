# Miriam Baumann, 2015-11-16
# This script loads two excel dataframes, cleans and merges them , and then outputs a
# figure with two subplots showing the relationship between cost of ads and
# Sales to New customers/ Number of New customers. The plots are analyzed using 
# regression analysis and show a linear regression line. 

# Importing Libraries
import pandas as pd
import xlsxwriter
import numpy as np
import sys
import statsmodels.api as sm
import matplotlib.pyplot as plt
import csv

#Defining the variables
Salesdf = sys.argv[1]
sheetname1 = sys.argv[2]

Adsdf = sys.argv[3]
sheetname2 = sys.argv[4]

savename = sys.argv[5]

def main():
	# Uses the load_data function to load the first dataframe into a variable
	Salesdata = load_data (dataframe = Salesdf, sheetname = sheetname1)
	# Uses the load_data function to load the second dataframe into a variable
	Adsdata = load_data (dataframe = Adsdf, sheetname = sheetname2)
	#Uses the merging_data function to merge the two dataframes previously loaded
	Combineddata = merging_data(Salesdata, Adsdata)
	#Uses the lm function to print the linear regression analysis results of the merged data of 2 columns 
	Summary = lm(Combineddata.Ad_Cost, Combineddata.Sales_in_CAD, Combineddata)
	print(Summary)
	#Uses the plot_lm function to plot the linear regression line of the first subplot
	Plotlm = plot_lm(Combineddata.Ad_Cost, Combineddata.Sales_in_CAD)
	# Uses the plot function to create a plot of the data
	plotting = plot(Combineddata.Ad_Cost, Combineddata.Sales_in_CAD, Combineddata.New_or_Returning, plotname = savename)
	print(plotting)
	#Uses the lm function to print the linear regression analysis results of the merged data of 2 different columns 
	Summary1 = lm(Combineddata.Ad_Cost, Combineddata.New_or_Returning, Combineddata)
	print(Summary1)
	#Uses the plot_lm function to plot the linear regression line of the second subplot
	Plotlm1 = plot_lm(Combineddata.Ad_Cost, Combineddata.New_or_Returning)
	

def load_data (dataframe, sheetname):
    '''This function loads an excel dataframe in a specified sheet'''
    #Loads the excel data using pandas 
    data = pd.read_excel(dataframe, sheetname)
    
    #Returning the data
    return data
	
	
def merging_data(dataframe1, dataframe2):
	'''This function merges the two dataframes that were loaded with the load data function.
	Before merging the data, this function cleans and organizes the two dataframes. The date columns
	in both dataframes are resampled to month, and set as the index so that they can be merged by Date.'''
    
	# Renaming the columns 
	dataframe1.columns = [['Exchange_Rate', 'Customer', 'Field', 'Date_of_Order', 'Total_Sales', 'Year_of_First_Order', 'New_or_Returning']]
    # Replacing the empty values in the Exchange Rate column with 1 and setting the index to Date_of_Order
	Sales_df= dataframe1[['Exchange_Rate', 'Customer', 'Field', 'Date_of_Order', 'Total_Sales', 'Year_of_First_Order', 'New_or_Returning']].replace([None], [1]).set_index('Date_of_Order')
    # Creating a new column in the data set, which puts all sales amounts in Canadian dollars. 
	Sales_df['Sales_in_CAD'] = Sales_df['Exchange_Rate'] * Sales_df['Total_Sales']
	
	# All rows with dates equal to and under 2013-07-31 will be deleted.
	Change_New = Sales_df[Sales_df.index > '2013-07-31'].reset_index()
	# Deleting all rows of sales from returning customers, to obtain Sales only from new customers. 
	Change1_New = Change_New.groupby(['New_or_Returning']).get_group('New')
	# Grabbing 3 columns from the dataset and setting the index to Date of order.
	Resampled_ind = Change1_New[['Date_of_Order', 'Sales_in_CAD', 'New_or_Returning']].set_index('Date_of_Order')
	# Replacing the 'New' string with the number 1 so that they can be added later.
	# And data is downsampled to month, taking the sum of the Sales and the new customers in each month. 
	Index_Month= Resampled_ind[['New_or_Returning', 'Sales_in_CAD']].replace(['New'], [1]).resample('M', how=('sum')) 
	
	# Setting the index to Date
	Ads_df = dataframe2.set_index('Date')
	# Renaming the columns
	Ads_df.columns = [['Ad_Cost']]
	# Resampling the date column, so that the month is synonymous with the other table 
	Ads1_df = Ads_df.resample('M', how=('sum'))
    
	# Now the two dataframes will be combined:
	# Combining the two dataframes by the date of order, and resetting the index.
	Combined_df = pd.concat([Index_Month, Ads1_df], axis=1, join_axes=[Index_Month.index]).reset_index()
    
	return Combined_df
	
	
def lm (x, y, data):
	'''This function calculates the linear regression of a scatter plot, where the 
	independent input variable is x and the dependant input variable is y.
	This function will print a summary of the results in a table.'''
    # Running linear regression on the plot 
	lm = sm.formula.ols(formula = 'y ~ x', data = data).fit()
	# generating a new data frame of the x variable, to produce a list of numbers from 1 to the same length as the x variable
	x_new = pd.DataFrame({'newdata' : range(1,len(x)+1)})
    # using the predict function to predict the y values based on x
	y_preds = lm.predict(x_new)
	
	# printing the summary of the linear model
	print(lm.summary())

	


def plot_lm (x, y):
    '''This function plots the linear regression line of a given scatter plot,
    where x is the depedant variable and y is the independant vairable.'''
    # Adds a column of ones as long as the x column, which will allow the calculation of the intercept
    X = sm.add_constant(x)
    # Creates a linear model of the scatter plot 
    lm = sm.formula.OLS(y, X).fit()
    # Predicts the x values from x min to x max, using 24 different values 
    x_pred= np.linspace(x.min(),x.max(), 24)
    # Adds the column of ones previously created to the x value predictions
    x_pred2 = sm.add_constant(x_pred)
    # Predicts the y values, based on the x value predictions
    y_preds = lm.predict(x_pred2)
    
    # Plots the linear regression line using the predicted x values and the predicted y values
    plt.plot(x_pred, y_preds, color='k', linewidth = 2)
    
    return plt.plot()	
	

def plot(x, y, z, plotname):
	'''This function will make 2 scatter plots, taking in data from three columns of a dataframe.
	The produced figure will be saved to a filename specified by the user in the input'''
    #Defining the size of the figure
	plt.figure(figsize=(13,5))
	#Defining an overarching title
	plt.suptitle('Relationship between Cost of Ads and Sales to New Customers/ Number of New Customers', fontsize=14)
    
	#Making the first subplot
	plt.subplot(1,2,1)
    # Creating a scatter plot from the dataframe
	plt.scatter(x, y)
    # Defining the y axis label
	plt.ylabel('Sales to New Customers (CAD)')
    # Defining the x-axis label 
	plt.xlabel(x.name)
	plot_lm(x, y)
    
    # Making the second subplot
	plt.subplot(1,2,2)
	plt.scatter(x, z)
    # Defining the y axis label
	plt.ylabel('Number of New Customers')
    # Defining the x-axis label 
	plt.xlabel(x.name)
    # Adding the linear model function, to plot the regression line on the plot
	plot_lm(x, z)
    
    #Saving the plot to a new file 
	plt.savefig(plotname)

main()