
#Assignment 2 - Pandas Introduction

"""
#scratch pad
import pandas as pd
#animals = ['Tiger', 'Bear', 'Moose']
#print (pd.Series(animals))
purchase_1 = pd.Series({'Name': 'Chris',
                        'Item Purchased': 'Dog Food',
                        'Cost': 22.50})
purchase_2 = pd.Series({'Name': 'Kevyn',
                        'Item Purchased': 'Kitty Litter',
                        'Cost': 2.50})
purchase_3 = pd.Series({'Name': 'Vinod',
                        'Item Purchased': 'Bird Seed',
                        'Cost': 5.00})

df = pd.DataFrame([purchase_1, purchase_2, purchase_3], index=['Store 1', 'Store 1', 'Store 2'])
#print (df['Item Purchased'])

seriP  = df['Item Purchased']
print (type(seriP))
print (seriP)
list = []
for label, value in seriP.iteritems():
    list.append(value)
print (list)

df['Cost'] *= 0.8
print(df)

print (df[(df['Cost'] > 3)])
print (df['Name'][(df['Cost'] > 3)])

df = df.set_index([df.index, 'Name'])
df.index.names = ['Location', 'Name']
df = df.append(pd.Series(data={'Cost': 3.00, 'Item Purchased': 'Kitty Food'}, name=('Store 2', 'Kevyn')))
print (df)
"""

"""
#Part 1
import pandas as pd
df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')
#print (df.head())
"""
"""
#Question 1: Which country has won the most gold medals in summer games?
#This function should return a single string value.
def answer_one():
    df['country'] = df.index
    df_copy = df.set_index('Gold')
    df_copy = df_copy.sort_index(ascending=False)    
    #print (df_copy.head())
    return df_copy.iloc[0]['country']
print (answer_one())
"""
"""
#Question 2: Which country had the biggest difference between their summer and winter gold medal counts? This function should return a single string value.
def answer_two():
    df['country'] = df.index
    df_copy = df.set_index(df['Gold']-df['Gold.1'])
    df_copy = df_copy.sort_index(ascending=False)
    return df_copy.iloc[0]['country']

print (answer_two())
"""
"""
#Question 3: Which country has the biggest difference between their summer gold medal counts and winter gold medal counts relative to their total gold medal count? 
#Only include countries that have won at least 1 gold in both summer and winter. This function should return a single string value.

def answer_three():
    df['country'] = df.index
    only_gold = df[(df['Gold.1'] > 0) & (df['Gold'] > 0)]
    only_gold = only_gold.set_index((only_gold['Gold']-only_gold['Gold.1'])/only_gold['Gold.2'])
    only_gold = only_gold.sort_index(ascending=False)
    return only_gold.iloc[0]['country']

print (answer_three())
"""
"""
#Question 4: Write a function that creates a Series called "Points" which is a weighted value where each gold medal (Gold.2) counts for 3 points, silver medals (Silver.2) for 2 points, and bronze medals (Bronze.2) for 1 point. The function should return only the column (a Series object) which you created.
#This function should return a Series named Points of length 146
def answer_four():    
    for index, row in df.iterrows():
        df['points'] = (df['Gold.2']*3 + df['Silver.2']*2 + df['Bronze.2'])
    Points  = df['points']
    return Points

print (answer_four())
"""

#Part 2
import pandas as pd
import operator
import numpy as np
census_df = pd.read_csv('census.csv')

#print (census_df.head())
"""
#Question 5: Which state has the most counties in it? (hint: consider the sumlevel key carefully! You'll need this for future questions too...). This function should return a single string value.
def answer_five():
    country_df=census_df[census_df['SUMLEV'] == 50]
    maxCounter = 0
    maxState = ''
    for stateValue in country_df['STATE'].unique():
        temp_df = country_df[country_df['STATE']==stateValue]
        counter = len(temp_df.index)
        #print ('counter = ',  counter)
        if(counter>maxCounter):
            maxCounter = counter
            maxState = temp_df.iloc[0]['STNAME']
    #print ('maxCounter = ', maxCounter)
    #print ('maxState = ', maxState)
    return maxState

print (answer_five())
"""
"""
#Question 6: Only looking at the three most populous counties for each state,
#what are the three most populous states (in order of highest population to
#lowest population)?  Use CENSUS2010POP.  This function should return a list of
#string values.
def answer_six():
    country_df = census_df[census_df['SUMLEV'] == 50]
    statesFirstThreePopulation = [1,2,3]
    mostPopulousStates = ['A','B','C']
    for stateValue in country_df['STATE'].unique():
        temp_df = country_df[country_df['STATE'] == stateValue]
        temp_df = temp_df.set_index('CENSUS2010POP')        
        temp_df = temp_df.sort_index(ascending=False)
        temp_df = temp_df.reset_index()
        rowCounter = len(temp_df.index)
        if(rowCounter>=3):
            statePopulation = temp_df.iloc[0]['CENSUS2010POP'] + temp_df.iloc[1]['CENSUS2010POP'] + temp_df.iloc[2]['CENSUS2010POP']
        elif(rowCounter==2):
            statePopulation = temp_df.iloc[0]['CENSUS2010POP'] + temp_df.iloc[1]['CENSUS2010POP']
        elif(rowCounter==1):
            statePopulation = temp_df.iloc[0]['CENSUS2010POP']
        else:
            print ('Error rowCounter')
        
        #print ('statePopulation = ',  statePopulation)
        
        if(statePopulation > statesFirstThreePopulation[2]):#larger than the smallest population in first 3 states
            #print (mostPopulousStates)
            #print (statesFirstThreePopulation)
            mostPopulousStates[2] = (temp_df.iloc[0]['STNAME'])
            statesFirstThreePopulation[2] = statePopulation            
            d = dict(zip(statesFirstThreePopulation, mostPopulousStates))
            #print (d)
            sorted_d = sorted(d.items(), key=lambda x: x[0], reverse=True)#sort by key which is population
            #print (sorted_d)
            index=0
            for i in(sorted_d):
                statesFirstThreePopulation[index] = i[0]
                mostPopulousStates[index] = i[1]
                index += 1       
            #print ('After sorting')
            #print (mostPopulousStates)
            #print (statesFirstThreePopulation)
    return mostPopulousStates

print(answer_six())
"""
"""
#Question 7: Which county has had the largest absolute change in population within the period 2010-2015? (Hint: population values are stored in columns POPESTIMATE2010 through POPESTIMATE2015, you need to consider all six columns.)
#e.g. If County Population in the 5 year period is 100, 120, 80, 105, 100, 130, then its largest change in the period would be |130-80| = 50.
#This function should return a single string value.

def answer_seven():
    country_df = census_df[census_df['SUMLEV'] == 50]
    largestChange = 0
    largestChangeCountry = 'A'
    changeValueList = []
    for index, row in country_df.iterrows():
        changeValueList = []
        changeValueList.append(row['POPESTIMATE2010'])
        changeValueList.append(row['POPESTIMATE2011'])
        changeValueList.append(row['POPESTIMATE2012'])
        changeValueList.append(row['POPESTIMATE2013'])
        changeValueList.append(row['POPESTIMATE2014'])
        changeValueList.append(row['POPESTIMATE2015'])
        #print (changeValueList)
        a = np.array(changeValueList)
        change = a.max()-a.min()
      
        if(change>largestChange):
            largestChange = change
            largestChangeCountry = row['CTYNAME']            
    return largestChangeCountry

print(answer_seven())
"""
#Question 8: In this datafile, the United States is broken up into four regions using the "REGION" column. 
#Create a query that finds the counties that belong to regions 1 or 2, whose name starts with 'Washington', and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014.
#This function should return a 5x2 DataFrame with the columns = ['STNAME', 'CTYNAME'] and the same index ID as the census_df (sorted ascending by index).
def answer_eight():
    country_df = census_df[((census_df['REGION'] == 1) | (census_df['REGION'] == 2)) & (census_df['POPESTIMATE2015']>census_df['POPESTIMATE2014'])]
    columns_to_keep = ['STNAME',
                   'CTYNAME']
    country_df = country_df[columns_to_keep]
    for index, row in country_df.iterrows():
        if(row['CTYNAME'].startswith("Washington")==False):
            country_df = country_df.drop(index)

    return country_df

print(answer_eight())
