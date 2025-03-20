# from django.shortcuts import render

# Create your views here.
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse
from django.shortcuts import render
from datetime import date, timedelta, datetime
# from .models import Student, Attendance,dim

# def attendance_calendar(request):
#     start_year = 2025
#     start_month = 2  # March
#     start_day = 5  # Start from the 1st of the month
#
#     # Get the current date
#     current_date = datetime.now()
#     data = tty.objects.get(name="GANAPATHI")
#     # Start from the given date
#     current_iteration_date = datetime(start_year, start_month, start_day)
#     count = 0
#     while current_iteration_date <= current_date:
#         year = current_iteration_date.year
#         month = current_iteration_date.month
#         month_name = current_iteration_date.strftime("%B")  # Get full month name
#
#         print(f"\nYear: {year}, Month: {month_name}")
#
#         # Get number of days in the current month
#         last_day = (current_iteration_date + relativedelta(months=1, days=-current_iteration_date.day)).day
#
#         for day, att in zip(range(start_day, last_day + 1),data.years):
#             current_day = datetime(year, month, day)
#             day_name = current_day.strftime("%A")
#             if current_date.month == current_day.month and current_date.day + 1 == current_day.day:
#                 pass
#             else:
#
#                 count += 1
#                 print(f"{day_name} {day} {month_name} {year}")
#
#             # Stop if we reach the current date
#             if current_day >= current_date:
#                 break
#         # Move to the next month
#         current_iteration_date += relativedelta(months=1)
#         start_day = 1  # Reset start day to 1 after the first month
#     print("\n--- Calendar Complete ---")
#
#     return HttpResponse("kskjds")











from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.shortcuts import render
from .models import AttStatus



def attendance_calendar(request):



    data = AttStatus.objects.get(name="GANAPATHI")

    start_year = 2024
    start_month = 11  # February
    start_day = 1  # Start from the 5th

    current_date = datetime.now()


    current_iteration_date = datetime(start_year, start_month, start_day)
    calendar_data = []

    attendance_list = list(data.att_status)
    att_index = 0

    while current_iteration_date <= current_date:
        year = current_iteration_date.year
        month = current_iteration_date.month
        month_name = current_iteration_date.strftime("%B")

        last_day = (current_iteration_date + relativedelta(months=1, days=-current_iteration_date.day)).day
        first_day_of_month = datetime(year, month, 1).weekday()  # Get first day of month

        days_list = []
        year1 = []
        for day in range(1, last_day + 1):
            current_day = datetime(year, month, day)
            day_name = current_day.strftime("%A")

            if current_day < datetime(start_year, start_month, start_day):
                continue  # Skip days before the start date

            if current_day > current_date:
                break  # Stop at today’s date

            att_status = attendance_list[att_index] if att_index < len(attendance_list) else "No Data"
            att_index += 1

            days_list.append({"day": day, "day_name": day_name, "status": att_status})

        calendar_data.append({
            "year": year,
            "month": month_name,
            "days": days_list,
            "start_offset": range(first_day_of_month),  # Fill empty days at the start
        })

        current_iteration_date += relativedelta(months=1)
    return render(request, "attendance_calender.html", {"cd": calendar_data, "y":year})
