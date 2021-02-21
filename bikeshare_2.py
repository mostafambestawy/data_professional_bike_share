import time
import pandas as pd
import numpy as np


def sameLengthList(words):
    """
    makes all elements of a string array have same length by adding spaces
    for better GUI .
    """
    maxLength = max([len(word) for word in words])
    result = {}
    for word in words:
        result[word] = word+' '*(maxLength-len(word))
    return result


CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['monday', 'tuesday', 'wednesday',
        'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (int) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # getting user's input for a city
    allowedCities = [item[0] for item in CITY_DATA.items()]
    print('Hello! Let\'s explore some US bikeshare data!')
    # aligning cities
    alignedCities = sameLengthList(allowedCities)
    inputMessgae = 'which city you want to analyze its data?\ntype in:\n'\
        + alignedCities['chicago']+' for Chicago City\n'\
        + alignedCities['new york']+' for New York City\n'\
        + alignedCities['washington']+' for Washington D.C City\n'
    city = input(inputMessgae)
    while city not in allowedCities:
        city = input('Invalid City\n'+inputMessgae)

    # getting user's input for a month
    allowedMonths = MONTHS+['all']
    allowedInputs = ''
    for month in allowedMonths:
        allowedInputs = allowedInputs+month
        if month != allowedMonths[-1]:
            allowedInputs = allowedInputs+', '
    inputMessgae = 'which month you want to analyze its data?\nallowed inputs: ' + \
        allowedInputs+'\n'
    month = input(inputMessgae)
    while month not in allowedMonths:
        month = input('Invalid Month\n'+inputMessgae)

    # getting user's input for a day
    allowedDays = DAYS+['all']
    allowedInputs = ''
    for day in allowedDays:
        allowedInputs = allowedInputs+day
        if day != allowedDays[-1]:
            allowedInputs = allowedInputs+', '
    inputMessgae = 'which day of week you want to analyze its data?\nallowed inputs: '+allowedInputs+'\n'
    day = input(inputMessgae)
    while day not in allowedDays:
        day = input('Invalid Day\n'+inputMessgae)

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday
    
    #more efficent way:
    df_parse_dates=pd.read_csv("chicago.csv",parse_dates=['Start Time','End Time'])
    df_parse_dates['month'] = df_parse_dates['Start Time'].dt.month
    df_parse_dates['day']=df_parse_dates['Start Time'].dt.weekday

    


    if month != 'all':
        monthInt = MONTHS.index(month) + 1  # months are 1 based indexed
        df = df[df['month'] == monthInt]
    if day != 'all':
        dayInt = DAYS.index(day)  # days are 0 based indexed
        df = df[df['day'] == dayInt]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('the most common month is ' + str(MONTHS[df['month'].mode()[0]-1]))

    # display the most common day of week
    print('the most common day of week is ' + str(DAYS[df['day'].mode()[0]]))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('the most common start of hour is ' + str(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    display_sample_data(df)
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('the most common start station is ' +
          str(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('the most commonly used end station is ' +
          str(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    print('most frequent combination of start station and end station trip is:\nStart Staion--> ' +
          str((df['Start Station']+'\nEnd Station--> '+df['End Station']).mode()[0]))
    
    # more efficent way
    df=df[['Start Station','End Station']].dropna().groupby(['Start Station','End Station']).size().sort_values(ascending=False)
    startStation,endStation=df[df==df[0]].index[0]
    print('most frequent combination of start station and end station trip is:\nStart Staion--> ' +
          startStation+'\nEnd Station--> '+endStation)
    display_sample_data(df)
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('total travel time is '+str(df['Trip Duration'].sum()))

    # display mean travel time
    print('mean travel time is '+str(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    display_sample_data(df)
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    userCount = str(df['User Type'].value_counts())
    # remove not necessary data
    userCount = userCount[:userCount.index('Name:')]
    print('counts of user types:\n'+userCount+'\n')
    # Display counts of gender
    genderCount = str(df['Gender'].value_counts())
    genderCount = genderCount[:genderCount.index(
        'Name:')]  # remove not necessary data
    print('counts of gender:\n'+genderCount)

    # Display earliest, most recent, and most common year of birth
    print('the earlist year of birth '+str(int(df['Birth Year'].min())))
    print('the most recent year of birth '+str(int(df['Birth Year'].max())))
    print('the most common year of birth ' +
          str(int(df['Birth Year'].mode()[0])))
    print("\nThis took %s seconds." % (time.time() - start_time))
    display_sample_data(df)
    print('-'*40)


def display_sample_data(df):
    PAGE_SIZE = 5
    inputMessage = '\nWould you like to display '+str(PAGE_SIZE)+' rows of data? Type in:\nyes        --> for displaying '+str(
        PAGE_SIZE)+' rows\nany number --> for displaying other amount of rows\nany text   --> for exiting data displaying\n'
    display_answer = input(inputMessage)
    if display_answer.lower() != 'yes':
        try:
            PAGE_SIZE = int(display_answer)
            display_answer = 'yes'
        except:
            pass
    displayed_count = 0
    resuidal = len(df) % PAGE_SIZE
    while display_answer.lower() == 'yes':
        if displayed_count+PAGE_SIZE < len(df):
            total = len(df)-displayed_count-PAGE_SIZE
            print('\ndisplaying '+str(PAGE_SIZE)+' rows from total resuidal '+str(total) +
                  ' rows of data:\n'+str(df.iloc[displayed_count:displayed_count+PAGE_SIZE]))
            resuidal = len(df) % PAGE_SIZE
            displayed_count += PAGE_SIZE
            inputMessage = '\nWould you like to display '+str(PAGE_SIZE)+' rows of data? Type in:\nyes        --> for displaying '+str(
                PAGE_SIZE)+' rows\nany number --> for displaying other amount of rows\nany text   --> for exiting data displaying\n'
            display_answer = input(inputMessage)
            if display_answer.lower() != 'yes':
                try:
                    PAGE_SIZE = int(display_answer)
                    display_answer = 'yes'
                except:
                    pass
        else:
            print('\ndisplaying the last '+str(len(df)-displayed_count) +
                  ' row(s)\n'+str(df.iloc[displayed_count:]))
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        if city != 'washington':
            user_stats(df)
        display_sample_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
