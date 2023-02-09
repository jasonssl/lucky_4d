import json
import requests
import sqlite3
from datetime import date, datetime, timedelta

def get_numbers():
    # Get the current date
    now = datetime.now()
    
    # longest date hisotry can provide
    start_date = datetime(2021, 9, 15)
    end_date = datetime(now.year, now.month, now.day)

    # Initialize the current date to the start date
    current_date = start_date

    numbers = []

    # Loop through the year by 2-week intervals
    while current_date <= end_date:
        # End date of the current 2-week period
        end_of_period = current_date + timedelta(weeks=2) - timedelta(days=1)

        # Check if the end date of the current 2-week period is after the end date of the year
        if end_of_period > end_date:
            end_of_period = end_date

        # Format the start and end dates for the URL
        start_date_str = current_date.strftime("%d-%m-%Y")
        end_date_str = end_of_period.strftime("%d-%m-%Y")

        # Generate the URL
        # url removed intentionally
        url = ""
        # print(url)
        
        # make a GET request to the url
        response = requests.get(url)
        json_data = response.json()
        
        # print the response
        # print(response.json())

        try:
            for result in json_data["PastResultsRange"]["PastResults"]:
                for key, value in result.items():
                    if ("prize" in key.lower() or "special" in key.lower() or "console" in key.lower()) and isinstance(value, str) and value.isdigit() and len(value) == 4:
                        numbers.append(int(value))
        except:
            # convert the dictionary to a JSON string
            json_data = json.dumps(json_data)

            # parse the JSON string
            parsed_json = json.loads(json_data)
            try:
                for key, value in parsed_json['PastResultsRange']['PastResults'].items():
                        if ("prize" in key.lower() or "special" in key.lower() or "console" in key.lower()) and isinstance(value, str) and value.isdigit() and len(value) == 4:
                            numbers.append(int(value))
            except:
                pass
        # Update the current date to the end of the current 2-week period + 1 day
        current_date = end_of_period + timedelta(days=1)

    # print(len(numbers))
    return numbers

def update_data():
       # Create a connection to the SQLite database and a cursor object to execute SQL commands:
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Create a table to store the data
    cursor.execute('''CREATE TABLE IF NOT EXISTS numbers (date text, numbers text)''')

    # Check if the local data is up to date before pulling new data from the URL
    cursor.execute("SELECT date FROM numbers ORDER BY date DESC LIMIT 1")
    
    most_recent_date = cursor.fetchone()
    if most_recent_date:
        print("DB Last Update: ",most_recent_date[0])
        most_recent_date = most_recent_date[0]
        if most_recent_date == str(date.today().strftime("%Y%m%d")):
            print("Using existing data!")
            # Use the local data instead of pulling new data from the URL
            cursor.execute("SELECT numbers FROM numbers ORDER BY date DESC LIMIT 1")
            numbers = json.loads(cursor.fetchone()[0])
        else:
            print("Data is old, getting new data!")
            # Pull new data from the URL
            numbers = get_numbers()
            # Save the new data to the "numbers" table
            # date_string = date.today().strftime("%Y-%m-%d")
            cursor.execute("INSERT INTO numbers VALUES (?, ?)", (date.today().strftime("%Y%m%d"), json.dumps(numbers)))
    else:
        print("No existing data found, getting some new data!")
        # Pull new data from the URL
        numbers = get_numbers()
        # Save the new data to the "numbers" table
        cursor.execute("INSERT INTO numbers VALUES (?, ?)", (date.today().strftime("%Y%m%d"), json.dumps(numbers)))

    # Commit the changes to the database and close the connection
    conn.commit()
    conn.close()

    return numbers

# update_data()
# get_numbers()
