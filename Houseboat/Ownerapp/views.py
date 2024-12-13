import smtplib

from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from Adminapp.models import tbl_package, tbl_service, tbl_category, tbl_location, tbl_district
from Ownerapp.models import tbl_boat
from Guestapp.models import tbl_login, tbl_owner, tbl_customer
from Customerapp.models import tbl_request
from django.views.decorators.cache import cache_control
from email.message import EmailMessage

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ownerhome(request):
    if 'Loginid' in request.session:
        return render(request, 'Owner/index.html')
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def boatreg(request):
    if 'Loginid' in request.session:
        if request.method == 'POST':
            boatid = request.POST.get('boatid')
            if tbl_boat.objects.filter(boatid=boatid).exists():
                return HttpResponse("<script>alert('Already Exists...');window.location='../boatreg';</script>")
            if len(request.FILES) != 0:
                cimage = request.FILES['boatimage']
            else:
                cimage = 'default.jpeg'
            # return HttpResponse(name+" "+desc+" "+cimage)
            boat = tbl_boat()
            boat.boatimage = cimage
            boat.boatname = request.POST.get('boatname')
            boat.boatamount = request.POST.get('boatamount')
            boat.categoryid = tbl_category.objects.get(categoryid=request.POST.get('categoryid'))
            boat.packageid = tbl_package.objects.get(packageid=request.POST.get('packageid'))
            boat.serviceid = tbl_service.objects.get(serviceid=request.POST.get('serviceid'))
            boat.loginid = tbl_login.objects.get(loginId=request.session['Loginid'])
            boat.save()
            return HttpResponse("<script>alert('Boat Registered..');window.location ='../viewboat';</script>")


        else:
            category = tbl_category.objects.all()
            package = tbl_package.objects.all()
            service = tbl_service.objects.all()

            return render(request, 'Owner/boatreg.html', {'package': package, 'service': service, 'category': category})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewboat(request):
    if 'Loginid' in request.session:
        boat = tbl_boat.objects.filter(loginid=request.session.get('Loginid'))
        c = tbl_category.objects.all()
        p = tbl_package.objects.all()
        s = tbl_service.objects.all()
        return render(request, 'Owner/viewboat.html', {'boat': boat, 'package': p, 'service': s, 'category': c})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editboat(request, id):
    if 'Loginid' in request.session:
        if request.method == 'POST':
            category = tbl_category.objects.get(categoryid=request.POST.get('categoryname'))
            package = tbl_package.objects.get(packageid=request.POST.get('packagename'))
            service = tbl_service.objects.get(serviceid=request.POST.get('serviceid'))
            boat = tbl_boat.objects.get(boatid=id)
            boatname = request.POST.get('boatname')
            boatamount = request.POST.get('boatamount')
            if len(request.FILES) == 0:
                bimage = request.POST.get('oldimg')
            else:
                bimage = request.FILES['image']
            boat.boatimage = bimage
            boat.categoryid = category
            boat.packageid = package
            boat.serviceid = service
            boat.boatname = boatname
            boat.boatamount = boatamount
            boat.save()
            return viewboat(request)
        d = tbl_boat.objects.get(boatid=id)
        category = tbl_category.objects.all()
        package = tbl_package.objects.all()
        service = tbl_service.objects.all()
        return render(request, 'Owner/editboat.html',
                      {'boat': d, 'package': package, 'service': service, 'category': category})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deleteboat(request, id):
    if 'Loginid' in request.session:
        boat = tbl_boat.objects.get(boatid=id)
        boat.delete()
        return viewboat(request)
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def choosepackage(request):
    if 'Loginid' in request.session:
        did = int(request.POST.get("did"))
        packageid = tbl_package.objects.filter(categoryid=did).values()
        return JsonResponse(list(packageid), safe=False)
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def chooseservices(request):
    if 'Loginid' in request.session:
        did = int(request.POST.get("did"))
        package = tbl_service.objects.filter(packageid=did).values()
        return JsonResponse(list(package), safe=False)
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def fillcategory(request):
    if 'Loginid' in request.session:
        boat = tbl_boat.objects.filter(loginid=request.session.get('Loginid'))
        categoryid = int(request.POST.get("catid"))
        category = tbl_boat.objects.filter(categoryid=categoryid,
                                           loginid=request.session.get('Loginid')).select_related(
            'loginid_tbl_owner__loginid', 'serviceid', 'packageid').values(
            'packageid__packagename', 'serviceid__servicename', 'boatname', 'boatamount', 'boatimage', 'boatid')
        return JsonResponse(list(category), safe=False)
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editchoosepackage(request):
    if 'Loginid' in request.session:
        packid = int(request.POST.get("packid"))
        packageid = tbl_package.objects.filter(categoryid=packid).values()
        return JsonResponse(list(packageid), safe=False)
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editchooseservices(request):
    if 'Loginid' in request.session:
        serid = int(request.POST.get("serid"))
        package = tbl_service.objects.filter(packageid=serid).values()
        return JsonResponse(list(package), safe=False)
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def requestbycustomers(request):
    if 'Loginid' in request.session:
        loginid = request.session.get('Loginid')
        owner_instance = tbl_login.objects.get(loginId=loginid)
        owner_boats = tbl_boat.objects.filter(loginid=owner_instance)
        customer_requests = tbl_request.objects.filter(boatid__in=owner_boats, requeststatus="Requested")

        return render(request, "Owner/requestbycustomers.html",
                      {'customer_requests': customer_requests})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def verifycustomer(request, id):
    if 'Loginid' in request.session:
        req = tbl_request.objects.get(requestid=id)
        req.requeststatus = "Accepted"
        cu=req.customerid
        email=cu.emailid
        #return HttpResponse(email)
        req.save()
        msg = EmailMessage()
        msg.set_content('Your Booking has been verified,your request for booking verification has been accepted..')
        msg['Subject'] = "Booking Verification"
        msg['From'] = 'classicgamer622@gmail.com'
        msg['To'] = email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('classicgamer622@gmail.com', 'xirp oknr fuom lltb')
            smtp.send_message(msg)
        return requestbycustomers(request)
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def rejectcustomer(request, id):
    if 'Loginid' in request.session:
        req = tbl_request.objects.get(requestid=id)
        cu = req.customerid
        email = cu.emailid
        req.requeststatus = "Rejected"
        req.save()
        msg = EmailMessage()
        msg.set_content('We regret to inform you that ,your request for booking verification has been rejected..')
        msg['Subject'] = "Booking Rejection"
        msg['From'] = 'classicgamer622@gmail.com'
        msg['To'] = email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('classicgamer622@gmail.com', 'xirp oknr fuom lltb')
            smtp.send_message(msg)
        return requestbycustomers(request)
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewacceptedcustomers(request):
    if 'Loginid' in request.session:
        loginid = request.session.get('Loginid')
        owner_instance = tbl_login.objects.get(loginId=loginid)
        ownerboats = tbl_boat.objects.filter(loginid=owner_instance)
        customerrequest = tbl_request.objects.filter(boatid__in=ownerboats, requeststatus="Accepted")
        return render(request, 'Owner/viewacceptedcustomers.html', {'customerrequest': customerrequest})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def rejectedcustomers(request, id):
    if 'Loginid' in request.session:
        req = tbl_request.objects.get(requestid=id)
        req.requeststatus = "Rejected"
        req.save()
        return viewacceptedcustomers(request)
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def paymentview(request):
    if 'Loginid' in request.session:
        loginid = request.session.get('Loginid')
        owner_instance = tbl_login.objects.get(loginId=loginid)
        ownerboat = tbl_boat.objects.filter(loginid=owner_instance)
        paymentview = tbl_request.objects.filter(boatid__in=ownerboat, requeststatus="Paid")
        return render(request, 'Owner/paymentview.html', {'paymentview': paymentview})
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
            "<script>alert('Logout Successfully');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ownerchangepassword(request):
    if 'Loginid' in request.session:
        if request.method == 'POST':
            uname = request.POST.get("username")
            password = request.POST.get("password")
            newpwd = request.POST.get("newpwd")
            connewpwd = request.POST.get("connewpwd")

            if tbl_login.objects.filter(username=uname, password=password).exists():
                lo = tbl_login.objects.get(username=uname, password=password)
                if newpwd == connewpwd:
                    lo.password = newpwd
                    lo.save()
                    return HttpResponse(
                        "<script>alert('Successfully updated!!');window.location='/login'</script>")
                else:
                    return HttpResponse(
                        "<script>alert('Password Mismatch !!');window.location='/Ownerapp/ownerchangepassword'</script>")
            else:
                return HttpResponse(
                    "<script>alert('Invalid Username or Password!!');window.location='/Ownerapp/ownerchangepassword'</script>")
        else:
            return render(request, "Owner/ownerchangepassword.html")
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ownerprofile(request):
    if 'Loginid' in request.session:
        id = request.session['Loginid']
        owner = tbl_owner.objects.get(loginid=id)
        idm = owner.ownerid
        owner = tbl_owner.objects.filter(ownerid=idm)
        # name=data.customername
        return render(request, 'Owner/ownerprofile.html', {'owner': owner})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editownerprofile(request, id):
    if 'Loginid' in request.session:
        if request.method == "POST":
            own = tbl_owner.objects.get(ownerid=id)
            own.ownername = request.POST.get('ownername')
            own.licenseno = request.POST.get('licenseno')
            own.email = request.POST.get('email')
            own.contactno = request.POST.get('contactno')
            own.pincode = request.POST.get('pincode')
            own.locationid = tbl_location.objects.get(locationid=request.POST.get("locationname"))
            own.districtid = tbl_district.objects.get(districtid=request.POST.get("districtname"))
            own.save()
            return HttpResponse(
                "<script>alert('Updation Successfully...');window.location='/Owner/ownerprofile/';</script>")
        locview = tbl_location.objects.all()
        distview = tbl_district.objects.all()
        owner = tbl_owner.objects.get(ownerid=id)
        return render(request, 'Owner/editownerprofile.html',
                      {'owner': owner, 'locationview': locview, 'distview': distview})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ownlocation(request):
    if 'Loginid' in request.session:
        did = int(request.POST.get("did"))
        # return HttpResponse(did)
        location = tbl_location.objects.filter(districtid=did).values()
        return JsonResponse(list(location), safe=False)
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

# Create your views here.
