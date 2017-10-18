
#Week 4 Assignment 4 - Hypothesis Testing


import pandas as pd
import numpy as np
#pd.show_versions(as_json=False)

from scipy.stats import ttest_ind
import re

HOUSING_DATA = "City_Zhvi_AllHomes.csv"



def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''

    state_substring = "[edit]"
    state_split = "["
    region_split = " ("
    columns = ["State", "RegionName"]
    state = ''
    lines = []
    with open('university_towns.txt') as univFile:
        for line in univFile:
            if state_substring in line:
                state = line.split(state_split)[0].strip()
            else:
                region = line.split(region_split)[0].strip()
                lines.append([state, region])
        
    data = pd.DataFrame(lines, columns=columns)
    #print (data.head())
    return data

#print (get_list_of_university_towns().head())

def get_GDP_data():
    columns = ["Year", "Annual GDP Current Billions",
	       "Annual GDP 2009 Billions", "to_delete", "YearQuarter",
	       "Quarterly GDP Current Billions", "Quarterly GDP 2009 Billions",
	       "to_delete"]
    first_quarter = "2000q1"
    delete_columns = "to_delete"
    
    GDPdata = pd.read_excel('gdplev.xls', skiprows=8, names=columns)
    GDPdata = GDPdata.drop(delete_columns, axis=1)
    GDPdata = GDPdata.iloc[GDPdata[GDPdata['YearQuarter']==first_quarter].index[0]:] #from required quarter
    #print (GDPdata.head())
    return GDPdata

def recession_start_index(data):
    for index, gdp in enumerate(data['Quarterly GDP 2009 Billions']):
        next_gdp = data['Quarterly GDP 2009 Billions'].iloc[index + 1]
        previous_gdp = data['Quarterly GDP 2009 Billions'].iloc[index - 1]
        if (index != 0 and (previous_gdp>gdp) and (gdp>next_gdp)):
            return index

def recession_end_index(data):
    for index, gdp in enumerate(data['Quarterly GDP 2009 Billions']):
        next_gdp = data['Quarterly GDP 2009 Billions'].iloc[index + 1]
        previous_gdp = data['Quarterly GDP 2009 Billions'].iloc[index - 1]
        if (index != 0 and (previous_gdp<gdp) and (gdp<next_gdp)):
            return index+1

def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    data = get_GDP_data()    
    index = recession_start_index(data)
    return data['YearQuarter'].iloc[index]

#print (get_recession_start())

def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    data = get_GDP_data()
    index = recession_start_index(data)
    data = data.iloc[index:] #from recession start quarter
    index = recession_end_index(data)
    return data['YearQuarter'].iloc[index]

#print (get_recession_end())


def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    data = get_GDP_data()
    startIndex = recession_start_index(data)
    tempdata = data.iloc[startIndex:] #from recession start quarter
    endIndex = recession_end_index(tempdata)+startIndex
    #print ('startIndex = ', startIndex)
    #print ('endIndex = ', endIndex)
    data = data.iloc[startIndex:endIndex]
    #print (data)
    return data['YearQuarter'].loc[data['Quarterly GDP 2009 Billions'].argmin()]

#print (get_recession_bottom())

def convert_quarters(data):
    year_month_pattern = re.compile("20\d\d-\d\d")
    years = ["20{0:02d}".format(year) for year in range(17)]
    quarters = [re.compile("|".join(["{0:02d}".format(month) for month in range(start, start+3)])) for start in range(1, 11, 3)]

    all_years = data.select(lambda x: year_month_pattern.match(x), axis=1)
    means = {}
    for year_label in years:
        year = all_years.select(lambda x: re.search(year_label, x), axis=1)
        for index, quarter_regex in enumerate(quarters):
            quarter = year.select(lambda x: quarter_regex.search(x), axis=1)
            means["{0}q{1}".format(year_label, index+1)] = quarter.mean(axis=1)
    return pd.DataFrame(means).dropna(axis="columns", how="all")


def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
    
    housedata = pd.read_csv('City_Zhvi_AllHomes.csv')
    housedata['State'] = housedata['State'].map(lambda x: states[x])
    tuples = [housedata['State'], housedata['RegionName']]
    multi_index = pd.MultiIndex.from_tuples(list(zip(*tuples)),	names=["State", "RegionName"])
    quarters = convert_quarters(housedata)    
    housedata = quarters.set_index(multi_index)
    
    return housedata

#print (convert_housing_data_to_quarters().head())


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    threshold = 0.01
    university_town = "university town"
    non_university_town = "non-university town"

    university_data = get_list_of_university_towns()
    data = get_GDP_data()
    index = recession_start_index(data)-1
    recession_start = data['YearQuarter'].iloc[index]
    recession_bottom = get_recession_bottom()
    housing_data = convert_housing_data_to_quarters()

    price_ratios = housing_data[recession_start].div(housing_data[recession_bottom])
    price_ratios = pd.DataFrame({'PriceRatio': price_ratios})
    price_ratios.reset_index(inplace=True)
    #print (price_ratios.head())

    university_price_ratios = pd.merge(price_ratios, university_data, how='inner', on=["State", "RegionName"])
    university_price_ratios.dropna(inplace=True)
    #print (university_price_ratios.head())

    university_towns = (price_ratios['State'].isin(university_price_ratios['State']) & (price_ratios['RegionName'].isin(university_price_ratios['RegionName'])))    
    non_university_price_ratios = price_ratios[~university_towns]
    non_university_price_ratios = non_university_price_ratios.dropna()
    #print (non_university_price_ratios.head())
    t_statistic, p_value = ttest_ind(university_price_ratios['PriceRatio'].values, non_university_price_ratios['PriceRatio'].values)
    better = (university_town if university_price_ratios['PriceRatio'].mean() < non_university_price_ratios['PriceRatio'].mean() else non_university_town)

    different = p_value < threshold
    return (different, p_value, better)

print (run_ttest())

# test output type (different, p, better)

res = run_ttest()
print('Type test:', 'Passed' if type(
    res) == tuple else 'Failed')
print('test `better` item type:','Passed' if type(res[0]) == bool or type(res[0]) == np.bool_ else 'Failed' )
print('`p` item type test:', 'Passed' if type(
    res[1]) == np.float64 else 'Failed')
print('`different` item type test:',
      'Passed' if type(res[2]) == str else 'Failed')
print('`different` item spelling test:', 'Passed' if res[2] in [
      "university town", "non-university town"] else 'Failed')
