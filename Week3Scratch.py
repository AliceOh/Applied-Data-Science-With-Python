
#Week 3 Assignment 3 - Pandas


#scratch pad begin
import pandas as pd
import numpy as np

#scratch pad end

#Assignment 3 - More Pandas
#Question 1 (20%)
import pandas as pd
import numpy as np
def get_Energy():
    energy = pd.read_excel('Energy Indicators.xls', na_values='...', header=None, parse_cols = "C:F", skiprows=18, skip_footer=38, names=['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'])
    energy['Energy Supply'] *= 1000000
    energy['Country'] = energy['Country'].str.replace('\d+', '') #remove digit, 'Switzerland17' should be 'Switzerland'.
    energy['Country'] = energy['Country'].str.replace('\s+\(+.*\)+', '') #remove parenthesis, 'Bolivia (Plurinational State of)' should be 'Bolivia', 
    dicts = {"Republic of Korea": "South Korea",
         "United States of America": "United States",
         "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
         "China, Hong Kong Special Administrative Region": "Hong Kong"}
    energy["Country"].replace(dicts, inplace=True)
    '''
    print (energy.info)
    print(energy.columns)
    print(energy.index)
    '''
    return energy
#print (get_energy())

def get_GDP():
    GDP = pd.read_csv('world_bank.csv', skiprows=4 )
    dicts = {"Korea, Rep.": "South Korea", 
             "Iran, Islamic Rep.": "Iran",
             "Hong Kong SAR, China": "Hong Kong"}
    GDP["Country Name"].replace(dicts, inplace=True)    
    GDP.rename(columns={'Country Name': 'Country'}, inplace = True)
    return GDP
#print (get_GDP())

def get_ScimEn():
    ScimEn= pd.read_excel('scimagojr.xlsx')
    return ScimEn
#get_ScimEn()

'''
def arrformat(arr):
    return '\n'.join(''.join( '{:15}'.format(e) for e in row) for row in arr)
res = []
res.append(['dataframe', 'Starts with', 'Ends with' ])
res.append(['-'*10, '-'*10, '-'*10 ])
res.append(['energy', get_energy()['Country'].iloc[0], get_energy()['Country'].iloc[-1]])
res.append(['GDP', get_GDP()['Country'].iloc[0], get_GDP()['Country'].iloc[-1]])
res.append(['ScimEn', get_ScimEn()['Country'].iloc[0], get_ScimEn()['Country'].iloc[-1]])

print(arrformat(res))
'''

def answer_one():
  Energy = get_Energy().set_index('Country')
  GDP = get_GDP().set_index('Country').loc[:, '2006':'2015']
  ScimEn = get_ScimEn().head(15).set_index('Country')
  
  mergedDF = pd.merge(ScimEn, Energy, how='inner', left_index=True, right_index=True)
  mergedDF = pd.merge(mergedDF, GDP, how='inner', left_index=True, right_index=True)
  '''
  print (mergedDF.info)
  print (mergedDF.columns)
  print (mergedDF.index)  
  '''
  return mergedDF
#answer_one()

#Question 2 (6.6%) The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
def answer_two():
  Energy = get_Energy().set_index('Country')
  GDP = get_GDP().set_index('Country')
  ScimEn = get_ScimEn().set_index('Country')
  GDPlen = len(GDP)
  Energylen = len(Energy)
  sciLen = len(ScimEn)

  union = pd.merge(GDP, Energy, how='outer', left_index=True, right_index=True)
  union = pd.merge(union, ScimEn, how='outer', left_index=True, right_index=True)

  union_count = len(union)
  #print ('union',  union_count)
  
  mergedDF = pd.merge(GDP, Energy, how='inner', left_index=True, right_index=True)
  mergedDF = pd.merge(mergedDF, ScimEn, how='inner', left_index=True, right_index=True)
  intersection_count = len(mergedDF)
  #print ('intersection_count', intersection_count)

  return union_count - intersection_count

#print (answer_two())

#Question 3 (6.6%): What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
#This function should return a Series named avgGDP with 15 countries and their average GDP sorted in descending order.
def answer_three():
    Top15 = answer_one()
    avgGDP = Top15[[str(year) for year in range(2006, 2016)]].mean(axis=1)
    avgGDP.sort_values(ascending=False, inplace=True)
    return avgGDP

#print (answer_three())

#Question 4 (6.6%): By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
#This function should return a single number.
def answer_four():
    Top15 = answer_one()
    avgGDP = Top15[[str(year) for year in range(2006, 2016)]].mean(axis=1)
    avgGDP.sort_values(ascending=False, inplace=True)
    a = Top15.loc[avgGDP.index[5]].loc['2006':'2015']
    print (a)
    b = a['2015']-a['2006']
    return  b
#print (answer_four())

#Question 5 (6.6%): What is the mean Energy Supply per Capita?
#This function should return a single number.
def answer_five():
    Top15 = answer_one()
    return  Top15['Energy Supply per Capita'].mean()
#print (answer_five())

#Question 6 (6.6%): What country has the maximum % Renewable and what is the percentage?
#This function should return a tuple with the name of the country and the percentage.
def answer_six():
    Top15 = answer_one()
    Top15.sort_values(['% Renewable'], ascending=False, inplace=True)
    countryName = Top15.index[0];
    per = Top15.iloc[0]['% Renewable']    
    return (countryName, per)
#print (answer_six())

#Question 7 (6.6%): Create a new column that is the ratio of Self-Citations to Total Citations. What is the maximum value for this new column, and what country has the highest ratio?
#This function should return a tuple with the name of the country and the ratio.
def answer_seven():
    Top15 = answer_one()
    Top15['Ratio-C'] = Top15['Self-citations']/Top15['Citations']
    Top15.sort_values(['Ratio-C'], ascending=False, inplace=True)
    countryName = Top15.index[0];
    per = Top15.iloc[0]['Ratio-C']    
    return (countryName, per)
#print (answer_seven())


#Question 8 (6.6%): Create a column that estimates the population using Energy Supply and Energy Supply per capita. What is the third most populous country according to this estimate?
#This function should return a single string value
def answer_eight():
    Top15 = answer_one()
    #print (Top15.columns)
    Top15['PopulationEnergy'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']
    Top15.sort_values(['PopulationEnergy'], ascending=False, inplace=True)
    #print (Top15.head())
    countryName = Top15.index[2];
    return countryName
#print (answer_eight())

#Question 9 (6.6%): Create a column that estimates the number of citable documents per person. What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the .corr() method, (Pearson's correlation).
#This function should return a single number.
def answer_nine():
    Top15 = answer_one()
    Top15['PopulationEnergy'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopulationEnergy']

    return Top15['Citable docs per Capita'].corr(Top15['Energy Supply per Capita'])
#print (answer_nine())


#Question 10 (6.6%):Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
#This function should return a series named HighRenew whose index is the country name sorted in ascending order of rank.

def answer_ten():
    Top15 = answer_one()
    medianRenew = Top15['% Renewable'].median()

    def decideValue(x):
        retValue = 0;
        if(x>=medianRenew):
           retValue = 1;
        return retValue
    
    HighRenew = Top15['% Renewable'].map(decideValue)
    return HighRenew
# print (answer_ten())


#Question 11 (6.6%): Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
#This function should return a DataFrame with index named Continent ['Asia', 'Australia', 'Europe', 'North America', 'South America'] and columns ['size', 'sum', 'mean', 'std']
ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}

def answer_eleven():
    Top15 = answer_one()
    Top15['PopulationEnergy'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']
    Top15['Continent'] = Top15.index.map(lambda x: ContinentDict[x])
    
    group = Top15.groupby('Continent')
    return pd.DataFrame({"size": group.count()["2010"],
			     "sum": group['PopulationEnergy'].sum(),
			     "mean": group['PopulationEnergy'].mean(),
			     "std": group['PopulationEnergy'].std()})
#print (answer_eleven())

#Question 12 (6.6%): Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
#This function should return a Series with a MultiIndex of Continent, then the bins for % Renewable. Do not include groups with no countries.
def answer_twelve():
    Top15 = answer_one()
    Top15['Continent'] = Top15.index.map(lambda x: ContinentDict[x])
    
    group = Top15.groupby(['Continent',
			  pd.cut(Top15['% Renewable'], 5,
			  labels=["bin{0}".format(bin) for bin in range(5)])])
    s = group['2010'].count()    
    return s
#print (answer_twelve())

#Question 13 (6.6%) Convert the Population Estimate series to a string with thousands separator (using commas). Do not round the results.
# e.g. 317615384.61538464 -> 317,615,384.61538464
# This function should return a Series PopEst whose index is the country name and whose values are the population estimate string.
def answer_thirteen():
    Top15 = answer_one()
    Top15['PopulationEnergy'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']
    return Top15['PopulationEnergy'].map(lambda x: "{0:,}".format(x))
print (answer_thirteen())

