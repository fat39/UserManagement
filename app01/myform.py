from django.forms import Form,fields,widgets
from django.core.exceptions import ValidationError
from rbac import models as Rbacmodels


class UserAddForm(Form):
    username = fields.CharField(required=True,max_length=32)
    email = fields.EmailField()

    def clean_username(self):
        username = self.cleaned_data["username"]
        if Rbacmodels.User.objects.filter(username=username):
            raise ValidationError("该用户已被占用")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if Rbacmodels.User.objects.filter(email=email):
            raise ValidationError("该邮箱已被占用")
        return email


class RegisterForm(Form):
    username = fields.CharField(widget=widgets.TextInput(attrs={"class":"form-control"}))
    email = fields.EmailField(widget=widgets.TextInput(attrs={"class":"form-control"}))
    password = fields.CharField(widget=widgets.TextInput(attrs={"class":"form-control","type":"password"}))
    password2 = fields.CharField(widget=widgets.TextInput(attrs={"class":"form-control","type":"password"}))
    code = fields.CharField(widget=widgets.TextInput(attrs={"class":"form-control"}))


    # 传入request是为了检查session中的code字段
    def __init__(self,request,*args,**kwargs):  # 传入request
        super(RegisterForm, self).__init__(*args,**kwargs)
        self.request = request


    def clean_code(self):
        input_code = self.cleaned_data["code"]
        session_code = self.request.session.get("code")
        if input_code.upper() != session_code.upper():
            raise ValidationError("验证码错误")
        return input_code

    # 检出用户名是否已被占用
    def clean_username(self):
        username = self.cleaned_data["username"]
        if Rbacmodels.User.objects.filter(username=username):
            raise ValidationError("该用户已被占用")
        return username

    # 检出邮箱是否已被占用
    def clean_email(self):
        email = self.cleaned_data["email"]
        if Rbacmodels.User.objects.filter(email=email):
            raise ValidationError("该邮箱已被占用")
        return email


    def clean(self):
        # 检查两次密码是否一致
        p1 = self.cleaned_data.get("password")
        p2 = self.cleaned_data.get("password2")
        if p1 != p2:
            self.add_error("password2", ValidationError("密码不一致"))
            # raise ValidationError("密码不一致")
        else:
            self.cleaned_data.pop("password2")  # 如果一致，则去除password2，只保留password，为了与数据库字段一致（数据库只有password）
            # return self.cleaned_data
            # return None # 两者均可

        # 如果验证码正确，去除code，目的是与数据库字段一致（数据库没code）
        if self.cleaned_data.get("code"):
            self.cleaned_data.pop("code")
        return self.cleaned_data


class LoginForm(Form):
    username = fields.CharField(widget=widgets.TextInput(attrs={"class": "form-control"}))
    password = fields.CharField(widget=widgets.TextInput(attrs={"class":"form-control","type":"password"}))
    code = fields.CharField(widget=widgets.TextInput(attrs={"class": "form-control"}))

    # 传入request是为了检查session中的code字段
    def __init__(self,request,*args,**kwargs):  # 传入request
        super(LoginForm, self).__init__(*args,**kwargs)
        self.request = request


    def clean_code(self):
        input_code = self.cleaned_data["code"]
        session_code = self.request.session.get("code")
        if input_code.upper() != session_code.upper():
            raise ValidationError("验证码错误")
        return input_code

    def clean(self):
        u = self.cleaned_data.get("username")
        p = self.cleaned_data.get("password")

        if not Rbacmodels.User.objects.filter(username=u,password=p):
            self.add_error("username", ValidationError("用户名或密码"))
            self.add_error("password", ValidationError("用户名或密码"))

        return self.cleaned_data
