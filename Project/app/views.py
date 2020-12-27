from django.shortcuts import render , redirect , HttpResponse
from django.contrib import messages
import bcrypt
from .models import *

def about(request):
    try:
        if "user_id" in request.session:
            current_user = User.objects.get(id = request.session['user_id'])
            context = {
                "user": current_user,
                    
                    }
            return render(request, 'about.html',context )
        else:
            current_driver = Driver.objects.get(id = request.session['driver_id'])
            context = {
            "driver" : current_driver
            
                }
            return render(request, 'about.html',context )
    except:
        return render(request, 'about.html')

def drivers(request):
    try:
        if "user_id" in request.session:
            current_user = User.objects.get(id = request.session['user_id'])
            context = {
                "user": current_user,
                    
                    }
            return render(request, 'drivers.html',context )
        else:
            current_driver = Driver.objects.get(id = request.session['driver_id'])
            context = {
            "driver" : current_driver
            
                }
            return render(request, 'drivers.html',context )
    except:
        return render(request, 'drivers.html')

def contact(request):
    try:
        if "user_id" in request.session:
            current_user = User.objects.get(id = request.session['user_id'])
            context = {
                "user": current_user,
                    
                    }
            return render(request, 'contact.html',context )
        else:
            current_driver = Driver.objects.get(id = request.session['driver_id'])
            context = {
            "driver" : current_driver
            
                }
            return render(request, 'contact.html',context )
    except:
        return render(request, 'contact.html' )

def registration(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register')
    else:
        email = request.POST['email']
        try:
            User.objects.get(email=email)
            messages.error(request, "A user with this email already exists")
            return redirect('/register')
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
            return redirect('/userorder')

def registerdriver(request):
    errors = Driver.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register')
    else:
        email = request.POST['email']
        try:
            Driver.objects.get(email=email)
            messages.error(request, "A user with this email already exists")
            return redirect('/register')
        except:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            birthday = request.POST["birthday"]
            phone = request.POST["phone"]
            address = request.POST["address"]
            password = request.POST["password"]
            # car = request.POST["car"]
            password = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
            this_user = Driver.objects.create(first_name = first_name,last_name = last_name, email = email, password = password, phone = phone , address = address , birthday = birthday)
            request.session['driver_id'] = this_user.id
            errors["success"] = "Successfully registered (or logged in)!"
            return redirect('/driverorder')

def register(request):
    try:
        if request.session:
            current_user = User.objects.get(id = request.session['user_id'])
            current_driver = Driver.objects.get(id = request.session['driver_id'])
            context = {
            "user": current_user,
            "driver" : current_driver
                
                }
        return render(request, 'about.html',context )
    except:
        return render(request, 'register.html')

def login(request):
    try:
        if request.POST["option"] == "user":
            this_user = User.objects.get(email=request.POST['email'])
            print(this_user.password)
            if bcrypt.checkpw(request.POST['password'].encode(), this_user.password.encode()):
                request.session['user_id'] = this_user.id
                print (request.session['user_id'])
                messages.error(request, "Successfully registered (or logged in)!")
                return redirect('/userorder')
            else:
                messages.error(request, "Wrong password")
                return redirect('/')
        if request.POST["option"] == "driver":
            driver = Driver.objects.get(email=request.POST['email'])
            if bcrypt.checkpw(request.POST['password'].encode(), driver.password.encode()):
                request.session['driver_id'] = driver.id
                messages.error(request, "Successfully registered (or logged in)!")
                return redirect('/driverorder')
            else:
                messages.error(request, "Wrong password")
                return redirect('/')
    except Exception as exp:
        messages.error(request, "Email not found: " + str(exp))
        return redirect('/')

def logout(request):
    request.session.clear()
    messages.error(request, "You have successfully logged out")
    return redirect('/')


def userorder(request):
    if "user_id" in request.session:
        current_user = User.objects.get(id = request.session['user_id'])
        myorders = Order.objects.filter(poster=current_user)
        context = {
            "user": current_user ,
            "myorders" : myorders,
                }
        return render(request, 'userorder.html',context )
    else:
        return HttpResponse("<h2>You are not Allowed to View this page</h2>")
def driverorder(request):
    if "driver_id" in request.session:
        current_driver = Driver.objects.get(id = request.session['driver_id'])
        favourites = Order.objects.filter(deliver=current_driver)
        context = {
            "user": current_driver,
            'order_list' : Order.objects.all(),
            "favourites" : favourites
                }
        return render(request, 'driverorder.html',context )
    else:
        return HttpResponse("<h2>You are not Allowed to View this page</h2>")


def edit_account(request, user_id):
    if "user_id" in request.session:
        context = {
        "user": User.objects.get(id=request.session['user_id']),
        }
        return render(request, "account.html", context)
    else:
        return redirect('/')
def edit_accountdriver(request, driver_id):
    if "driver_id" in request.session:
        context = {
        "driver": Driver.objects.get(id=request.session['driver_id']),
        }
        return render(request, 'account.html', context)
    else:
        return redirect('/')

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

def submitdriver(request, driver_id):    
    selected = Driver.objects.get(id= request.session['driver_id'])
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/editaccdriver/{driver_id}')
    else:
        password = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
        selected.first_name = request.POST['first_name']
        selected.last_name = request.POST['last_name']
        selected.email = request.POST['email']
        selected.password = password
        selected.save()
        messages.success(request, "Account successfully updated")
        return redirect(f'/editaccdriver/{driver_id}')

def removeorder(request, order_id):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in!")
        return redirect('/')

    current_user = User.objects.get(id=request.session['user_id'])
    current_Order = Order.objects.get(id = order_id)

    current_Order.delete()

    return redirect('/userorder')

def addorder(request, order_id):
    fav = Driver.objects.get(id = request.session['driver_id'])
    Order.objects.get(id = order_id).deliver.add(fav)
    return redirect('/driverorder')

def doneorder(request, order_id):
    if 'driver_id' not in request.session:
        messages.error(request, "Must be logged in!")
        return redirect('/')

    current_user = Driver.objects.get(id=request.session['driver_id'])
    current_Order = Order.objects.get(id = order_id)
    current_Order.deliver.remove(current_user)

    return redirect('/driverorder')

def post_order(request):
    if request.method == 'POST':
        new_order = Order.objects.create(content = request.POST['order'],poster_id = request.session['user_id'])
        new_order.save()
    return redirect('/userorder')
