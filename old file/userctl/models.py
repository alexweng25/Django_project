from django.db import models
from django.contrib.auth.models import User
import uuid
import os
from datetime import date
# Create your models here.


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:8], ext)
    sub_folder = 'file'
    if ext.lower() in ["jpg", "png", "gif"]:
        sub_folder = "avatar"
    if ext.lower() in ["pdf", "docx"]:
        sub_folder = "document"
    return os.path.join(instance.user.id, sub_folder, filename)


class SexClass(models.TextChoices):
    MALE = 'Male', '男生'
    FEMALE = 'Female', '女生'
    UN = 'Unknow', '匿性'


class UserInformation(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile', null=True)

    account = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    password2 = models.CharField(max_length=50, null=True)
    fullname = models.CharField(max_length=30)
    birthday = models.DateField(default=date.today)
    # phone = models.(blank=True, help_text='聯絡電話')
    email = models.EmailField(max_length=254)
    sex = models.CharField(
        max_length=10, choices=SexClass.choices, default=SexClass.UN)
    avatar = models.ImageField(
        upload_to=user_directory_path,  blank=True, null=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.account
