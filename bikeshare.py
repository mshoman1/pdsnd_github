import time
import pandas as pd

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_user_input(prompt, valid_options):
    """Handles and validates user input."""
    while True:
        user_input = input(prompt).lower()
        if user_input == 'exit':
            exit()
        if user_input in valid_options:
            return user_input
        print("Invalid input. Try again.")

def get_filters():
    """Gets filters from user for city, month, and day."""
    print("Hello! Let's explore some US bikeshare data!")
    print("You can type 'exit' anytime to quit the program.\n")

    city = get_user_input("Enter city (Chicago, New York City, Washington): ", CITY_DATA.keys())
    month = get_user_input("Enter month (January - June) or 'all': ", 
                           ['january', 'february', 'march', 'april', 'may', 'june', 'all'])
    day = get_user_input("Enter day (e.g., Monday) or 'all': ", 
                         ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'])

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """Loads data based on selected city, month, and day."""
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
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print('Most Common Month:', df['month'].mode()[0])
    print('Most Common Day of Week:', df['day_of_week'].mode()[0])
    print('Most Common Start Hour:', df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print('Most Common Start Station:', df['Start Station'].mode()[0])
    print('Most Common End Station:', df['End Station'].mode()[0])

    df['Trip'] = df['Start Station'].str.cat(df['End Station'], sep=" -> ")
    print('Most Common Trip:', df['Trip'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on trip durations."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print('Total Travel Time (seconds):', df['Trip Duration'].sum())
    print('Average Travel Time (seconds):', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('User Type Counts:\n', df['User Type'].value_counts())

    if 'Gender' in df.columns:
        print('\nGender Counts:\n', df['Gender'].value_counts())

    if 'Birth Year' in df.columns:
        print('\nEarliest Birth Year:', int(df['Birth Year'].min()))
        print('Most Recent Birth Year:', int(df['Birth Year'].max()))
        print('Most Common Birth Year:', int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays raw data 5 rows at a time on user request."""
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
    """Main function to run the bikeshare program."""
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
