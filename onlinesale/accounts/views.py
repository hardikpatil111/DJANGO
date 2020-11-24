from django.shortcuts import render,redirect
from .forms import RegisterForm,SignInForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.utils.http import is_safe_url

User = get_user_model()

def signout_page(request):
    logout(request)
    return redirect("/")

def signin_page(request):
    signinform = SignInForm(request.POST or None)
    redirect_path=request.POST.get("next_url") or None
    context = {
        'signinform':signinform
    }
    if signinform.is_valid():
        user=authenticate(username=signinform.data.get('username'),password=signinform.data.get('pwd'))
        if user:
            login(request,user)
            if redirect_path is not None:
                if is_safe_url(redirect_path,request.get_host()):
                    return redirect(redirect_path)
            return redirect("home")
            #return redirect("/")
        else:
            context["errMsg"]="Invalid credentials"
    return render(request,"accounts/login.html",context)




def register_page(request):
    if request.method =="POST":
        form = RegisterForm(request.POST)
    
    else:
        form = RegisterForm()
        #form=RegisterForm(request.POST or None)
    context={'form':form}
    if form.is_valid():
           email=form.data.get('email')
           fn=form.data.get('fullname')
           mobile=form.data.get('mobile')
           pwd=form.data.get('pwd')
           user = User.objects.create_user(email=email,password=pwd,full_name=fn,mobile=mobile)
           
           if user:
               context['msg'] = "User created successfully"
               context['form'] = RegisterForm()
           else:
                context['msg'] ="Something went wrong try again"

    return render(request,"accounts/register.html",context)
# Create your views here.
