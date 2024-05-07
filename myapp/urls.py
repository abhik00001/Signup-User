from django.urls import path
from . import views

urlpatterns = [
    # user signup and login
    path("",views.login_page,name="login_page"),
    path("signup",views.signup,name="signup"),
    path("dashboard",views.dashboard,name="dashboard"),
    path("add_user",views.add_user),
    path("login_user",views.login_user),
    path("logout_user",views.logout_user),
    path("delete_user/<int:id>",views.delete_user),

    #blog post and get
    path("add_blog",views.add_blog),
    path("edit_blog/<int:id>",views.edit_blog),
    path("delete_blog/<int:id>",views.delete_blog),
    path("update_draft/<int:id>",views.update_draft),
]
