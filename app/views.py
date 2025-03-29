from datetime import datetime
from .utils import send_email, gt
from dateutil.relativedelta import relativedelta
from django.shortcuts import render, HttpResponse, redirect
from .models import Register
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password,check_password




@csrf_exempt
def clogin(request):

    if request.method == "POST":
        try:

            data = Register.objects.get(username=request.POST.get("username"))
            if check_password(request.POST.get("password"), data.password):
                if data.is_verified:
                    request.session["user"] = request.POST.get("username")
                    return redirect("attendance_calendar")
                else:
                    data1 = gt(request)
                    request.session["vt"] = data1[2]
                    request.session["ruser"] = request.POST.get("username")
                    send_email(data1[1], data1[0], receiver_mail=data.email)
                    return HttpResponse("You already done your Registration \n \
                                        Please follow the link, we just sent your \
                                        email to verify your account")
            else:
                return render(request, "app/usererrors.html", {"nopass": "no"})

        except Exception as e:

            print(e)
            return render(request, "app/usererrors.html", {"nouser":"ns"})

    return render(request, "app/login.html")



def clogout(request):
    try:
        del request.session["user"]
        return redirect("login")
    except Exception as e:
        print(e)
        return redirect("login")

@csrf_exempt
def cregister(request):
    if request.method == "POST" and request.POST.get("reg") == "reg":
        try:
            date = datetime.now().date()
            Register.objects.create(username=request.POST.get("username"),
                                    name=request.POST.get("name"),
                                    password=make_password(request.POST.get("password")),
                                    phone=request.POST.get("phone"),
                                    email=request.POST.get("email"),
                                    AdmissionDate=date,
                                    address=request.POST.get("address"))
            return HttpResponse("<h1>Registration is Successful.\n Please login with username and password to verify \
                                your account</h1>")
        except Exception as e:

            if "UNIQUE constraint failed" in str(e):
                noregister = 1
            else:
                noregister = 0
            print(e)
            return render(request,
                          "app/usererrors.html",
                          {"nor":noregister})
    return render(request, "app/register.html")


def attendance_calendar(request):

    try:

        data = Register.objects.get(username=request.session["user"])

        if request.session["user"] and data.is_verified == True:
            i_am_in = request.session["user"]
            data = Register.objects.get(username=i_am_in)
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
            return render(request, "app/attendance_calender.html",
                          {"cd": calendar_data, "data": data})
        return HttpResponse("user not verified")
    except Exception as e:
        print(e)
        return redirect("login")
