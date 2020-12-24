from django.shortcuts import render , redirect
from django.contrib import messages
import bcrypt
from .models import *

def about(request):
    try:
        current_user = User.objects.get(id = request.session['user_id'])
        context = {
        "user": current_user
            
            }
        return render(request, 'about.html',context )
    except:
        return render(request, 'about.html')

def drivers(request):
    try:
        current_user = User.objects.get(id = request.session['user_id'])
        context = {
        "user": current_user
            
            }
        return render(request, 'drivers.html',context )
    except:
        return render(request, 'drivers.html')

def contact(request):
    try:
        current_user = User.objects.get(id = request.session['user_id'])
        context = {
        "user": current_user
            
            }
        return render(request, 'contact.html',context )
    except:
        return render(request, 'contact.html' )

def registration(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        email = request.POST['email']
        try:
            User.objects.get(email=email)
            messages.error(request, "A user with this email already exists")
            return redirect('/')
        except:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            birthday = request.POST["birthday"]
            phone = request.POST["phone"]
            address = request.POST["address"]
            password = request.POST["password"]
            password = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
            this_user = User.objects.create(first_name = first_name,last_name = last_name, email = email, password = password, phone = phone , address = address , birthday = birthday)
            request.session['user_id'] = this_user.id
            errors["success"] = "Successfully registered (or logged in)!"
            return redirect('/')

def register(request):
    try:
        current_user = User.objects.get(id = request.session['user_id'])
        context = {
        "user": current_user
            
            }
        return render(request, 'about.html',context )
    except:
        return render(request, 'register.html')

def login(request):
    try:
        print ('-' * 30 )
        this_user = User.objects.get(email=request.POST['email'])
        # driver = Driver.objects.get(email=request.POST['email'])
        print ('*' * 30 )
        if this_user:
            print(this_user.password)
            if bcrypt.checkpw(request.POST['password'].encode(), this_user.password.encode()):
                request.session['user_id'] = this_user.id
                print (request.session['user_id'])
                messages.error(request, "Successfully registered (or logged in)!")
                return redirect('/userorder')
            else:
                messages.error(request, "Wrong password")
                return redirect('/')
        # else:
        #     if bcrypt.checkpw(request.POST['password'].encode(), driver.password.encode()):
        #         request.session['user_id'] = driver.id
        #         messages.error(request, "Successfully registered (or logged in)!")
        #         return redirect('/')
        #     else:
        #         messages.error(request, "Wrong password")
        #         return redirect('/')
    except Exception as exp:
        messages.error(request, "Email not found: " + str(exp))
        return redirect('/')

def logout(request):
    del request.session['user_id']
    messages.error(request, "You have successfully logged out")
    return redirect('/')

def userorder(request):
    try:
        current_user = User.objects.get(id = request.session['user_id'])
        context = {
        "user": current_user
            
            }
        return render(request, 'userorder.html',context )
    except:
        return render(request,"userorder.html")

def driverorder(request):
    try:
        current_user = User.objects.get(id = request.session['user_id'])
        context = {
        "user": current_user
            
            }
        return render(request, 'driverorder.html',context )
    except:
        return render(request,"driverorder.html")

def edit_account(request, user_id):
    if request.session['user_id']:
        context = {
        "user": User.objects.get(id=request.session['user_id']),
        }
        return render(request, 'account.html', context)
    else:
        return redirect('/quotes')

def submit(request, user_id):

    selected = User.objects.get(id= request.session['user_id'])
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/editacc/<user_id>')
    else:
        password = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
        selected.first_name = request.POST['first_name']
        selected.last_name = request.POST['last_name']
        selected.email = request.POST['email']
        selected.password = password
        selected.save()
        messages.success(request, "Account successfully updated")
        return redirect('/editacc/<user_id>')