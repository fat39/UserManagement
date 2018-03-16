from django.db import models
from rbac.models import User as RbacUser



class UserInfo(models.Model):
    user = models.OneToOneField(RbacUser,on_delete=models.CASCADE)
    nickname = models.CharField(max_length=32,null=True)
    age = models.IntegerField(null=True)
    gender_choice = [
        (1, "男"),
        (2, "女"),
    ]
    gender = models.IntegerField(choices=gender_choice, default=None)
