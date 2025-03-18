# from django.shortcuts import render

# Create your views here.
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse
from django.shortcuts import render
from datetime import date, timedelta, datetime
from .models import Student, Attendance,dim,tty

def attendance_calendar(request):
    start_year = 2025
    start_month = 2  # March
    start_day = 5  # Start from the 1st of the month

    # Get the current date
    current_date = datetime.now()
    data = tty.objects.get(name="GANAPATHI")
    # Start from the given date
    current_iteration_date = datetime(start_year, start_month, start_day)
    count = 0
    while current_iteration_date <= current_date:
        year = current_iteration_date.year
        month = current_iteration_date.month
        month_name = current_iteration_date.strftime("%B")  # Get full month name

        print(f"\nYear: {year}, Month: {month_name}")

        # Get number of days in the current month
        last_day = (current_iteration_date + relativedelta(months=1, days=-current_iteration_date.day)).day

        for day, att in zip(range(start_day, last_day + 1),data.years):
            current_day = datetime(year, month, day)
            day_name = current_day.strftime("%A")
            if current_date.month == current_day.month and current_date.day + 1 == current_day.day:
                pass
            else:

                count += 1
                print(f"{day_name} {day} {month_name} {year}")

            # Stop if we reach the current date
            if current_day >= current_date:
                break
        # Move to the next month
        current_iteration_date += relativedelta(months=1)
        start_day = 1  # Reset start day to 1 after the first month

    print("\n--- Calendar Complete ---")

    return HttpResponse("kskjds")
