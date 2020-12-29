import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while city.lower() not in CITY_DATA:
        city = input("Would you like to see data for Chicago, New York City, or Washington?\n").lower()
    
    # get user input for month (all, january, february, ... , june)
    while True:
        filter_by = input('Would you like to filter the data by month, day or not at all? Type "none" for no time filter.\n')
        if filter_by.lower().strip() == 'month':
            month = input('Which month? January, February, March, April, May, or June? Please type out the full month name.\n')
            day = None
            break
        # get user input for day of week (all, monday, tuesday, ... sunday)
        elif filter_by.lower().strip() == 'day':
            day = input('Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? Please type out the full day name.\n')
            month = None
            break
        elif filter_by.lower().strip() == 'none':
            month = None
            day = None
            break
        else:
            print('make sure your inputs are valid!\n')
            main()
            
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
    #load data
    df = pd.read_csv(CITY_DATA[city])
    
    #drop the unknown column that appears
    df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1,inplace=True)

    #convert the Date to datetime data type
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['Month'] = pd.DatetimeIndex(df['Start Time']).strftime('%B')
    df['Day_Of_Week'] = pd.DatetimeIndex(df['Start Time']).strftime('%A')

    # #check for duplicated values
    # if df.duplicated().sum() > 0:
    #     #delete duplicated values
    #     df.drop_duplicates(inplace=True)
        
    if month != None:
        # filter by month to create the new dataframe
        try:
            df = df[df['Month'] == month.title()]
        except:
            print("You didn't enter a valid month name!\n")
            main()

    # filter by day of week if applicable
    if day != None:
        try:
            # filter by day of week to create the new dataframe
            df = df[df['Day_Of_Week'] == day.title()]
        except:
            print("You didn't enter a valid day of week!\n")
            main()
    if day == None and month == None:
        try:
            # filter by all
            df = df
        except:
            pass



    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    try:
        print("The most common month is {} with the count of {}.\n".format(df['Month'].value_counts().index[0],
                                                                        df['Month'].value_counts().max()))
    except:
        pass

    # display the most common day of week
    try:
        print("The most common day of week is {} with the count of {}.\n".format(df['Day_Of_Week'].value_counts().index[0],
                                                                        df['Day_Of_Week'].value_counts().max()))
    except:
        pass
    
    # display the most common start hour
    try:
        print("The most common start hour is {}H with the count of {}.\n".format((pd.DatetimeIndex(df['Start Time']).hour).value_counts().index[0],
                                                                                 (pd.DatetimeIndex(df['Start Time']).hour).value_counts().max()))
    except:
        pass
    
    
    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    try:
        print("The most commonly used start station is {} with the count of {}.\n".format(df['Start Station'].value_counts().index[0],
                                                                        df['Start Station'].value_counts().max()))
    except:
        pass


    # display most commonly used end station
    try:
        print("The most commonly used end station is {} with the count of {}.\n".format(df['End Station'].value_counts().index[0],
                                                                        df['End Station'].value_counts().max()))
    except:
        pass



    # display most frequent combination of start station and end station trip
    try:
        print("The most frequent combination of start station and end station trip is {} with the count of {}.\n".format((df['Start Station']+" - "+df['End Station']).value_counts().index[0],
                                                                        (df['Start Station']+" - "+df['End Station']).value_counts().max()))
    except:
        pass

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # total travel time in seconds
    total_travel_time = df['Trip Duration'].sum()
    
    #travel time in days
    days = total_travel_time // 86400
    #remaining travel time in hours
    hours = (total_travel_time % 86400) // 3600
    
    #remaining travel time in minutes
    minutes = ((total_travel_time % 86400) % 3600) // 60
    
    #remaining travel time in seconds
    seconds = (((total_travel_time % 86400) % 3600) % 60) // 1
    print("The total travel time is {:.0f} days {:.0f} hours {:.0f} minutes {:.0f} seconds.\n".format(days,hours, minutes, seconds ))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].sum()/len(df['Trip Duration'])
    
    #travel time in days
    days_mean = mean_travel_time // 86400
    #remaining travel time in hours
    hours_mean = (mean_travel_time % 86400) // 3600
    
    #remaining travel time in minutes
    minutes_mean = ((mean_travel_time % 86400) % 3600) // 60
    
    #remaining travel time in seconds
    seconds_mean = (((mean_travel_time % 86400) % 3600) % 60) // 1
    
    print("The mean travel time is {:.0f} days {:.0f} hours {:.0f} minutes {:.0f} seconds.\n".format(days_mean,hours_mean, minutes_mean, seconds_mean ))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    try:
        usertype_count = df['User Type'].value_counts().to_frame()
        usertype_count.rename(columns={"User Type":"Count"}, inplace=True)
        usertype_count.index.name = "User Type"
        print(usertype_count)
    except:
        pass

    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts().to_frame()
        gender_count.rename(columns={"Gender":"Count"}, inplace=True)
        gender_count.index.name = "Gender"
        print("\n",gender_count)
    except:
        pass

    # Display earliest, most recent, and most common year of birth
    try:
        print("The earliest year of birth is {:.0f}.\n".format(df['Birth Year'].min()))
        print("The most recent year of birth is {:.0f}.\n".format(df['Birth Year'].max()))
        print("The most common year of birth is {:.0f} with the count of {}.\n".format(df['Birth Year'].value_counts().index[0],
                                                                        df['Birth Year'].value_counts().max()))
    except:
        pass


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        try:
            view_data = input("would you like to view the first ten rows of the data? (yes/no)")
            if view_data.lower() == "yes":
                print(df.head(10))
            else:
                pass
        except:
            pass
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
