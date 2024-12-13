import smtplib
from email.message import EmailMessage

from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from Adminapp.models import tbl_category, tbl_package, tbl_service, tbl_location, tbl_district
from Customerapp.models import tbl_request, tbl_payment
from Guestapp.models import tbl_owner, tbl_login, tbl_customer
from Ownerapp.models import tbl_boat
from django.views.decorators.cache import cache_control

@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def customerhome(request):
    if 'Loginid' in request.session:
        c = tbl_category.objects.all()
        return render(request, 'Customer/index.html',{'category': c})

    else:
        return HttpResponse("<script>alert('You have to login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def categoryview(request):
    if 'Loginid' in request.session:
        c = tbl_category.objects.all()
        return render(request, 'Customer/categoryview.html', {'category': c})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def packageview(request, id):
    if 'Loginid' in request.session:
        package = tbl_package.objects.filter(categoryid=id)
        return render(request, 'Customer/packageview.html', {'package': package})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def serviceview(request, id):
    if 'Loginid' in request.session:
        service = tbl_service.objects.filter(packageid=id)
        return render(request, 'Customer/serviceview.html', {'service': service})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewboat(request, id):
    if 'Loginid' in request.session:
        boat = tbl_boat.objects.filter(serviceid=id)
        return render(request, 'Customer/viewboat.html', {'boat': boat})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def boatdetails(request, id):
    if 'Loginid' in request.session:
        boatdetails = tbl_boat.objects.filter(boatid=id).select_related('loginid_tbl_owner__loginid', 'packageid',
                                                                        'serviceid').values('boatid',
                                                                                            'loginid__tbl_owner__ownername',
                                                                                            'loginid__tbl_owner__contactno',
                                                                                            'loginid__tbl_owner__locationid__locationname',
                                                                                            'boatamount',
                                                                                            'packageid__packagename',
                                                                                            'serviceid__servicename',
                                                                                            'serviceid__serviceamount',
                                                                                            'packageid__amount',
                                                                                            'boatname',
                                                                                            'boatimage')
        return render(request, 'Customer/boatdetails.html', {'boatdetails': boatdetails})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def requestdetails(request, id, pa, sa, am):
    if 'Loginid' in request.session:
        # return HttpResponse(id)
        if request.method == 'POST':
            req = tbl_request()
            if tbl_request.objects.filter(fromdate=request.POST.get('fromdate'), boatid=id,
                                          todate=request.POST.get('todate')).exists():
                return HttpResponse("<script>alert('Houseboat Not available');window.location='/Customer/customerhome'</script>")

            # req.ownerid = tbl_owner.objects.get(ownerid=id)
            req.customerid = tbl_customer.objects.get(loginid=request.session['Loginid'])
            req.boatid = tbl_boat.objects.get(boatid=id)
            req.requeststatus = 'Requested'
            req.requestremark = request.POST.get('requestremark')
            req.persons = request.POST.get('persons')
            req.fromdate = request.POST.get('fromdate')
            req.todate = request.POST.get('todate')
            req.totalamount = request.POST.get('totalamount')
            req.save()
            return HttpResponse("<script>alert('Request Sent');window.location='/Customer/categoryview'</script>")

        requestdetails = tbl_boat.objects.filter(boatid=id).select_related('loginid_tbl_owner__loginid', 'packageid',
                                                                           'serviceid').values('packageid__packagename',
                                                                                               'serviceid__servicename',
                                                                                               'boatimage', 'boatname',
                                                                                               'packageid__amount',
                                                                                               'boatamount',
                                                                                               'serviceid__serviceamount')
        pcamt = int(pa)
        bamt = int(sa)
        samt = int(am)
        total = pcamt + bamt + samt
        # return HttpResponse(total)
        return render(request, 'Customer/requestdetails.html', {'requestdetails': requestdetails, 'total': total})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def myorders(request):
    if 'Loginid' in request.session:
        customerid = tbl_customer.objects.get(loginid=request.session.get('Loginid'))
        # return HttpResponse(customerid)
        order = tbl_request.objects.filter(customerid=customerid)
        return render(request, 'Customer/myorders.html', {'order': order})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def payment(request, id):
    if 'Loginid' in request.session:
        if request.method == 'POST':
            pay = tbl_payment()

            pay.adminamount = float(request.POST.get('amount')) * 0.02
            pay.paymentamount = float(request.POST.get('amount')) - pay.adminamount
            pay.requestid = tbl_request.objects.get(requestid=id)
            pay.customerid = tbl_customer.objects.get(loginid=request.session.get('Loginid'))
            pay.paymentstatus = 'Paid'
            pay.save()
            request = tbl_request.objects.get(requestid=id)
            request.requeststatus = "paid"
            request.save()
            Houseboat_email = pay.customerid.emailid
            msg = EmailMessage()
            msg.set_content('Your Payment Succesfully.')
            msg['Subject'] = "Payment Confirmation"
            msg['From'] = 'classicgamer622@gmail.com'
            msg['To'] = Houseboat_email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('classicgamer622@gmail.com', 'xirp oknr fuom lltb')
                smtp.send_message(msg)
            return HttpResponse(
                "<script>alert('Payment Successfully');window.location='/Customer/categoryview'</script>")
        pay = tbl_request.objects.filter(requestid=id)
        payment = list(
            pay.values('requestid', 'totalamount', 'boatid__boatname', 'boatid__loginid__tbl_owner__ownername'))

        # return HttpResponse(payment)

        return render(request, 'Customer/payment.html', {'payment': payment})
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

    if 'Loginid' in request.session:
        return render(request, "Admin/index.html")
    else:
        return HttpResponse(
            "<script>alert('Logout Successfully');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def customerprofile(request):
    if 'Loginid' in request.session:
        id = request.session['Loginid']
        customer = tbl_customer.objects.get(loginid=id)
        idm = customer.customerid
        data = tbl_customer.objects.filter(customerid=idm)
        # name=data.customername
        return render(request, 'Customer/customerprofile.html', {'data': data})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editcustomerprofile(request, id):
    if 'Loginid' in request.session:
        if request.method == "POST":
            cust = tbl_customer.objects.get(customerid=id)
            cust.customername = request.POST.get('customername')
            cust.housename = request.POST.get('housename')
            cust.emailid = request.POST.get('emailid')
            cust.phoneno = request.POST.get('phoneno')
            cust.pincode = request.POST.get('pincode')
            cust.locationid = tbl_location.objects.get(locationid=request.POST.get("locationname"))
            cust.districtid = tbl_district.objects.get(districtid=request.POST.get("districtname"))
            cust.save()
            return HttpResponse(
                "<script>alert('Updation Successfully...');window.location='/Customer/customerprofile/';</script>")
        locview = tbl_location.objects.all()
        distview = tbl_district.objects.all()
        customer = tbl_customer.objects.get(customerid=id)
        return render(request, 'Customer/editcustomerprofile.html',
                      {'customer': customer, 'locationview': locview, 'distview': distview})
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def custlocation(request):
    if 'Loginid' in request.session:
        did = int(request.POST.get("did"))
        # return HttpResponse(did)
        location = tbl_location.objects.filter(districtid=did).values()
        return JsonResponse(list(location), safe=False)
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def changepassword(request):
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
                        "<script>alert('Password Mismatch !!');window.location='/Customerapp/changepassword'</script>")
            else:
                return HttpResponse(
                    "<script>alert('Invalid Username or Password!!');window.location='/Customerapp/changepassword'</script>")
        else:
            return render(request, "Customer/changepassword.html")
    else:
        return HttpResponse(
            "<script>alert('Authentication Required Please login first');window.location='/login';</script>")
