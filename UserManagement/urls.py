"""UserManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path,re_path
from app01 import views
from app01.auth import auth_views

urlpatterns = [
    # path('admin/', admin.site.urls),
    re_path("^$",auth_views.login),
    re_path("^index.html$",views.index),

    # 登录注册
    re_path("^Login.html$",auth_views.login),
    re_path("^Logout/$",auth_views.logout),
    re_path("^Register.html$",auth_views.register),
    re_path("check_code/",auth_views.check_code),

    # 用户组管理
    re_path("^Group.html$",views.group),
    re_path("^GroupMember.html$",views.groupmember),
    re_path("^GroupAdd/$",views.groupadd),
    re_path("^GroupEdit.html$",views.groupedit),
    re_path("^GroupDel/$",views.groupdel),

    # 用户管理
    re_path("^User.html$",views.user),
    re_path("^UserDetail.html$",views.userdetail),
    re_path("^UserEdit.html$",views.useredit),
    re_path("^UserDel/$",views.userdel),
    re_path("^UserAdd/$",views.useradd),

]
