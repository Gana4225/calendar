from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.shortcuts import render
from .models import Register
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def clogin(request):
    if request.method == "POST":
        print("hello")
    return render(request, "app/login.html")


def cregister(request):
    pass



def attendance_calendar(request):
    data = Register.objects.get(username="gana225")
    start_year = data.AdmissionDate.year
    start_month = data.AdmissionDate.month
    start_day = data.AdmissionDate.day

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
    return render(request, "app/attendance_calender.html", {"cd": calendar_data, "data":data})
