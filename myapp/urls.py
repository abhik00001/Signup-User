from django.urls import path
from . import views

urlpatterns = [
    path("",views.login_page,name="login_page"),
    path("signup",views.signup,name="signup"),
    path("dashboard",views.dashboard,name="dashboard"),
    path("add_user",views.add_user),
    path("login_user",views.login_user),
    path("logout_user",views.logout_user),
    path("delete_user/<int:id>",views.delete_user),
]
