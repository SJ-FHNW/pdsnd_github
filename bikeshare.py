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
    city=input('Please select a city - data availiable for: Chicago, New York City or Washington:\n').lower()
    while city not in ['chicago','new york city','washington']:
        print('Typo? - Please try again!')
        city=input('Please select a city: Chicago, New York City or Washington:\n').lower()

    # get user input for month (all, january, february, ... , june)
    month=input('Is there a month you are interested in? Type in a month between January and June - or all (for all months):\n').lower()
    while month not in ['all','january','february','march','april','may','june']:
        print('Sorry - there is only data for January to June. Please try again.')
        month=input('Type in a month between January and June - or all (for all months):\n').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day=input('Great - any day you\'d like to see? - Please select one or type in all (for all days):\n').lower()
    while day not in ['all', 'monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
        print('Ups - please try again!')
        day=input('Please select a day (Monday to Sunday) or type in all (for all days):\n').lower()

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

    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['s_month']=df['Start Time'].dt.month_name()
    df['s_day']=df['Start Time'].dt.day_name()

    if month !='all':
        df= df[df['s_month'] == month.title()]
    if day != 'all':
        df= df[df['s_day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    mostcom_month=df['s_month'].mode()[0]
    print('Most common month:',mostcom_month)

    # display the most common day of week
    mostcom_day=df['s_day'].mode()[0]
    print('Most common weekday:',mostcom_day)

    # display the most common start hour
    df['s_hour']=df['Start Time'].dt.hour
    mostcom_hour=df['s_hour'].mode()[0]
    print('Most common starting hour for a trip:',mostcom_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mostcom_start=df['Start Station'].mode()[0]
    print('Most popular station for starting a trip:',mostcom_start)

    # display most commonly used end station
    mostcom_end=df['End Station'].mode()[0]
    print('Most popular station for ending a trip:',mostcom_end)

    # display most frequent combination of start station and end station trip
    df['trip']= df['Start Station'] + " - " + df['End Station']
    mostcom_trip=df['trip'].mode()[0]
    print('Most popular trip:',mostcom_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tot_travel=round(((df['Trip Duration'].sum()/60)/60),2)
    print('Total travel time (h):',tot_travel)

    # display mean travel time
    mean_travel=round((df['Trip Duration'].mean()/60),2)
    print('Average travel time (min):',mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_typ=df['User Type'].value_counts()
    print("\nNumer of different user types:\n", user_typ)

    # Display counts of gender
    user_gen=df['Gender'].value_counts()
    print("\nNumer of female and male users:\n", user_gen)

    # Display earliest, most recent, and most common year of birth
    user_min_by=round(df['Birth Year'].min())
    user_max_by=round(df['Birth Year'].max())
    user_mode_by=df['Birth Year'].mode()[0]
    print("\nYoungest User, born in:", user_max_by)
    print("\nOldest User, born in:", user_min_by)
    print("\nMost common year of birth:", user_mode_by)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_raw_data(df):
    """Not included in template - but mentioned in rubric:
    displays some raw data for city, month, day - always in blocks of 5 rows."""
    start_time = time.time()

    while True:
        show=input('\nWould you like to see some (more) raw data (Yes or No)?').lower()
        if show=='yes':
            for i in range(0,len(df),5):
                if show=='yes':
                    print(df[i:i+5])
                    show=input('\nWould you like to see some (more) raw data (Yes or No)?').lower()
        if show=='no':
            print('\nOk - no more raw data.')
            break
        else:
            print('\nTypo - try again.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)

        if city in['chicago','new york city']:
            user_stats(df)
        else:
            print('\nSorry - no user data for Washington.')

        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter Yes or No.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
