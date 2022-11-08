import time
import pandas as pd
import numpy as np
#three database file will be used
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# def a function to check user's inputs
def check_answer(answer,answers=('y','n')):
    while True:
        check_answer = input(answer).lower().strip()
        if ',' in check_answer:
            check_answer = [i.strip().lower() for i in check_answer.split(',')]
            if list(filter(lambda x: x in answers, check_answer)) == check_answer:
                break
        elif ',' not in check_answer:
            if check_answer in  answers:
                break

        answer = ("Sorry, your input is wrong, please try again:")

    return check_answer
# def function
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    Formal_city = ["chicago","new york city","washington"]
    Formal_Time = ["month","day","not at all"]
    Formal_month = ["all","january","february","march","april","may","june"]
    Formal_day = ["all","monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = check_answer("Would you like to see data for chicago, new york city, washington or muti cities?:",CITY_DATA.keys())
        month = check_answer("Which month would you like to see?:",Formal_month)
        day = check_answer("Which day would you like to see?:",Formal_day)
        double_check = check_answer("Is this data set you would like to see? City:{},Month:{},day:{}: [y] yes or [n] No  ".format(city, month, day))
        if double_check == 'y':
            break
        else:
            print("Do not worry, let us try again carefully")


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
    #convert the start time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['Start hour']=df['Start Time'].dt.hour

    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['Month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    Most_common_month = df['Month'].mode()[0]
    print('Most Popular month:', Most_common_month)

    # TO DO: display the most common day of week
    Most_common_day = df['day_of_week'].mode()[0]
    print('Most Popular day:', Most_common_day)

    # TO DO: display the most common start hour
    Most_common_start_hour = df['Start hour'].mode()[0]
    print('Most Start hour:', Most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    Most_common_start_station = df['Start Station'].mode()[0]
    print('Most popular Start Station:', Most_common_start_station)

    # TO DO: display most commonly used end station
    Most_common_end_station = df['End Station'].mode()[0]
    print('Most popular end Station:', Most_common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['Start_Station_+_end_station_trip'] = (df['Start Station'] + ' - ' + df['End Station'])
    most_frequent_combination_of_Start_End_Station_trip = df['Start_Station_+_end_station_trip'].mode()[0]
    print('most frequent combination of Start & End Station trip:',most_frequent_combination_of_Start_End_Station_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time is:',total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time is:',mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types

    counts_of_user_types = df['User Type'].value_counts()
    print('Counts of user types:', counts_of_user_types)
    # TO DO: Display counts of gender
    try:
        counts_of_gender = df['gender'].value_counts()
        print('Counts of gender:', counts_of_gender)
    except KeyError:
        print('No user gender of {}'.format(city))
    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_year_of_birth = df['Birth Year'].min()
        print('The erliest year of birth is:', earliest_year_of_birth)
        most_recent_year_of_birth = df['Birth Year'].max()
        print('The most recent year of birth is:',  most_recent_year_of_birth)
        most_common_year_of_birth = df['Birth Year'].mode()[0]
        print('The most common year of birth is:', most_common_year_of_birth)
    except:
        print("Sorry,No data about year birth message for {}".format(city))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?")
    start_loc = 0
    while view_data =='yes':
        print(df.iloc[start_loc : start_loc+5])
        start_loc += 5
        view_display = input("Do you wish to continue?Enter yes or no: ").lower()
        if view_display == 'yes':
            continue
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        display_data(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
