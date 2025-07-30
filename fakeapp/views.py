
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .middleware import auth, guest




# Create your views here.
def Home(request):
    return render(request,"base.html")

def Aboutus(request):
    return render(request, "aboutus.html", {'show_navbar': False})

def Service(request):
    return render(request, 'service.html')

def Modifications(request):
    return render(request,'modifications.html')

def Accessories(request):
    return render(request,'accessories.html')

def Contactus(request):
    if request.method=="POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name, email, phone, content)

        message_body = f"""
                Name: {name}
                Email: {email}
                Phone: {phone}
                Message: {content}
                """

        send_mail(
            subject='Contact Form Submission',
            message=message_body,
            from_email = settings.EMAIL_HOST_USER,
            recipient_list=['achinni29@gmail.com'],  # Replace with where you want to receive messages
            fail_silently=False,
        )


        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill all the fields Correctly")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your form has been submitted Successfully")

    return render(request, 'contactus.html')

@guest
def Register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        initial_data = {'username':'','password1':'','password2':''}
        form = UserCreationForm(initial=initial_data)
    return render(request, 'register.html',{'form': form})

@guest
def Login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        initial_data = {'username': '', 'password': ''}
        form = AuthenticationForm(initial=initial_data)
    return render(request, 'login.html', {'form': form})

@auth
def Dashboard(request):
    return render(request, 'dashboard.html')

def Logout(request):
    logout(request)
    return redirect('login')





