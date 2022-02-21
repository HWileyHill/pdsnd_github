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
    # Get user input for city (chicago, new york city, washington)
    line_in = '' #Define this value ahead of time for use in user input
    while line_in.lower() not in ['c', 'n', 'w']:
        print('Are you interested in data on [C]hicago, [N]ew York City, or [W]ashington?')
        line_in = input('Type one letter only: ')

    city_dict = {'c': 'chicago', 'n': 'new york city', 'w': 'washington'}
    city = city_dict[line_in.lower()]

    # Get user input for month (all, january, february, ... , june)
    n_range = []
    for i in range(7):
        n_range.append(str(i)) #Should practice automating making lists like this.

    line_in = '-1' #Don't want to recycle the value from the last input
    while line_in not in n_range: #0 through 7
        print('Enter the number for the month you want, from 1 (January) to 6 (June).')
        print('If interested in data for all months, enter the number 0.')
        line_in = input('One numerical digit only, please: ')

    month_list = ['all', 'January', 'February', 'March', 'April', 'May', 'June']
    month = month_list[int(line_in)]
    # Coder's note: I'm a bit proud of myself for making 0 the "all" value.
    # It's sensible for the user, and it elegantly dodges a potential one-off error.

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    line_in = '-1'
    n_range.append('7')
    while line_in not in n_range:
        print('Enter the number for the weekday you want, from 1 (Monday) to 7 (Sunday).')
        print('If interested in data for all weekdays, enter the number 0.')
        line_in = input('One numerical digit only, please: ')

    day_list = ['all', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day = day_list[int(line_in)]

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
    # I can literally just copy all this from Example Problem 3...

    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month_name()
    df['Weekday'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        #Since the database now uses the month name instead of the month number,
        # we don't need to look up the number.  Commenting this out.
#        # use the index of the months list to get the corresponding int
#        months = ['January', 'February', 'March', 'April', 'May', 'June']
#        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['Month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Weekday'] == day]

    return df


def show_raw_data(df, column_name):
    """
    Shows the raw data in an interactive format.

    Args:
        (DataFrame) df - the dataframe to show data from
        (str) column_name - the name of the column to organize the data by
    """

    view = ''
    while view.lower() not in ['y', 'n']:
        view = input('Display the raw data organized by ' + column_name.lower() + '?  Type Y or N: ')

    #Sort the data by the given column name
    if view.lower() == 'y':
        pd.set_option('display.max_columns',200)
        df = df.sort_values(column_name)

    it = 0 # It stands for "iterator"
    while view.lower() != 'n':
        #Display the data in sets of five, sorted by the given column name
        if view.lower() == 'y': #This allows the print to be skipped under special circumstances
            print(df.iloc[it:it+5])

        view = ''
        while view.lower() not in ['n', 'p', 'r', 'q']:
            print('View [N]ext or [P]revious data, [R]epeat the last data, or [Q]uit?')
            view = input('Type one letter only: ')

        if view.lower() == 'n':
            if it+5 > len(df):
                print('Oops, you\'re at the end of the dataframe!  No more to display!')
                view = 'x' #Special value to skip printing the same data again
            else:
                it += 5
                view = 'y'
        elif view.lower() == 'p':
            if it <= 0:
                print('Oops, you\'re at the beginning of the dataframe!  No more to display!')
                view = 'x'
            else:
                it -= 5
                view = 'y'
        elif view.lower() == 'r':
            view = 'y'
        else: #Can only be Q at this point
            view = 'n'


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating the most frequent times of travel...\n')
    start_time = time.time()

    # Display the most common month
    if df.nunique()['Month'] > 1:
        print("Most Frequent Month: " + str(df['Month'].mode()[0]))
    else:
        print("Month statistic skipped over; this slice only covers one month")

    # Display the most common day of week
    print("Most frequent weekday: " + str(df['Weekday'].mode()[0]))

    # Display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    print("Most frequent hour: " + str(df['Hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    df.drop(columns='Hour', inplace=True) #Clean up
    show_raw_data(df, 'Start Time')
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating the most popular stations and trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print("Most common start station: " + df['Start Station'].mode()[0])

    # Display most commonly used end station
    print("Most common end station: " + df['End Station'].mode()[0])

    # Display most frequent combination of start station and end station trip
    df['Start/End Station'] = df['Start Station'] + " -> " + df['End Station']
    print("Most common start/end combination: " + df['Start/End Station'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    df.drop(columns='Start/End Station', inplace = True)
    show_raw_data(df, 'Start Station')
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating trip duration...\n')
    start_time = time.time()

    # Display total travel time
    print("Total travel time: " + str(df['Trip Duration'].sum()) + " seconds")

    # Display mean travel time
    print("Mean travel time: " + str(round(df['Trip Duration'].mean(), 1)) + " seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    show_raw_data(df, 'Trip Duration')
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating user stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Statistics of user types:\n' + str(df['User Type'].value_counts()))

    # Display counts of gender - if available, of course
    if 'Gender' in df.columns: #More modular than checking if the city is Washington.
        print('\nStatistics of user genders:\n' + str(df['Gender'].value_counts()))
    else: #A bit of user-friendliness, here
        print('\nGender statistics not available for this dataset')

    # Display earliest, most recent, and most common year of birth, if available
    if 'Birth Year' in df.columns:
        print('\nEarliest birth year: ' + str(int(df['Birth Year'].min())))
        print('Most recent birth year: ' + str(int(df['Birth Year'].max())))
        print('Most common birth year: ' + str(int(df['Birth Year'].mode()[0])))
    else:
        print('\nBirth year statistics not available for this dataset')

    print("\nThis took %s seconds." % (time.time() - start_time))
    show_raw_data(df, 'User Type')
    if 'Gender' in df.columns:
        show_raw_data(df, 'Gender')
    if 'Birth Year' in df.columns:
        show_raw_data(df, 'Birth Year')
    print('-'*40)


def main():
    restart = '' #Defining it up here for better flow control
    while restart.lower() != 'n':
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = ''
        while restart.lower() not in ['y', 'n']:
            restart = input('\nWould you like to restart?  Type Y or N: ')


if __name__ == "__main__":
	main()
