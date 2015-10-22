# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 22:47:07 2015

@author: WangZiyan
"""

import pandas as pd
import os
import csv
from time import strptime


"""
Functions
"""

def read_clean_index_data(file_name):
    """ read csv file as raw input, add one column for date, 
        remove useless rows and columns """
    
    date = ''   # record date
    file_list = []
    header = []
    is_index_data = False
    
    with open(file_name, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == 'Time Interval':   # it is header of index data
                header = row
                header.insert(0, 'Date')
                del header[-1]
                is_index_data = True
                continue
            if is_index_data:
                if row[0] == 'Summary':
                    continue
                if row[1] == '':    # adjust date format
                    day = row[0][0:2]
                    if day[0] == '0':
                        day = day[1]
                    mon = str(strptime(row[0][2:5],'%b').tm_mon)
                    year = row[0][5:9]
                    date = mon + '/' + day + '/' + year
                    continue
                row.insert(0, date)
                del row[-1]     # last element is volume which is N.A.
                file_list.append(row)    
            else:   # is exchange rate data
                if row[0] in ['Security', 'Start Date', 'End Date', 'Period', \
                              'Pricing Source', '']:
                    continue
                if row[0] == 'Date':
                    header = row
                    header[1] = 'ExRate'
                    continue
                file_list.append(row)
        
        df = pd.DataFrame(file_list, columns = header)
    return df



def change_currency(price_df, exrate_df):
    """ change pricing currency from local to USD """
    
    price1 = price_df
#    dates = list(set(price1.Date))
#    for date in dates:
    for i in range(len(price1)):
        try:
            today = price1.Date.iloc[i]
            today_exrate = exrate_df[exrate_df.Date==today].ExRate.iloc[0]
            local_price = price1.Close.iloc[i]
            price1.Close.iloc[i] = float(local_price) / float(today_exrate)
        except:
            print(i)
    
    
    return price1


#def realized_vol()



"""
Main
"""


if __name__ == '__main__':
#    # get all files in current directory
#    files = [f for f in os.listdir('.') if \
#             os.path.isfile(f) and f.endswith('.csv')]
#             
#    data = {}
#    
#    for file1 in files:
#        file_name = file1.split('_')[0]
#        data[file_name] = read_clean_index_data(file1)
#        
#        # output
#        data[file_name].to_csv('./clean_data/' + file_name+'.csv', index=False)

    
    new_df = change_currency(data['STI'], data['USDSGD'])