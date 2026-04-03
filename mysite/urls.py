"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from views import depart,user,pretty,account,admin
urlpatterns = [
    # path('admin/', admin.site.urls),
    #部门管理
    path('depart/list/',depart.depart_list),
    path('depart/add/',depart.depart_add),
    path('depart/delete/',depart.depart_delete),
    path('depart/<int:nid>/edit/',depart.depart_edit),
    #用户管理
    path('user/list/',user.user_list),
    path('user/add/',user.user_add),
    path('user/model/form/add/',user.user_model_form_add),
    path("user/<int:nid>/edit/",user.user_edit),
    path("user/<int:nid>/delete/",user.user_delete),
    #优质号码管理
    path('prettynum/list/',pretty.prettynum_list),
    path('prettynum/add/',pretty.prettynum_add),
    path('prettynum/<int:nid>/edit/',pretty.prettynum_edit),
    path('prettynum/<int:nid>/delete/',pretty.prettynum_delete),
    #管理员管理
    path ('admin/list/',admin.admin_list),
    path('admin/add/', admin.admin_add),
    path('admin/<int:nid>/edit/', admin.admin_edit),
    path('admin/<int:nid>/delete/', admin.admin_delete),
    path('admin/<int:nid>/reset/', admin.admin_reset),
    #登录
    path('login/',account.login),
    path('logout/',account.logout)

]
