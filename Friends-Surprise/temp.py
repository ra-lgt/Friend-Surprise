import time
from datetime import datetime, timedelta

def your_daily_function():
    print("Running your daily function from 19:10 to 19:40")

def run_daily_schedule():
    while True:
        now = datetime.now()

        # Check if the current time is between 19:10 and 19:40
        if datetime(now.year, now.month, now.day, 19, 10) <= now < datetime(now.year, now.month, now.day, 19, 40):
            your_daily_function()

        # Calculate the time until 19:10 of the next day
        next_run_time = datetime(now.year, now.month, now.day) + timedelta(days=1, hours=19, minutes=10)
        time_until_next_run = (next_run_time - now).total_seconds()

        # Sleep until 19:10 of the next day
        print(time_until_next_run)
        time.sleep(time_until_next_run)

if __name__ == '__main__':
    run_daily_schedule()
