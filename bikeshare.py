import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    Asks user to specify a city, filter type, and filter value to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) filter_type - type of filter to apply: 'month', 'day', or 'none'
        (str) filter_value - specific month or day to filter by, or 'all' if no filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington)
    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington?\n").lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid input. Please choose Chicago, New York City, or Washington.")
    
    # get user input for filter type
    while True:
        filter_type = input("Would you like to filter the data by month, day, or not at all? Type 'month', 'day', or 'none'.\n").lower()
        if filter_type in ['month', 'day', 'none']:
            break
        else:
            print("Invalid input. Please choose 'month', 'day', or 'none'.")
    
    # get user input for filter value based on filter type
    if filter_type == 'month':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        while True:
            filter_value = input("Which month? January, February, March, April, May, or June?\n").lower()
            if filter_value in months:
                break
            else:
                print("Invalid input. Please choose a month from the list.")
    elif filter_type == 'day':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        while True:
            filter_value = input("Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n").lower()
            if filter_value in days:
                break
            else:
                print("Invalid input. Please choose a day from the list.")
    else:  # 'none'
        filter_value = 'all'

    print('-'*40)
    return city, filter_type, filter_value

def load_data(city, filter_type, filter_value):
    """
    Loads data for the specified city and filters by month or day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) filter_type - type of filter to apply: 'month', 'day', or 'none'
        (str) filter_value - specific month or day to filter by, or 'all' if no filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if filter_type == 'month':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(filter_value) + 1
        df = df[df['month'] == month]

    # filter by day of week if applicable
    elif filter_type == 'day':
        df = df[df['day_of_week'] == filter_value.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print(f"Most common month: {most_common_month}")

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print(f"Most common day of week: {most_common_day}")

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print(f"Most common start hour: {most_common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start = df['Start Station'].mode()[0]
    print(f"Most commonly used start station: {most_common_start}")

    # display most commonly used end station
    most_common_end = df['End Station'].mode()[0]
    print(f"Most commonly used end station: {most_common_end}")

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
    most_common_trip = df['Trip'].mode()[0]
    print(f"Most frequent trip: {most_common_trip}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total travel time: {total_travel_time} seconds")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"Mean travel time: {mean_travel_time} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of user types:")
    print(user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of gender:")
        print(gender_counts)
    else:
        print("\nGender data not available for this city.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print(f"\nEarliest year of birth: {earliest_year}")
        print(f"Most recent year of birth: {most_recent_year}")
        print(f"Most common year of birth: {most_common_year}")
    else:
        print("\nBirth year data not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays rows of data from the DataFrame."""
    start = 0
    while True:
        view_data = input('\nDo you want to check the first 5 rows of the dataset related to the chosen city? Enter yes or no.\n')
        if view_data.lower() != 'yes':
            return
        
        print(df.iloc[start:start+5])
        start += 5
        
        while True:
            more_data = input('Do you want to check another 5 rows of the dataset? Enter yes or no.\n')
            if more_data.lower() != 'yes':
                return
            
            print(df.iloc[start:start+5])
            start += 5
            
            if start >= len(df):
                print("No more rows to display.")
                return

def main():
    while True:
        city, filter_type, filter_value = get_filters()
        df = load_data(city, filter_type, filter_value)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        display_data(df)  # Call the new function to display rows
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
