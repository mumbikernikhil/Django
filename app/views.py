from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.conf import settings
from .models import *
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage
from django.core import mail
import razorpay
from django.views.decorators.csrf import csrf_exempt



# Create your views here.
def home(request):
    return render(request, 'index.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        query = Contact(name=name, email=email, phone=phone, description=desc)
        query.save()

        # emails
        from_email = settings.EMAIL_HOST_USER
        connection = mail.get_connection()
        connection.open()
        email_message = mail.EmailMessage(f'Email from {name}', f'User Email {email}\nUser Phone_number: {phone}\n\n Query: {desc}', from_email, ['nikhilshirke32@gmail.com'], connection=connection)

        email_client = mail.EmailMessage(f'Response Email', 'Thanks For Reaching Us.\n\nCall_centre_number:111222000\n support@gmail.com', from_email, [email], connection=connection)

        connection.send_messages([email_message, email_client])
        connection.close()

        messages.info(request, 'Thanks For Contacting Us. We Will Get Back To You Shortly')
        return redirect('/contact')
    return render(request, 'contact.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        
        if pass1 == pass2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Exists')
                return redirect('/signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('/signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=pass1)
            user.save()
            messages.success(request, 'User Created')
            return redirect('/signup')
        else:
            messages.info(request, 'Password does not match')
            return redirect('/signup')
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('/login')
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/login')

def handle_blog(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'To Access The Content, You Need To Login First')
        return redirect('/login')
    allPosts = Blog.objects.all()
    context = {
        'allPosts':allPosts
    }
    return render(request, 'blog.html', context)

def search(request):
    query = request.GET['search']
    if len(query) > 100:
        allPosts = Blog.objects.none()
    else:
        allPostsTitles = Blog.objects.filter(title__icontains=query)
        allPostsDescription = Blog.objects.filter(description__icontains=query)
        allPosts = allPostsTitles.union(allPostsDescription)
    if allPosts.count()==0:
        messages.warning(request, 'No Search Results')
    params = {'allPosts':allPosts, 'query':query}
    return render(request, 'search.html', params)

def subscription(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        
        client = razorpay.Client(auth=('rzp_test_NlSkBVS1erkl63', 'wvQerxoTXLjk9084udQRWoI3'))
        payment = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        print(payment)
        subscribe = Subscribe(name=name, amount=amount, payment_id=payment["id"])
        subscribe.save()
        return render(request, 'subscription.html', {'payment':payment})

    return render(request, 'subscription.html')

@csrf_exempt
def success(request):
    if request.method == 'POST':
        a = request.POST
        print(a)
        order_id = ""
        for key,val in a.items():
            if key == "razorpay_order_id":
                order_id = val
                break
        user = Subscribe.objects.filter(payment_id=order_id).first()
        user.paid = True
        user.save()
    return render(request, 'success.html')



# FOR TEST