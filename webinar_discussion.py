from datetime import datetime
import time
import pandas as pd
import numpy as np
"""
this snippet is to prove that loading date using parse_dates parameter in read_csv()
is better than loading data as it is,then using  to_datetime conversion
on the behave of performance
"""

print("loading data frame using to_datetime")
start_time = time.time()
df=pd.read_csv("chicago.csv")
df['Start Time'] = pd.to_datetime(df['Start Time'])
df['day']=df['Start Time'].dt.weekday
print('the most common day of week is ' + str(df['day'].mode()[0]))
print("This took %s seconds." % (time.time() - start_time))


print("*"*20)


print("loading data frame using parse_dates")
start_time = time.time()
df_parse_dates=pd.read_csv("chicago.csv",parse_dates=['Start Time'])
df_parse_dates['day']=df_parse_dates['Start Time'].dt.weekday
print('the most common day of week is ' + str(df_parse_dates['day'].mode()[0]))
print("This took %s seconds." % (time.time() - start_time))


start_time = time.time()
df=pd.read_csv('chicago.csv')
df=df[['Start Station','End Station']].dropna().groupby(['Start Station','End Station']).size().sort_values(ascending=False)
startStation,endStation=df[df==df[0]].index[0]
print('most frequent combination of start station and end station trip is:\nStart Staion--> ' +
          startStation+'\nEnd Station--> '+endStation)
print('This took %s seconds.' % (time.time() - start_time))
print('*'*20)

start_time = time.time()
df=pd.read_csv('chicago.csv')
df=df[['Start Station','End Station']].dropna()
print('most frequent combination of start station and end station trip is:\nStart Staion--> ' +
          str((df['Start Station']+'\nEnd Station--> '+df['End Station']).mode()[0]))
print('This took %s seconds.' % (time.time() - start_time))

