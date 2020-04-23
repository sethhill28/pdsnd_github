import time
import pandas as pd
import numpy as np
from scipy import stats


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }



MONTH_LIST = ['january',
              'february',
              'march',
             'april',
             'may',
             'june',
             'all']

DAYS_LIST = ['monday',
              'tuesday',
              'wednesday',
             'thursday',
             'friday',
             'saturday',
            'sunday',
            'all']

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
    try:
        city = input('Would you like to analyze data from Chicago, New York City, or Washington?').lower()
        while city not in CITY_DATA:
            print('Seems like there was a typo, please check your spelling')
            city = input('Would you like to analyze data from Chicago, New York City, or Washington?')

        print('you chose: ', city)


        # get user input for month (all, january, february, ... , june)
        month = input('Which month you would like to analyse from january to june? Or do you want to analyze all of them?').lower()
        while month not in MONTH_LIST:
            print('Seems like there was a typo, please check your spelling!')
            month = input('Which month you would like to analyse from january to june? Or simply all of them?')

        print('you chose: ', month)




    # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input("Please select a day you would like to analyze, or input 'all' for all of them-").lower()
        while day not in DAYS_LIST:
            print('Seems like there was a typo, please check your spelling')
            day = input("Please select a day you would like to analyze, or input 'all' for all of them")

        print('you chose: ', day)

        return city, month, day
    except Exception as e:
        print('There was an error with your inputs: {}'.format(e))
    print('-'*40)




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
    try:
        df = pd.read_csv(CITY_DATA[city])

        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['End Time'] = pd.to_datetime(df['End Time'])
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.weekday_name
        df['hour'] = df['Start Time'].dt.hour

        # filter by month if applicable
        if month != 'all':
        # use the index of the months list to get the corresponding int
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            month = MONTH_LIST.index(month) + 1

            # filter by month to create the new dataframe
            df = df[df['month'] == month]

    # filter by day of week if applicable
        if day != 'all':
            # filter by day of week to create the new dataframe
            df = df[df['day_of_week'] == day.title()]
        return df
    except Exception as e:
        print('Error occurred, could not load the file: {}'.format(e))

def time_stats(df, city):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    try:
        pop_month_num = df['Start Time'].dt.month.mode()[0]
        pop_month = MONTH_LIST[pop_month_num-1].title()
        print('The most popular month in', city, 'is:', pop_month)
    except Exception as e:
        print('Error occurred, could not calculate the most common month: {}'.format(e))

    # display the most common day of week
    try:
        pop_day_of_week = df['day_of_week'].mode()[0]
        print('The most popular weekday in', city, 'is:',pop_day_of_week)
    except Exception as e:
        print('Error occurred, could not calculate the most common day of week: {}'.format(e))


    # display the most common start hour
    try:
        pop_start_hour = df['hour'].mode()[0]
        print('The most popular starting hour in', city, 'is:',pop_start_hour)
    except Exception as e:
        print('Error occurred, Could not calculate the most common start hour: {}'.format(e))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df, city):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most common start station
    try:
        pop_start_station = df['Start Station'].mode()[0]
        pop_start_station_amount = df['Start Station'].value_counts()[0]
        print('The most popular start station in', city, 'is:',pop_start_station, 'and was used', pop_start_station_amount, 'times.')
    except Exception as e:
        print('Error occurred, could not calculate the most used start station: {}'.format(e))
    #display most common end station
    try:
        pop_end_station = df['End Station'].mode()[0]
        pop_end_station_amount = df['End Station'].value_counts()[0]
        print('The most popular end station in', city, 'is:',pop_end_station, 'and was used', pop_end_station_amount, 'times.')
    except Exception as e:
        print('Error occurred, could not calculate the most used end station: {}'.format(e))

    # display most frequent combination of start station and end station trip
    try:
        pop_trip = df.loc[:, 'Start Station':'End Station'].mode()[0:]
        pop_trip_amt = df.groupby(["Start Station", "End Station"]).size().max()
        print('the most popular trip is:\n', pop_trip, '\n and was driven', pop_trip_amt,'times')
    except Exception as e:
        print('Error occurred, could not calculate the most frequent combination of start station and end station: {}'.format(e))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, city):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    try:
        df['Time Delta'] = df['End Time'] - df['Start Time']
        total_time_delta = df['Time Delta'].sum()
        print('the total travel time was:', total_time_delta)
    except Exception as e:
        print('Error occurred, could not calculate the total travel time of users: {}'.format(e))
    # display mean travel time
    try:
        total_mean = df['Time Delta'].mean()
        print('the mean travel time was about:', total_mean)
    except Exception as e:
        print('Error occurred, could not calculate the mean travel time of users: {}'.format(e))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df,city):
    """Displays statistics on bikeshare users."""


    start_time = time.time()

    # Display counts of user types

    print('\nCalculating User Stats...\n')
    try:
        print('The amount and type of users in', city, 'are as followed:\n', df['User Type'].value_counts())
    except Exception as e:
        print('No data available: {}'.format(e))
        # Display counts of gender
    try:
        print('The amount and gender of users in', city, 'are as followed:\n',df['Gender'].value_counts())
    except Exception as e:
        print('No data available: {}'.format(e))
         # Display earliest, most recent, and most common year of birth
    try:
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()
        print('The age structure of our customers in', city, 'is:\n' 'oldest customer was born in:', int(earliest_year),'\n' 'youngest customer: was born in:', int(most_recent_year),'\n' 'most of our customer are born in:', int(most_common_year))
    except Exception as e:
        print('No data available: {}'.format(e))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

#Display data based on user input
def display_data(df):

    start = 0
    end = 5

    display = input("Do you want to see the raw data?: ").lower()

    if display == 'yes':
        while end <= df.shape[0] - 1:

            print(df.iloc[start:end,:])
            start += 5
            end += 5

            end_display = input("Do you want to see more data?: ").lower()
            if end_display == 'no':
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, city)
        station_stats(df, city)
        trip_duration_stats(df, city)
        user_stats(df,city)
        display_data(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
