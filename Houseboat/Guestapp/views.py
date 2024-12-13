import random
import smtplib
import string
from email.message import EmailMessage

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from Adminapp.models import tbl_district, tbl_location
from Guestapp.models import tbl_login, tbl_owner, tbl_customer


def index(request):
    return render(request, 'Guest/index.html')


def login(request):
    if request.method == 'POST':
        Username = request.POST.get("username")
        Password = request.POST.get("password")
        if tbl_login.objects.filter(username=Username, password=Password).exists():
            Logindata = tbl_login.objects.get(username=Username, password=Password)
            request.session['Uname'] = Logindata.username
            request.session['Loginid'] = Logindata.loginId
            role = Logindata.role
            status = Logindata.status
            if role == "Admin":
                return redirect('/Admin/')
            # return render(request, "Admin/index.html")
            elif role == "Owner" and status == "Accepted":
                return redirect('/Owner/')
            elif role == "Customer" and status == "Confirmed":
                return redirect('/Customer/customerhome')
            else:
                return HttpResponse("NOT Approved")
        else:
            context = {"error": "Incorrect Username or Password"}
            return render(request, "Guest/login.html", context)

    else:
        return render(request, "Guest/login.html")


def ownerreg(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if tbl_login.objects.filter(username=username, password=password).exists():
            return HttpResponse(
                "<script>alert('Username or password already exist');window.location='/ownerreg';</script>")

        lob = tbl_login()
        lob.username = request.POST.get('username')
        lob.password = request.POST.get('password')
        lob.role = 'Owner'
        lob.status = 'Requested'
        email = request.POST.get('email')
        if tbl_owner.objects.filter(email=email).exists():
            return HttpResponse("<script>alert(' Email Already exist');window.location='/ownerreg';</script>")
        cob = tbl_owner()
        lob.save()
        cob.ownername = request.POST.get('ownername')
        cob.email = request.POST.get('email')
        cob.licenseno = request.POST.get('licenseno')
        cob.contactno = request.POST.get('contactno')

        cob.districtid = tbl_district.objects.get(districtid=request.POST.get('districtid'))
        cob.locationid = tbl_location.objects.get(locationid=request.POST.get('locationid'))

        cob.loginid = lob
        cob.save()
        msg = EmailMessage()
        msg.set_content('Your Account has been Registered.')
        msg['Subject'] = "Owner Registration"
        msg['From'] = 'classicgamer622@gmail.com'
        msg['To'] = cob.email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('classicgamer622@gmail.com', 'xirp oknr fuom lltb')
            smtp.send_message(msg)
        return HttpResponse("<script>alert('Owner Registered');window.location='/';</script>")
    district = tbl_district.objects.all()
    location = tbl_location.objects.all()
    return render(request, 'Guest/ownereg.html', {'location': location, 'district': district})


def selectlocation(request):
    did = int(request.POST.get("did"))
    location = tbl_location.objects.filter(districtid=did).values()
    return JsonResponse(list(location), safe=False)


def customerreg(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if tbl_login.objects.filter(username=username, password=password).exists():
            return HttpResponse(
                "<script>alert('Username or password already exist');window.location='/customerreg';</script>")

        lob = tbl_login()
        lob.username = request.POST.get('username')
        lob.password = request.POST.get('password')
        lob.role = 'Customer'
        lob.status = 'Confirmed'
        emailid = request.POST.get('email')
        if tbl_customer.objects.filter(emailid=emailid).exists():
            return HttpResponse("<script>alert(' Email Already exist');window.location='/customerreg';</script>")
        cob = tbl_customer()
        lob.save()
        cob.customername = request.POST.get('customername')
        cob.housename = request.POST.get('housename')
        cob.emailid = request.POST.get('emailid')
        cob.pincode = request.POST.get('pincode')
        cob.phoneno = request.POST.get('phoneno')

        cob.districtid = tbl_district.objects.get(districtid=request.POST.get('districtid'))
        cob.locationid = tbl_location.objects.get(locationid=request.POST.get('locationid'))

        cob.loginid = lob
        cob.save()
        msg = EmailMessage()
        msg.set_content('Your Account has been Registered.')
        msg['Subject'] = "Customer Registration"
        msg['From'] = 'classicgamer622@gmail.com'
        msg['To'] = cob.emailid
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('classicgamer622@gmail.com', 'xirp oknr fuom lltb')
            smtp.send_message(msg)
        return HttpResponse("<script>alert('Customer Registered');window.location='/';</script>")
    district = tbl_district.objects.all()
    location = tbl_location.objects.all()
    return render(request, 'Guest/customerreg.html', {'location': location, 'district': district})


def selectlocation(request):
    did = int(request.POST.get("did"))
    location = tbl_location.objects.filter(districtid=did).values()
    return JsonResponse(list(location), safe=False)


def forgotpassword(request):
    if request.method == 'POST':
        uname = request.POST.get("name")
        if tbl_login.objects.filter(username=uname).exists():
            lg = tbl_login.objects.get(username=uname)
            lid = lg.loginId
            try:
                cust = tbl_owner.objects.get(loginid=lid)
                email = cust.email
                customer_name = cust.ownername
            except ObjectDoesNotExist:
                cust = None

            try:
                emp = tbl_customer.objects.get(loginid=lid)
                emp_mail = emp.emailid
            except ObjectDoesNotExist:
                emp = None

            if cust is None and emp is None:
                return HttpResponse("<script>alert('No data found');window.location='/forgotpassword';</script>")

            characters = string.ascii_letters + string.digits
            random_number = ''.join(random.choice(characters) for _ in range(8))

            lg.password = random_number
            lg.save()

            msg = EmailMessage()
            msg.set_content(
                f'Hi {customer_name if cust else emp.customername}, Your new password to log in is {random_number}')
            msg['Subject'] = "Forgot Password?"
            msg['From'] = 'classicgamer622@gmail.com'
            recipients = [email] if cust else []
            if emp:
                recipients.append(emp_mail)
            msg['To'] = recipients
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('classicgamer622@gmail.com', 'xirp oknr fuom lltb')
                smtp.send_message(msg)

            return HttpResponse(
                "<script>alert('Login with new password in your email');window.location='/login';</script>")
        return HttpResponse("<script>alert('No data found');window.location='/forgotpassword';</script>")
    return render(request, "Guest/forgotpassword.html")
