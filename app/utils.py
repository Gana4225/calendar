import smtplib
import threading

from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
from django.shortcuts import render, HttpResponse
from .models import Register
import uuid


def send_email(subject, message, receiver_mail):
    def send():
        try:
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email="chganapathi4225@gmail.com",  # Sender email
                to=[receiver_mail]
            )
            email.content_subtype = "html"
            email.send(fail_silently=False)
            print(f"Email sent successfully to {receiver_mail}")
        except smtplib.SMTPException as e:
            print(f"Failed to send email: {e}")

    # Start a new thread for email sending
    thread = threading.Thread(target=send)
    thread.start()




def verify(request, token):
    name = request.session.get("ruser")
    stored_token = request.session.get("vt")
    if token == stored_token:
        user = Register.objects.get(username=name)
        user.is_verified = True
        user.save()
        if "ruser" in request.session:
            del request.session["ruser"]

        if "vt" in request.session:
            del request.session["vt"]

        return render(request, "app/success.html", {"reg":"done"})
    else:
        return HttpResponse("Invalid verification link or expired token.")




def forgetpass(request,token):
    if request.method == "POST" and token == "change":
        try:
            user = request.POST.get("username")
            print(user)
            data = Register.objects.get(username=user)
            date1 = gfp(request)
            request.session["vt"] = date1[2]
            request.session["ruser"] = user
            send_email(date1[1], date1[0], data.email)
            return HttpResponse("<h1>Please check your email just \
                                 we sent an forget password link to it</h1>")
        except Exception as e:
            print(e)
    if request.method == "POST" and token == request.session.get("vt"):

        new = request.POST.get("newpassword")
        old = request.POST.get("password")

        if new == old:
            try:
                data = Register.objects.get(username=request.session.get("ruser"))
                data.password = make_password(new)
                data.save()
                return HttpResponse("password Changed success")
            except Exception as e:
                print(e)

        return render(request, "app/forget.html", {"token": "token"})

    else:

        return render(request, "app/forget.html", {"token": token})


    return render(request, "app/forget.html", {"token": "token"})



    # if request.method == "POST":
    #     user = request.POST.get("username")
    #     data = Register.objects.get(username=user)
    #     print(data.username)
    #     return render(request, "app/forget.html", {"token": token})







































def gfp(request):
    token = str(uuid.uuid4())
    protocol = "https" if request.is_secure() else "http"
    host = request.get_host()
    link = f"{protocol}://{host}/forget/{token}/"
    gsubject = "Royal Gym Request for forget password"
    gmessage = f"""
                                                <html>
                                                <head>
                                                    <style>
                                                        body {{
                                                            font-family: Arial, sans-serif;
                                                            line-height: 1.6;
                                                            color: #333;
                                                        }}
                                                        .container {{
                                                            max-width: 600px;
                                                            margin: 0 auto;
                                                            padding: 20px;
                                                            background-color: #f9f9f9;
                                                            border-radius: 10px;
                                                            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
                                                        }}
                                                        .header {{
                                                            text-align: center;
                                                            font-size: 22px;
                                                            font-weight: bold;
                                                            color: #007bff;
                                                        }}
                                                        .content {{
                                                            font-size: 16px;
                                                            padding: 10px;
                                                            background-color: white;
                                                            border-radius: 8px;
                                                            text-align: justify;
                                                        }}
                                                        .button {{
                                                            display: block;
                                                            width: fit-content;
                                                            margin: 20px auto;
                                                            padding: 12px 25px;
                                                            color: white;
                                                            background-color: lightgreen;
                                                            text-decoration: none;
                                                            font-weight: bold;
                                                            border-radius: 5px;
                                                            text-align: center;
                                                        }}
                                                        .footer {{
                                                            text-align: center;
                                                            margin-top: 20px;
                                                            font-size: 14px;
                                                            color: #555;
                                                        }}
                                                    </style>
                                                </head>
                                                <body>
                                                    <div class="container">
                                                        <div class="header">Reset Your Password - Royal Gym 🔐</div>
                                                        <div class="content">
                                                            <p><strong>Dear Valued Member,</strong></p>
                                                            <p>We received a request to reset your password. Click the button below to set up a new password:</p>
                                                            <a href="{link}" class="button">Reset Password</a>
                                                            <p><strong>⚠️ Important:</strong></p>
                                                            <ul>
                                                                <li>This password reset link is valid for a limited time.</li>
                                                                <li>If you did not request a password reset, please ignore this email.</li>
                                                                <li><strong>Do not share this link</strong> with anyone for security reasons.</li>
                                                            </ul>
                                                            <p>If you have any issues, feel free to contact our support team.</p>
                                                        </div>
                                                        <div class="footer">
                                                            <strong>Stay Strong, Stay Secure! 🔒</strong> <br>
                                                            <strong>Royal Gym Team</strong> <br>
                                                            Your Fitness, Your Security!
                                                        </div>
                                                    </div>
                                                </body>
                                                </html>
                                                """
    return [gmessage, gsubject, token]



def gt(request):
    token = str(uuid.uuid4())
    protocol = "https" if request.is_secure() else "http"
    host = request.get_host()
    link = f"{protocol}://{host}/verify/{token}/"
    gsubject = "Royal Gym Registration/Verification – OTV"
    gmessage = f"""
                                            <html>
                                            <head>
                                                <style>
                                                    body {{
                                                        font-family: Arial, sans-serif;
                                                        line-height: 1.6;
                                                        color: #333;
                                                    }}
                                                    .container {{
                                                        max-width: 600px;
                                                        margin: 0 auto;
                                                        padding: 20px;
                                                        background-color: #f9f9f9;
                                                        border-radius: 10px;
                                                        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
                                                    }}
                                                    .header {{
                                                        text-align: center;
                                                        font-size: 22px;
                                                        font-weight: bold;
                                                        color: #007bff;
                                                    }}
                                                    .content {{
                                                        font-size: 16px;
                                                        padding: 10px;
                                                        background-color: white;
                                                        border-radius: 8px;
                                                        text-align: justify;
                                                    }}
                                                    .button {{
                                                        display: block;
                                                        width: fit-content;
                                                        margin: 20px auto;
                                                        padding: 12px 25px;
                                                        color: white;
                                                        background-color: lightgreen;
                                                        text-decoration: none;
                                                        font-weight: bold;
                                                        border-radius: 5px;
                                                        text-align: center;
                                                    }}
                                                    .footer {{
                                                        text-align: center;
                                                        margin-top: 20px;
                                                        font-size: 14px;
                                                        color: #555;
                                                    }}
                                                </style>
                                            </head>
                                            <body>
                                                <div class="container">
                                                    <div class="header">Welcome to Royal Gym! 🏋️</div>
                                                    <div class="content">
                                                        <p><strong>Dear Valued Member,</strong></p>
                                                        <p>We are thrilled to have you on board! 🎉 To complete your registration, please verify your account by clicking the button below:</p>
                                                        <a href="{link}" class="button">Verify Your Account</a>
                                                        <p><strong>⚠️ Important:</strong></p>
                                                        <ul>
                                                            <li>This verification link is valid for a limited time.</li>
                                                            <li><strong>Never share this link</strong> with anyone to keep your account secure.</li>
                                                        </ul>
                                                        <p>If you did not request this, please ignore this email.</p>
                                                    </div>
                                                    <div class="footer">
                                                        <strong>Stay Strong, Stay Fit! 💪</strong> <br>
                                                        <strong>Royal Gym Team</strong> <br>
                                                        Transforming Fitness, One Step at a Time!
                                                    </div>
                                                </div>
                                            </body>
                                            </html>
                                            """
    return [gmessage,gsubject,token]