import time
import pandas as pd


CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_valid_answer(prompt, valid_answers):
    """
    Asks user to make a choice until they specify a valid option among the ones provided.

    Args:
        (str) propmt - prompt to the user showing the valid options
        (list) valid_answers - list of valid answers (str)

    Returns:
        (str) answer - valid answer provided by the user (in lowercase)
    """

    print()
    answer = input(prompt)
    answer = answer.strip().lower()

    while answer not in valid_answers:
        print('\nSorry, you chose an invalid option. Please try again.\n')

        answer = input(prompt)
        answer = answer.strip().lower()
    
    return answer


def get_city_filter():
    """
    Asks user for a city until they specify a valid one.

    Returns:
        (str) city - name of the city in lowercase
    """

    city = get_valid_answer(
        prompt='Would you like to see data for Chicago, New York, or Washington?\n>>> ',
        valid_answers=('chicago', 'new york', 'washington')
    )

    print(f'\nYou chose {city.title()}. If this is not your choice, restart the program.')

    return city


def get_month_filter():
    """
    Asks if the user wants to filter the data by month. In the positive case, asks which month.

    Returns:
        (str) month - name of the month in lowercase or None if the filter was not required
    """

    month_filter = get_valid_answer(
        prompt='Would you like to filter the data by month (Y/N)?\n>>> ',
        valid_answers=('y', 'yes', 'n', 'no')
    )

    if month_filter in ('y', 'yes'):
        month = get_valid_answer(
            prompt='Which month (January, February, March, April, May, or June)?\n>>> ',
            valid_answers=('january', 'february', 'march', 'april', 'may', 'june')
        )
        
        print(f'\nYou choose {month.title()}. If this is not your choice, restart the program.')
    else:
        print('\nOK. You want to see data from all months.')
        month = None

    return month


def get_day_filter():
    """
    Asks if the user wants to filter the data by day. In the positive case, asks which day.

    Returns:
        (str) day - name of the day in lowercase or None if the filter was not required
    """

    day_filter = get_valid_answer(
        prompt='Would you like to filter the data by day (Y/N)?\n>>> ',
        valid_answers=('y', 'yes', 'n', 'no')
    )

    if day_filter in ('y', 'yes'):
        day = get_valid_answer(
            prompt='Which day (Monday, Tuesday, Wednesday, Thursday, or Friday)?\n>>> ',
            valid_answers=('monday', 'tuesday', 'wednesday', 'thursday', 'friday')
        )
        
        print(f'\nYou choose {day.title()}. If this is not your choice, restart the program.\n')
    else:
        print('\nOK. You want to see data from all days.\n')
        day = None

    return day


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or None to apply no month filter
        (str) day - name of the day of week to filter by, or None to apply no day filter
    """

    print()
    print('=' * 80)
    print('Hello! Let\'s explore some US bikeshare data!')
    print('=' * 80)

    # Get user input for city (Chicago, New York, or Washington)
    city = get_city_filter()

    # Get user input for month (all, january, february, ... , june)
    month = get_month_filter()

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_day_filter()

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or None to apply no month filter
        (str) day - name of the day of week to filter by, or None to apply no day filter
    
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city], index_col=0)

    # Convert the Start Time and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Filter by month if applicable
    if month is not None:
        df = df[df['Start Time'].dt.month_name() == month.title()]

    # Filter by day of week if applicable
    if day is not None:
        df = df[df['Start Time'].dt.day_name() == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('=' * 80)
    print('Calculating The Most Frequent Times of Travel...')
    print('=' * 80)

    start_time = time.time()

    # Display the most common month
    print('\n> Most common month:')
    print(f'  {df["Start Time"].dt.month_name().mode()[0]}')

    # Display the most common day of week
    print('\n> Most common day of week:')
    print(f'  {df["Start Time"].dt.day_name().mode()[0]}')

    # Display the most common start hour
    print('\n> Most common start hour:')
    print(f'  {df["Start Time"].dt.hour.mode()[0]}')

    print(f'\nThis took {(time.time() - start_time):.3f} seconds.\n')


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('=' * 80)
    print('Calculating The Most Popular Stations and Trip...')
    print('=' * 80)

    start_time = time.time()

    # Display most commonly used start station
    print('\n> Most common start station:')
    print(f'  {df["Start Station"].mode()[0]}')

    # Display most commonly used end station
    print('\n> Most common end station:')
    print(f'  {df["End Station"].mode()[0]}')

    # Display most frequent combination of start station and end station trip
    print('\n> Most common trip:')
    print(f'  {(df["Start Station"] + " -> " + df["End Station"]).mode()[0]}')

    print(f'\nThis took {(time.time() - start_time):.3f} seconds.\n')


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('=' * 80)
    print('Calculating Trip Duration...')
    print('=' * 80)

    start_time = time.time()

    # Display total travel time
    total_time = (df['End Time'] - df['Start Time']).sum().components
    print('\n> Total travel time:')
    print(f'  {total_time.days} day(s), {total_time.hours} hour(s), {total_time.minutes} minute(s), {total_time.seconds} second(s)')

    # Display mean travel time
    mean_time = (df['End Time'] - df['Start Time']).mean().components
    print('\n> Mean travel time:')
    print(f'  {mean_time.minutes} minute(s), {mean_time.seconds} second(s)')

    print(f'\nThis took {(time.time() - start_time):.3f} seconds.\n')


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('=' * 80)
    print('Calculating User Stats...')
    print('=' * 80)

    start_time = time.time()

    # Display counts of user types
    print('\nDistribution by user types:')
    print('-' * 40, end='\n\n')

    # Total values (some are null)
    total_users = df['User Type'].count()
    
    for user_type, count in df['User Type'].value_counts().to_dict().items():
        print(f'{user_type}:\t{count} ({count/total_users * 100:.2f}%)')

    # Display counts by gender
    if 'Gender' in df.columns:
        print('\nDistribution by gender:')
        print('-' * 40, end='\n\n')

        # Total values (some are null)
        total_users = df['Gender'].count()

        for gender, count in df['Gender'].value_counts().to_dict().items():
            print(f'{gender}:\t{count} ({count/total_users * 100:.2f}%)')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nBirth year statistics:')
        print('-' * 40, end='\n\n')

        print('> Birth year of oldest user:')
        print(f'  {df["Birth Year"].min():.0f}')

        print('\n> Birth year of youngest user:')
        print(f'  {df["Birth Year"].max():.0f}')

        print('\n> Most common birth year:')
        print(f'  {df["Birth Year"].mode()[0]:.0f}')

    print(f'\nThis took {(time.time() - start_time):.3f} seconds.\n')


def individual_trip_data(df, rows_per_time=5):
    """Asks if the user wants to see individual trip data and displays it if desired."""

    print('=' * 80)
    print('Individual trip data')
    print('=' * 80)

    trip_data = get_valid_answer(
        prompt='Would you like to see individual trip data (Y/N)?\n>>> ',
        valid_answers=('y', 'yes', 'n', 'no')
    )
    
    if trip_data in ('y', 'yes'):
        total_rows = len(df)
        current_row = 0

        while trip_data in ('y', 'yes') and current_row < total_rows:
            row_selection = df.iloc[current_row:current_row + rows_per_time]

            print()

            for idx, data in row_selection.to_dict(orient='index').items():
                print(f'Trip ID: {idx}')
                for col, value in data.items():
                    print(f'{col}: {value}')
                print()
        
            current_row += rows_per_time

            trip_data = get_valid_answer(
                prompt='Would you like to see more individual trip data (Y/N)?\n>>> ',
                valid_answers=('y', 'yes', 'n', 'no')
            )
        

def main():
    """Main function - Executes the interactive program."""

    while True:
        city, month, day = get_filters()

        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        individual_trip_data(df, rows_per_time=5)

        print()
        print('='*80)
        print('You have reached the end of the program.')
        print('='*80)

        restart = get_valid_answer(
            prompt='Would you like to restart the program (Y/N)?\n>>> ',
            valid_answers=('y', 'yes', 'n', 'no')
        )

        if restart in ('no', 'n'):
            break


if __name__ == "__main__":
	main()
