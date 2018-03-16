from django.shortcuts import render,redirect,HttpResponse
from rbac import models as Rbacmodels
from app01 import myform
from app01 import models

# Create your views here.



def index(request):
    return render(request,"index.html")

# def layout(request):
#     if request.method == "GET":
#         return render(request,"layout.html")


def group(request):
    group_list = Rbacmodels.Group.objects.all()
    u2g_list = Rbacmodels.User2Group.objects.all()
    return render(request,"Group.html",{
        "group_list":group_list,
        "u2g_list":u2g_list,
    })

def groupadd(request):
    if request.method == "GET":
        return render(request,"GroupAdd.html")
    else:
        usergroup = request.POST.get("usergroup")
        if Rbacmodels.Group.objects.filter(caption=usergroup):
            err_msg = "用户组已存在"
            return render(request,"GroupAdd.html",{"err_msg":err_msg})
        Rbacmodels.Group.objects.create(caption=usergroup)
        return redirect("/Group.html")

def groupmember(request):
    if request.method == "GET":
        gid = request.GET.get("gid")
        caption = request.GET.get("caption")
        user_list = Rbacmodels.User.objects.filter(groups__group_id=gid)

        return render(request,"GroupMember.html",{"user_list":user_list,"caption":caption})

def groupedit(request):
    if request.method == "GET":
        gid = request.GET.get("gid")
        caption = request.GET.get("caption")
        users_list = Rbacmodels.User.objects.all()
        member_list = Rbacmodels.User.objects.filter(groups__group_id=gid)

        return render(request,"GroupEdit.html",{
            "gid":gid,
            "caption":caption,
            "users_list":users_list,
            "member_list":member_list,
        })
    else:
        gid = request.GET.get("gid")
        caption = request.POST.get("caption")
        member_list = request.POST.getlist("member_list")
        if Rbacmodels.Group.objects.filter(caption=caption).exclude(id=gid):
            err_msg = "用户组已存在"
            return render(request,"GroupEdit.html",{"err_msg":err_msg})
        else:
            Rbacmodels.Group.objects.filter(id=gid).update(caption=caption)
            Rbacmodels.User2Group.objects.filter(group_id=gid).delete()
            member_objs_list = []
            for member in member_list:
                member_objs_list.append(Rbacmodels.User2Group(group_id=gid,user_id=member))
            Rbacmodels.User2Group.objects.bulk_create(member_objs_list)
            return redirect("/Group.html")


def groupdel(request):
    if request.method == "GET":
        gid = request.GET.get("gid")
        Rbacmodels.Group.objects.filter(id=gid).delete()
        return redirect("/Group.html")


def user(request):
    if request.method == "GET":
        user_list = Rbacmodels.User.objects.all()
        u2g_list = Rbacmodels.User2Group.objects.all()
        return render(request,"User.html",{
            "user_list":user_list,
            "u2g_list":u2g_list,
        })

def useradd(request):
    if request.method == "GET":
        obj = myform.UserAddForm()
        return render(request,"UserAdd.html",{"obj":obj})
    else:
        obj = myform.UserAddForm(request.POST)
        if obj.is_valid():
            Rbacmodels.User.objects.create(**obj.cleaned_data)
            return redirect("/User.html")
        else:
            return render(request,"UserAdd.html",{"obj":obj})


def userdetail(request):
    if request.method == "GET":
        uid = request.GET.get("uid")
        user_obj = Rbacmodels.User.objects.filter(id=uid)[0]
        group_obj_list = Rbacmodels.Group.objects.filter(users__user_id=uid)
        # userinfo = models.UserInfo.objects.filter(id=uid)[0] if models.UserInfo.objects.filter(id=uid) else None
        return render(request,"UserDetail.html",{
            "user_obj":user_obj,
            "group_obj_list":group_obj_list
        })

def useredit(request):
    if request.method == "GET":
        uid = request.GET.get("uid")
        user_obj = Rbacmodels.User.objects.filter(id=uid)[0]
        my_group_list = Rbacmodels.Group.objects.filter(users__user_id=uid)
        usergroup_list = Rbacmodels.Group.objects.all()
        return render(request,"UserEdit.html",{
            "user_obj":user_obj,
            "my_group_list": my_group_list,
            "usergroup_list":usergroup_list,
        })
    else:
        uid = request.GET.get("uid")
        username = request.POST.get("uname")
        email = request.POST.get("email")
        usergroup_list = request.POST.getlist("ugroup")
        Rbacmodels.User.objects.filter(id=uid).update(username=username,email=email)
        Rbacmodels.User2Group.objects.filter(user_id=uid).all().delete()
        g_objs_list = []
        for gid in usergroup_list:
            g_objs_list.append(Rbacmodels.User2Group(user_id=uid,group_id=gid))
        Rbacmodels.User2Group.objects.bulk_create(g_objs_list)

        return redirect("/User.html")

def userdel(request):
    if request.method == "GET":
        uid = request.GET.get("uid")
        Rbacmodels.User.objects.filter(id=uid).delete()
        return redirect("/User.html")


