from django.shortcuts import render,redirect,HttpResponse
from rbac import models as Rbacmodels
from rbac.service import initial_permission
from app01.myform import RegisterForm,LoginForm
from app01 import models




def login(request):
    if request.method == "GET":
        login_user = LoginForm(request)
        return render(request,"Login.html",{"login_user":login_user})
    else:
        login_user = LoginForm(request,request.POST)
        if login_user.is_valid():
            # obj = models.UserInfo.objects.filter(user__username=login_user.cleaned_data["username"], user__password=login_user.cleaned_data["password"]).first()
            obj = Rbacmodels.User.objects.get(username=login_user.cleaned_data["username"],password=login_user.cleaned_data["password"])
            request.session["user_info"] = {"username":login_user.cleaned_data.get("username")}
            # initial_permission(request, obj.user_id)
            initial_permission(request, obj.id)

            return redirect("/index.html")
        else:
            return render(request, "Login.html", {"login_user": login_user})


def register(request):
    """
    :param request:
    :return:
    """
    if request.method == "GET":
        new_user = RegisterForm(request)
        return render(request,"Register.html",{"new_user":new_user})
    else:
        # 验证码操作
        new_user = RegisterForm(request,request.POST,request.FILES)
        if new_user.is_valid():
            Rbacmodels.User.objects.create(**new_user.cleaned_data)
            return redirect("/Login.html")
        else:
            return render(request,"Register.html",{"new_user":new_user})
            # obj.errors
            # clean方法出错了，err放在__all__



def check_code(request):
    # 读取硬盘中的文件，在页面显示
    # f = open("staticc/imgs/md.jpg","rb")
    # data = f.read()
    # f.close()
    # return HttpResponse(data)

    # from PIL import Image
    # f = open("code.png","wb")
    # img = Image.new(mode="RGB",size=(120,30),color=(255,255,255))
    # img.save(f,"png")
    # f.close()
    # f = open("code.png","rb")
    # data = f.read()
    # f.close()

    # from PIL import Image,ImageDraw,ImageFont
    # from io import BytesIO  # 在内存中开辟一块空间
    # f = BytesIO()  # 写到内存，在内存中开辟一块空间
    # img = Image.new(mode="RGB",size=(120,30),color=(255,255,255))  # 图片对象
    # draw = ImageDraw.Draw(img,mode="RGB")  # 创建画笔对象
    # draw.point([10,10],fill="red")  # 红色
    # draw.point([10,10],fill=(255,255,255))  # RGB颜色
    # draw.line((15,10,50,30),fill="red")  # 画线
    # draw.line((45,20,100,100),fill=(255,0,255))  # 画线
    #
    # draw.arc((0,0,30,30),0,90,fill="red")  # 画圆,0-90度
    #
    # # draw.text([0,0],"python","red")
    #
    # # font = ImageFont.truetype("kumo.ttf",28)
    # # draw.text([0,0],"python",(0,255,0),font=font)
    # import random
    #
    # # char_list = []
    # # for i in range(5):
    # #     char = chr(random.randint(65,90))
    # #     chhar_list.append(char)
    # # "".join(char_list)
    #
    # # v = "".join[chr(random.randint(65,90)) for i in range(5)]
    #
    # char_list = []
    # for i in range(5):
    #     char = chr(random.randint(65,90))
    #     char_list.append(char)
    #     font = ImageFont.truetype("static/myfont/kumo.ttf",28)
    #     draw.text([i*24, 0], char, (random.randint(0,255), random.randint(0,255), random.randint(0,255)), font=font)
    # img.save(f,"png")  # 写到内存
    # data = f.getvalue()
    #
    # code="".join(char_list)
    # request.session["code"] = code
    from io import BytesIO  # 在内存中开辟一块空间
    from utils.random_check_code import rd_check_code
    img,code = rd_check_code()
    stream = BytesIO()
    img.save(stream,"png")  # 图片以png的格式存储到内存stream中
    request.session["code"] = code  # 验证码存储在session中
    return HttpResponse(stream.getvalue())


def logout(request):
    del request.session["user_info"]
    request.session.delete("sessionid")
    return redirect("/Login.html")