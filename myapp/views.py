from datetime import timedelta
import time
import datetime

from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required

from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import pytz
import json
# from google.oauth2.credentials import Credentials
# import sys


# calendar authentication

import sys
  
scopes = ['https://www.googleapis.com/auth/calendar']

credentials = pickle.load(open("D:/projects/assignment/assignment/token.pkl", "rb"))


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
    if request.user.is_authenticated:
         return redirect("dashboard")
    else:
        return render(request,"login.html")

@login_required
def dashboard(request):
             data = CustomUser.objects.filter(username=request.user.username)
             doctors = CustomUser.objects.filter(user_type= "doctor")
             blog_data = blog.objects.filter(is_draft = "False").using("mysql")
             draft_data = blog.objects.filter(author=request.user,is_draft = "True").using("mysql")

             appointment_data = appointment.objects.filter(user = request.user.username)

             context = {
                 "data":data,
                 "blog_data":blog_data,
                 "draft_data":draft_data,
                 "doctors":doctors,
                 "appointment_data":appointment_data
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


def book_appointment(request,id):
     get_doctor = CustomUser.objects.filter(id=id)
     context = {
          "doc_name" : get_doctor,
     }
     return render(request,"make_appointment.html",context)

def confirm_appointment(request):
        service = build("calendar", "v3", credentials=credentials)
        if request.method == "POST":
            doctor = request.POST.get("doctor_firstname")
            speciality = request.POST.get("speciality")
            date = request.POST.get("date")

            timezone = 'Asia/Kolkata'

            # india_timezone = pytz.timezone('Asia/Kolkata')
            # Serialize timezone object to JSON
            # timezone_json = json.dumps({'timezone': india_timezone.zone})
            email= request.POST.get("email")


            time = request.POST.get("time")

            start = date +' '+ time +':' '00' 
            start_time = datetime.datetime.strptime(start,"%Y-%m-%d %H:%M:%S")
            end_time  = start_time + timedelta(minutes=45)

            doc_name = CustomUser.objects.get(user_type="doctor",first_name = doctor)

            confirm = appointment(user=request.user ,doctor= doc_name , speciality=speciality, date=date, start_time=start_time , end_time = end_time)

            event = (service.events().insert(
                     calendarId="primary",
                     body={
                         "summary": speciality,

                         "start": {"dateTime": start_time.isoformat(),
                         'timeZone': timezone,


                         },
                         "end": {
                             "dateTime": end_time.isoformat(),
                             'timeZone': timezone,
                         },
                         "attendees":[{"email":email}

                         ]
                     },
                 )
                 .execute()
                  )
        
            confirm.save()
            return redirect("dashboard")
        
def cancel_appointment(request,id):
     cancel = appointment.objects.filter(id = id)
     cancel.delete()
     return redirect("dashboard")

# def viewevent(request):
#     service = build("calendar", "v3", credentials=credentials)
#     now = datetime.datetime.utcnow().isoformat() + 'Z' 
#     events_result = service.events().list(calendarId='primary', timeMin=now,
#                                               maxResults=10, singleEvents=True,
#                                               orderBy='startTime').execute()
#     events = events_result.get('items', [])

#     if not events:
#         event_list = 'No upcoming events found.'
#         return redirect("dashboard")

#         # Prints the start and name of the next 10 events
#     for event in events:
#         start = event['start'].get('dateTime', event['start'].get('date'))
#         email = event['attendees'][0:]
#         print(start,email)

#     return render(request,'viewevent.html',)


