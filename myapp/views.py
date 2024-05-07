from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required

# Create your views here.

def signup(request):
    return render(request, 'signup.html')

def add_user(request):
    if request.method =="POST":
        user_type = request.POST.get("user_type")
        profile_pic = request.FILES.get("profile_pic")
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        username = request.POST.get("username")
        email = request.POST.get("email")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        pincode = request.POST.get("pincode")
        password = request.POST.get("password")
        Cpassword = request.POST.get("Cpassword")

        if int(pincode)<0:
             messages.warning(request,"Pincode always in positive  number")
             return redirect("signup")

        if password != Cpassword:
            messages.warning(request,"Password doesn't match")
            return redirect("signup")
        
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request,"Username already exists")
            return redirect("signup")
        
        user = CustomUser.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name,profile_pic=profile_pic,user_type=user_type,address=address,city=city,state=state,pincode=pincode)
        
        user.save()
        messages.success(request,"User Added Successfully")
        return redirect("login_page")
    
def login_page(request):
    return render(request,"login.html")

@login_required
def dashboard(request):
             data = CustomUser.objects.filter(username=request.user.username)
             blog_data = blog.objects.filter(is_draft = "False").using("mysql")
             draft_data = blog.objects.filter(author=request.user,is_draft = "True").using("mysql")
             context = {
                 "data":data,
                 "blog_data":blog_data,
                 "draft_data":draft_data,
             }
             return render(request,"dashboard.html",context)

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"Login Successful")
            return redirect("dashboard")
        else:
            messages.warning(request,"Invalid Credentials")
            
            return redirect("login_page")

def logout_user(request):
    logout(request)
    messages.success(request,"Logout successfull")
    return redirect("login_page")

def delete_user(request,id):
     data = CustomUser.objects.filter(id=id)
     data.delete()
     return redirect("login_page")


def add_blog(request):
     if request.method == "POST":
            if "add_blog" in request.POST:
                category = request.POST.get("category")
                blog_image = request.FILES.get("blog_image")
                title = request.POST.get("title")
                summary = request.POST.get("summary")
                content = request.POST.get("content")

                post = blog(category=category,blog_image=blog_image,title=title,summary=summary,Content=content,is_draft ="False",author =request.user)
                post.save(using="mysql")
            
            elif "save_draft" in request.POST:
                category = request.POST.get("category")
                blog_image = request.FILES.get("blog_image")
                title = request.POST.get("title")
                summary = request.POST.get("summary")
                content = request.POST.get("content")

                post = blog(category=category,blog_image=blog_image,title=title,summary=summary,Content=content,is_draft ="True",author=request.user)
                post.save(using="mysql")
            return redirect("dashboard")

def edit_blog(request,id):
     blog_data = blog.objects.filter(id = id).using("mysql")
     context={
          "blog_data":blog_data
     }
     return render(request,"draft.html",context)

def update_draft(request,id):
      drafts = blog.objects.filter(id = id).using("mysql")
      print(drafts)

      if "update_draft" in request.POST:
            category = request.POST.get("category")
            blog_image = request.FILES.get("blog_image")
            title = request.POST.get("title")
            summary = request.POST.get("summary")
            content = request.POST.get("content")

            for draft in drafts:
                draft.category = category
                if blog_image is not None:
                    draft.blog_image = blog_image
                draft.title = title
                draft.summary = summary
                draft.Content = content
                draft.is_draft = "True"
                draft.save(using="mysql")

      elif "add_blog" in request.POST:
            category = request.POST.get("category")
            blog_image = request.FILES.get("blog_image")
            title = request.POST.get("title")
            summary = request.POST.get("summary")
            content = request.POST.get("content")
            post = blog(category=category,blog_image=blog_image,title=title,summary=summary,Content=content,author =request.user)
            post.is_draft = "False"

            post.save(using="mysql")
            drafts.delete()
      return redirect("dashboard")
      

def delete_blog(request,id):
     blog_data = blog.objects.filter(id = id).using("mysql")
     blog_data.delete()
     return redirect("dashboard")