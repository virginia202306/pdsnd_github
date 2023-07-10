#Please read firtst README#

import time
import pandas as pd
import numpy as np

#Please check that the data for the three cities are available.
CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

month_list = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
weekday_list = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

# function to validate user input
def check_user_input(user_input, input_type):
    while True:
        input_user_entered = input(user_input).lower()
        try:
            if input_user_entered in ['chicago', 'new york city', 'washington'] and input_type == 'c':
                break
            elif input_user_entered in month_list and input_type == 'm':
                break
            elif input_user_entered in weekday_list and input_type == 'd':
                break
            else:
                if input_type == 'c':
                    print('Invalid Input! Input must be: Chicago, New York City or Washington')
                if input_type == 'm':
                    print('Invalid Input! Input must be: January, February, March, April, May, June or all')
                if input_type == 'd':
                    print('Invalid Input! Input must be: Sunday, ...Friday, Saturday or all')
        except ValueError:
            print('Sorry, your input is wrong.')
    return input_user_entered

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bike share data!')


    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = check_user_input('Would you like to see the data for Chicago, New York City or Washington?\n', 'c')

    # get user input for month (all, january, february, ... , june)
    month = check_user_input('For filtering data by specific month please enter month name from (January, February, March, April, May, June) otherwise enter all\n', 'm')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = check_user_input('For filtering data by specific day please enter day name from (Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday) otherwise enter all\n', 'd')

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
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    #filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    #filter by day of week if applicable
    if day != 'all':
        days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        day = days.index(day) + 1

        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()
    print('Most Common Month is: ', most_common_month[0])

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()
    print('Most Common Day of Week is: ', most_common_day[0])


    # display the most common start hour
    most_common_hour = df['hour'].mode()
    print('Most common Start Hour of Day is: ', most_common_hour[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_commo_start_station = df['Start Station'].mode()
    print('Most Common Start Station is: ', most_commo_start_station)


    # display most commonly used end station
    most_commo_end_station = df['End Station'].mode()
    print('Most Common End Station is: ', most_commo_end_station)


    # display most frequent combination of start station and end station trip
    combination_group = df.groupby(['Start Station', 'End Station'])
    most_frequent_combination_station = combination_group.size().sort_values(ascending=False).head(1)
    print('Most frequent combination of Start Station and End Station trip is: ', most_frequent_combination_station)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time is: ', total_travel_time)


    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time is: ', mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bike share users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User Types in Data are: ', df['User Type'].value_counts())


    # Display counts of gender
    if city != 'Washington':
        if 'Gender' in df.columns:
            print('Counts of Gender: ', df['Gender'].value_counts())
        else:
            print('Unfortunately no Gender data are available.')

        # Display earliest, most recent, and most common year of birth

        if 'Birth Year' in df.columns:
            earliest_year = df['Birth Year'].min()
            print('Earliest Year is: ', earliest_year)

            most_recent_year = df['Birth Year'].max()
            print('Most recent Year is: ', most_recent_year)

            most_common_year = df['Birth Year'].mode()
            print('Most common Year is: ', most_common_year)

            print("\nThis took %s seconds." % (time.time() - start_time))
            print('-'*40)

        else:
            print('Unfortunately no Birth Year is available.')

#view raw data to user
def show_row_data(df):
    row=0
    while True:
        view_raw_data = input('Would you like to see the raw data? For Yes enter Y for No enter N. \n').lower()
        if view_raw_data == 'y':
            print(df.iloc[row : row + 11])
            row += 11
        elif view_raw_data == 'n':
            break
        else:
            print('Sorry! You entered wrong Input! Kindly try again!')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        show_row_data(df)
        restart = input('\nWould you like to restart? For Yes enter Y for No enter N. \n').lower()
        if restart.lower() != 'y':
            break
if __name__ == "__main__":
    main()