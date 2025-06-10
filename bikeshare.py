import time
import pandas as pd

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    print("Hello! Let's explore some US bikeshare data!")
    print("You can type 'exit' anytime to quit the program.\n")

    # City
    while True:
        city = input("Enter city (Chicago, New York City, Washington): ").lower()
        if city == 'exit':
            exit()
        if city in CITY_DATA:
            break
        print("Invalid city. Try again.")

    # Month
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("Enter month (January - June) or 'all': ").lower()
        if month == 'exit':
            exit()
        if month in months:
            break
        print("Invalid month. Try again.")

    # Day
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input("Enter day (e.g., Monday) or 'all': ").lower()
        if day == 'exit':
            exit()
        if day in days:
            break
        print("Invalid day. Try again.")

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_index = months.index(month) + 1
        df = df[df['month'] == month_index]

    if day != 'all':
        df = df[df['day_of_week'].str.lower() == day.lower()]

    return df

def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print('Most Common Month:', df['month'].mode()[0])
    print('Most Common Day of Week:', df['day_of_week'].mode()[0])
    print('Most Common Start Hour:', df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print('Most Common Start Station:', df['Start Station'].mode()[0])
    print('Most Common End Station:', df['End Station'].mode()[0])

    df['Trip'] = df['Start Station'] + " -> " + df['End Station']
    print('Most Common Trip:', df['Trip'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print('Total Travel Time (seconds):', df['Trip Duration'].sum())
    print('Average Travel Time (seconds):', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('User Type Counts:\n', df['User Type'].value_counts())

    # Gender column only exists in Chicago and NYC
    if 'Gender' in df.columns:
        print('\nGender Counts:\n', df['Gender'].value_counts())

    # Birth Year stats
    if 'Birth Year' in df.columns:
        print('\nEarliest Birth Year:', int(df['Birth Year'].min()))
        print('Most Recent Birth Year:', int(df['Birth Year'].max()))
        print('Most Common Birth Year:', int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    i = 0
    while True:
        show_data = input("\nWould you like to view 5 rows of raw data? Enter yes, no, or 'exit': ").lower()
        if show_data == 'exit':
            exit()
        if show_data != 'yes':
            break
        print(df.iloc[i:i+5])
        i += 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes, no, or "exit":\n').lower()
        if restart == 'exit' or restart != 'yes':
            break

if __name__ == "__main__":
    main()
