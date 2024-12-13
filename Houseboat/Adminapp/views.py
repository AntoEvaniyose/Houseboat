import smtplib
from datetime import datetime
from email.message import EmailMessage
import xlwt
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control

from Adminapp.models import tbl_district, tbl_location, tbl_category, tbl_package, tbl_service
from Customerapp.models import tbl_payment, tbl_request
from Guestapp.models import tbl_owner, tbl_login, tbl_customer
from django.views.generic import View

from Ownerapp.models import tbl_boat


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminhome(request):
    if 'Loginid' in request.session:
        return render(request, 'Admin/index.html', {'Uname': request.session['Loginid']})
    else:
        return HttpResponse("<script>alert('You have to login first');window.location='../login';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def district(request):
    if 'Loginid' in request.session:
        if request.method == "POST":
            d = tbl_district()
            d.districtname = request.POST.get('districtname')
            if tbl_district.objects.filter(districtname=request.POST.get('districtname')).exists():
                return HttpResponse("<script>alert('Already Exists...');window.location='../district';</script>")
            else:
                d.save()
                return HttpResponse(
                    "<script>alert('Succesfully Added...');window.location='../districtview/';</script>")
        else:
            district = tbl_district.objects.all()
            return render(request, 'Admin/district.html', {'district': district})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def location(request):
    if 'Loginid' in request.session:
        if request.method == "POST":
            data = tbl_location()
            data.locationname = request.POST.get('locationname')
            if tbl_location.objects.filter(locationname=request.POST.get('locationname')).exists():
                return HttpResponse("<script>alert('already exists');window.location='../location';</script>")
            else:
                data.districtid = tbl_district.objects.get(districtid=request.POST.get('districtid'))
                data.save()
                return HttpResponse("<script>alert('successfully added');window.location='../locationview';</script>")
        location = tbl_location.objects.all()
        district = tbl_district.objects.all()
        return render(request, 'Admin/location.html', {'location': location, 'district': district})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def districtview(request):
    if 'Loginid' in request.session:
        districtview = tbl_district.objects.all()
        return render(request, 'Admin/viewdistrict.html', {'districtview': districtview})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editdistrict(request, id):
    if 'Loginid' in request.session:
        if request.method == 'POST':
            districtname = request.POST.get('districtname')
            dist = tbl_district.objects.get(districtid=id)
            dist.districtname = districtname
            dist.save()
            return districtview(request)
        dist = tbl_district.objects.get(districtid=id)
        return render(request, 'Admin/editdistrict.html', {'dist': dist})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletedistrict(request, id):
    dist = tbl_district.objects.get(districtid=id)
    dist.delete()
    return districtview(request)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewlocation(request):
    if 'Loginid' in request.session:
        location = tbl_location.objects.all()
        district = tbl_district.objects.all()
        return render(request, "admin/viewlocation.html", {'location': location, 'district': district})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editlocation(request, id):
    if 'Loginid' in request.session:
        if request.method == 'POST':
            locationname = request.POST.get('locationname')
            loc = tbl_location.objects.get(locationid=id)
            loc.locationname = locationname
            loc.save()
            return viewlocation(request)
        loc = tbl_location.objects.get(locationid=id)
        return render(request, "Admin/editlocation.html", {'loc': loc})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletelocation(request, id):
    if 'Loginid' in request.session:
        data = tbl_location.objects.get(locationid=id)
        data.delete()
        return viewlocation(request)
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def filllocation(request):
    if 'Loginid' in request.session:
        did = int(request.POST.get("did"))
        # return HttpResponse(did)
        location = tbl_location.objects.filter(districtid=did).values()
        return JsonResponse(list(location), safe=False)
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def category(request):
    if 'Loginid' in request.session:
        if request.method == 'POST':
            categoryname = request.POST.get('categoryname')
            if tbl_category.objects.filter(categoryname=request.POST.get('categoryname')).exists():
                return HttpResponse("<script>alert('Already Exists...');window.location='../category';</script>")
            if len(request.FILES) != 0:
                cimage = request.FILES['image']
            else:
                cimage = 'images/default.jpeg'
            # return HttpResponse(name+" "+desc+" "+cimage)
            catobj = tbl_category()
            catobj.categoryname = categoryname
            catobj.image = cimage
            catobj.save()
            return HttpResponse(
                "<script>alert('Category added successfully');window.location ='../viewcategory';</script>")
        else:
            return render(request, "Admin/category.html")
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewcategory(request):
    if 'Loginid' in request.session:
        ca = tbl_category.objects.all()
        return render(request, "Admin/viewcategory.html", {'category': ca})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editcategory(request, id):
    if 'Loginid' in request.session:
        if request.method == "POST":
            cat = tbl_category.objects.get(categoryid=id)
            cat.categoryname = request.POST.get('categoryname')
            if len(request.FILES) == 0:
                cat.image = request.POST.get('oldimg')
            else:
                cat.image = request.FILES['Image']
            cat.save()
            return HttpResponse(
                "<script>alert('successfully updated');window.location='/Admin/viewcategory/';</script>")
        else:
            category = tbl_category.objects.get(categoryid=id)
            return render(request, 'Admin/editcategory.html', {'cat': category})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletecategory(request, id):
    if 'Loginid' in request.session:
        ca = tbl_category.objects.get(categoryid=id)
        ca.delete()
        return viewcategory(request)
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def package(request):
    if 'Loginid' in request.session:
        if request.method == "POST":
            pac = tbl_package()
            pac.categoryid = tbl_category.objects.get(categoryid=request.POST.get('categoryid'))
            pac.packagename = request.POST.get('packagename')
            pac.description = request.POST.get('description')
            pac.amount = request.POST.get('amount')
            pac.days = request.POST.get('days')
            if tbl_package.objects.filter(packagename=request.POST.get('packagename')).exists():
                return HttpResponse("<script>alert('Already Exists...');window.location='../package';</script>")
            else:
                pac.save()
                return HttpResponse("<script>alert('Succesfully Added...');window.location='../viewpackage/';</script>")
        else:
            package = tbl_package.objects.all()
            category = tbl_category.objects.all()
            return render(request, 'Admin/package.html', {'package': package, 'category': category})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewpackage(request):
    if 'Loginid' in request.session:
        package = tbl_package.objects.all()
        category = tbl_category.objects.all()
        return render(request, 'Admin/viewpackage.html', {'package': package, 'category': category})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editpackage(request, id):
    if 'Loginid' in request.session:
        if request.method == 'POST':
            categoryname = tbl_category.objects.get(categoryid=request.POST.get('categoryname'))
            packagename = request.POST.get('packagename')
            description = request.POST.get('description')
            amount = request.POST.get('amount')
            days = request.POST.get('days')
            pac = tbl_package.objects.get(packageid=id)
            pac.categoryid = categoryname
            pac.packagename = packagename
            pac.description = description
            pac.amount = amount
            pac.days = days
            pac.save()
            return viewpackage(request)
        pac = tbl_package.objects.get(packageid=id)
        category = tbl_category.objects.all()
        return render(request, 'Admin/editpackage.html', {'pac': pac, 'category': category})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletepackage(request, id):
    if 'Loginid' in request.session:
        pac = tbl_package.objects.get(packageid=id)
        pac.delete()
        return viewpackage(request)
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def service(request):
    if 'Loginid' in request.session:
        if request.method == "POST":
            ser = tbl_service()
            ser.packageid = tbl_package.objects.get(packageid=request.POST.get('packageid'))
            ser.servicename = request.POST.get('servicename')
            ser.serviceamount = request.POST.get('serviceamount')
            if tbl_service.objects.filter(servicename=request.POST.get('servicename')).exists():
                return HttpResponse("<script>alert('Already Exists...');window.location='../service';</script>")
            else:
                ser.save()
                return HttpResponse("<script>alert('Succesfully Added...');window.location='../viewservice/';</script>")
        else:
            service = tbl_service.objects.all()
            package = tbl_package.objects.all()
            return render(request, 'Admin/service.html', {'service': service, 'package': package})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewservice(request):
    if 'Loginid' in request.session:
        service = tbl_service.objects.all()
        package = tbl_package.objects.all()
        return render(request, 'Admin/viewservice.html', {'service': service, 'package': package})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editservice(request, id):
    if 'Loginid' in request.session:
        if request.method == 'POST':
            packagename = tbl_package.objects.get(packageid=request.POST.get('packagename'))
            servicename = request.POST.get('servicename')
            serviceamount = request.POST.get('serviceamount')
            ser = tbl_service.objects.get(serviceid=id)
            ser.packageid = packagename
            ser.servicename = servicename
            ser.serviceamount = serviceamount
            ser.save()
            return viewservice(request)
        ser = tbl_service.objects.get(serviceid=id)
        package = tbl_package.objects.all()
        return render(request, 'Admin/editservice.html', {'ser': ser, 'package': package})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deleteservice(request, id):
    if 'Loginid' in request.session:
        ser = tbl_service.objects.get(serviceid=id)
        ser.delete()
        return viewservice(request)
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Requestbyowners(request):
    if 'Loginid' in request.session:
        Owner = tbl_owner.objects.filter(loginid__status="Requested")
        return render(request, "Admin/Requestbyowners.html", {'ownerrequest': Owner})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def verify(request, id):
    if 'Loginid' in request.session:
        login = tbl_login.objects.get(loginId=id)
        login.status = "Accepted"
        o=tbl_owner.objects.get(loginid=id)
        email=o.email
        #return HttpResponse(email)
        login.save()
        msg = EmailMessage()
        msg.set_content('Your Account has been verified.Now please login to the site.')
        msg['Subject'] = "Account Verification"
        msg['From'] = 'classicgamer622@gmail.com'
        msg['To'] = email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('classicgamer622@gmail.com', 'xirp oknr fuom lltb')
            smtp.send_message(msg)
        return Requestbyowners(request)
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reject(request, id):
    if 'Loginid' in request.session:
        login = tbl_login.objects.get(loginId=id)
        o = tbl_owner.objects.get(loginid=id)
        email = o.email
        login.status = "Rejected"
        login.save()
        msg = EmailMessage()
        msg.set_content('We regret to inform you that ,your request for account verification has been rejected..')
        msg['Subject'] = "Account Rejection"
        msg['From'] = 'classicgamer622@gmail.com'
        msg['To'] = email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('classicgamer622@gmail.com', 'xirp oknr fuom lltb')
            smtp.send_message(msg)
        return Requestbyowners(request)
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewacceptedowners(request):
    if 'Loginid' in request.session:
        Owner = tbl_owner.objects.filter(loginid__status="Accepted")
        return render(request, 'Admin/viewacceptedowners.html', {'ownerrequest': Owner})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def rejected(request, id):
    if 'Loginid' in request.session:
        login = tbl_login.objects.get(loginId=id)
        login.status = "Rejected"
        login.save()
        return viewacceptedowners(request)
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewpayment(request):
    if 'Loginid' in request.session:
        viewpayment = tbl_payment.objects.all()
        view = list(viewpayment.values('paymentamount', 'adminamount', 'requestid__boatid__boatname',
                                       'requestid__boatid__loginid__tbl_owner__ownername', 'customerid__customername'))
        # return HttpResponse(view)
        return render(request, 'Admin/viewpayment.html', {'viewpayment': view})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

def logout(request):
    if "Loginid" in request.session:
        del request.session["Loginid"]
        del request.session['Uname']
        return redirect('/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    logid = request.session.get('Loginid')
    logname = request.session.get('Uname')
    if logid:
        return render(request, "Admin/index.html", {'Loginid': logid, 'Logname': logname})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please loginfirst');window.location='/login';</script>")


def categorypiechart(request):
    labels = []
    data = []
    queryset = tbl_package.objects.values('categoryid__categoryname').annotate(total_boat=Count("packageid"))
    for s in queryset:
        labels.append(s['categoryid__categoryname'])
        data.append(s['total_boat'])
    return render(request, 'Admin/categorypiechart.html', {
        'labels': labels,
        'data': data,
    })

def boatpiechart(request):
    labels = []
    data = []
    # Query to count the number of requests for each boat
    queryset = tbl_request.objects.values('boatid__boatname').annotate(total_requests=Count("boatid")).order_by(
        '-total_requests')[:5] # Get the top 5 most booked boats

    for s in queryset:
        labels.append(s['boatid__boatname'])
        data.append(s['total_requests'])

    return render(request, 'Admin/boatpiechart.html', {
        'labels': labels,
        'data': data,
    })
def Exportcustomerview(request):
    customer = tbl_customer.objects.all()
    return render(request, 'Admin/Exportcustomerview.html', {'customer': customer})

class ExportExcelcustomer(View):
    def get(self, request):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="customerlist.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Sheet1')

        # Define the column headings
        row_num = 0
        columns = ['Customer Name', 'House Name', 'Phone No ', 'Email ID ','Pincode','Registeration Date','District Name','Location Name']
        for col_num, column_title in enumerate(columns):
            ws.write(row_num, col_num, column_title)

        # Query the data from your model, and write it to the worksheet
        queryset = tbl_customer.objects.all().values_list('customername', 'housename', 'phoneno', 'emailid', 'pincode','regdate','locationid__districtid__districtname','locationid__locationname')
        for row in queryset:
            row_num += 1
            for col_num, cell_value in enumerate(row):
                ws.write(row_num, col_num, cell_value)

        wb.save(response)
        return response

def Exportownerview(request):
    owner = tbl_owner.objects.all()
    return render(request, 'Admin/Exportownerview.html', {'owner': owner})

class ExportExcelowner(View):
    def get(self, request):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ownerlist.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Sheet1')

        # Define the column headings
        row_num = 0
        columns = ['Owner Name', 'License Number', 'Contact No ', 'Email ID ','Registeration Date','District Name','Location Name']
        for col_num, column_title in enumerate(columns):
            ws.write(row_num, col_num, column_title)

        # Query the data from your model, and write it to the worksheet
        queryset = tbl_owner.objects.all().values_list('ownername', 'licenseno', 'contactno', 'email','regdate','locationid__districtid__districtname','locationid__locationname')
        for row in queryset:
            row_num += 1
            for col_num, cell_value in enumerate(row):
                ws.write(row_num, col_num, cell_value)

        wb.save(response)
        return response


class ExportExcelDatewiseReport(View):
    def get(self, request):
        return render(request, 'Admin/datewise_boat_report.html')

    def post(self, request):
        from_date_str = request.POST.get('fromdate')
        to_date_str = request.POST.get('todate')

        if not from_date_str or not to_date_str:
            return HttpResponse("Both fromDate and toDate are required.")

        fromdate = datetime.strptime(from_date_str, '%Y-%m-%d').date()
        todate = datetime.strptime(to_date_str, '%Y-%m-%d').date()

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="datewise_report.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Datewise Report')

        row_num = 0
        columns = ['Boat Name', 'Total Boat Requested']
        for col_num, column_title in enumerate(columns):
            ws.write(row_num, col_num, column_title)

        queryset = tbl_request.objects \
            .filter(requestdate__range=(fromdate, todate)) \
            .values('boatid__boatname') \
            .annotate(total_req=Count('requestid'))

        for row in queryset:
            row_num += 1
            for col_num, cell_value in enumerate(row.values()):
                ws.write(row_num, col_num, cell_value)

        wb.save(response)
        return response

def Exportlocationview(request):
    location = tbl_location.objects.all()
    return render(request, 'Admin/Exportlocationview.html', {'location': location})


class ExportExceldistrict(View):
    def get(self, request):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Districtlist.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Sheet1')

        # Define the column headings
        row_num = 0
        columns = ['District Name']
        for col_num, column_title in enumerate(columns):
            ws.write(row_num, col_num, column_title)

        # Query the data from your model, and write it to the worksheet
        queryset = tbl_district.objects.all().values_list('districtname')
        for row in queryset:
            row_num += 1
            for col_num, cell_value in enumerate(row):
                ws.write(row_num, col_num, cell_value)

        wb.save(response)
        return response


def Exportpaymentview(request):
    pay=tbl_payment.objects.all()
    #return HttpResponse(payment)
    payment = list(pay.values('customerid__customername',
                                                     'requestid__boatid__loginid__tbl_owner__ownername',
                                                     'requestid__boatid__boatname', 'paymentamount', 'adminamount',
                                                     'paymentstatus'))
    #return HttpResponse(queryset)
    return render(request, 'Admin/Exportpaymentview.html', {'n': payment})

class ExportExcelpayment(View):
    def get(self, request):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="paymentlist.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Sheet1')

        # Define the column headings
        row_num = 0
        columns = ['Customer Name','Owner Name','Boat Name','Payment Amount','Admin Amount','Payment Status']
        for col_num, column_title in enumerate(columns):
            ws.write(row_num, col_num, column_title)

        # Query the data from your model, and write it to the worksheet
        queryset = tbl_payment.objects.all().values_list('customerid__customername', 'requestid__boatid__loginid__tbl_owner__ownername','requestid__boatid__boatname','paymentamount','adminamount','paymentstatus')
       # return HttpResponse(queryset)
        for row in queryset:
            row_num += 1
            for col_num, cell_value in enumerate(row):
                ws.write(row_num, col_num, cell_value)

        wb.save(response)
        return response


# Create your views here.
