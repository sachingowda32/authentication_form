from django.shortcuts import render,redirect
from .forms import signupForm,identifyuser
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,SetPasswordForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail,EmailMessage
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.encoding import force_str,force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode

# Create your views here.
def resetpasswordview(request,en_uname):
    dc_name = force_str(urlsafe_base64_decode(en_uname))
    user = User.objects.get(username=dc_name)
    if request.method=='POST':
        form = SetPasswordForm(user=user,data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'password reset successfull')
            return redirect('login')
        else:
            messages.error(request,'password reset failed')
            return redirect('login')
    form = SetPasswordForm(user=user)
    return render(request,'passwordreset.html',{'form':form})

def identifyuserview(request):
    if request.method == 'POST': 
        form = identifyuser(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                email = User.objects.get(username=username).email
                en_uname = urlsafe_base64_encode(force_bytes(username))
                url = 'http://127.0.0.1:8000/resetpassword/'+en_uname+'/'
                send_mail(
                    subject='Password Reset Request',
                    message=f'Click the link to reset your password: {url}',
                    from_email='sachingowda741517@gmail.com',
                    recipient_list=[email],
                    fail_silently=True
                )
                messages.success(request,'Password reset link sent to your email')
                return redirect('login') 
            else:
                messages.error(request,'User not Exist')
    form = identifyuser()
    return render(request,'identifyuser.html',{'form': form})            
def update_pasword(request):
    user = User.objects.get(username = request.user.username)
    if request.method == 'POST':
        form = PasswordChangeForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'password update successful')
            return redirect('logout')
    form = PasswordChangeForm(user=user)
    return render(request,'update_pwd.html',{'form':form})    

def signupview(request):
    if request.method == 'POST':
        fm = signupForm(request.POST)
        if fm.is_valid():
            fm.save()
            email = fm.cleaned_data.get('email')
            fname = fm.cleaned_data.get('first_name')
            lname = fm.cleaned_data.get('last_name')
            username = fm.cleaned_data.get('username')
            if email:
                    send_mail(
                        subject='Account Registration Successful - Welcome to Django Email Service',
                        message=f'''Dear {fname} {lname}
Thank you for registering with us!
We're excited to confirm that your account {username} has been successfully created. You can now log in and start using our services.
• Account Name: {username}
                                                            
Best regards,
Django Email Team''',
                        from_email='sachingowda741517@gmail.com',
                        recipient_list=[email],
                        fail_silently=True

                        )
            return redirect('login')
    fm = signupForm()
    context = {
        'form': fm
    }
    return render(request,'signup.html',context)
def login_view(request):
    if request.method == 'POST':
        fm = AuthenticationForm(request,data=request.POST)
        if fm.is_valid():
            username = fm.cleaned_data.get('username')
            password = fm.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                #if user.is_authenticated: or
                login(request,user)
                messages.success(request,' logged successfully') # message go to redirect page in that page we print this message
                return redirect('home')
            else:
                return HttpResponse('Invalid username or password') 
        else:
            return HttpResponse('Invalid username or password')
    else:
        fm = AuthenticationForm()

    return render(request, 'login.html', {'form': fm})

def logoutview(request):
    #user=request.POST.get('username')
    logout(request)
    messages.error(request,'you are logged out successfully')
    return redirect('login')    
@login_required(login_url='/login/') # if it login it redirect and show message otherwise it redirect to login_url
def home(request):
    return render(request,'home.html')

def send_email_view(request):
    email = request.POST.get('email')
    if email:
        send_mail(
            subject='Django Sample',
            message='Consider a project named geeksforgeeks having an app named geeks.',
            from_email='sachingowda741517@gmail.com',
            recipient_list=[email],
            fail_silently=True
        )
        return HttpResponse('Email sent')
    else:
        return HttpResponse('No email provided')

'''def send_email_view2(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if email and subject and message:
            send_mail(
                subject=subject,    
                message=message,
                from_email='sachingowda741517@gmail.com',
                recipient_list=[email],
                fail_silently=True
            )
            return HttpResponse('Email sent')
        else:
            return HttpResponse('Missing fields')
    return render(request, 'Email.html')'''

def send_email_view2(request):
    if request.method == 'POST':
        from_email=request.POST.get('from')
        to_email = request.POST.get('to')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        cc=request.POST.get('cc')
        if cc:
            cc=cc.split(',')
        else:
            cc=[]
        mail = EmailMessage( 
            subject,
            message,
            from_email,
            [to_email],
            cc=cc

        )
        mail.send(fail_silently=True)
        return HttpResponse('Mail Sent')

    return render(request, 'Email.html')

def 