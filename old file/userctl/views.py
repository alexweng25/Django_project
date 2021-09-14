# Create your views here.
import getopt
from datetime import datetime

from django import forms
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User
from trips.models import Post

from .forms import LoginForm, RegisterForm, ProfileForm, PasswordForm
from .models import UserInformation
# 登入裝飾器
from django.contrib.auth.decorators import login_required


def Login(request):
    if request.session.get('is_login', None):  # 不允許重複登錄
        # request.session['is_login'] = False
        return redirect("/")

    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        # form = LoginForm(request.POST)
        if form.is_valid():  # 驗證資料是否正確
            account = form.cleaned_data['account']
            password = form.cleaned_data['password']

            user = auth.authenticate(
                username=account, password=password)

            if not user.is_active:
                message = '用戶凍結'
                return render(request, 'Userlogin.html', locals())

            # 自訂義使用者資料表

            userprofile = UserInformation.objects.get(account=account)
            request.session['is_login'] = True
            request.session['user_id'] = userprofile.id
            request.session['user_name'] = userprofile.fullname

            auth.login(request, user)

            return redirect("/")

    return render(request, 'Userlogin.html', locals())


def Logout(request):
    if not request.session.get('is_login', None):
        return redirect("/")
    # 內建登出
    auth.logout(request)

    # 一次清除，會影響全部已經登入的使用者，包括管理員
    # request.session.flush()

    # 獨立清除
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']

    return redirect("/")


def Register(request):
    form = RegisterForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['account']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']
            avatar = form.cleaned_data['avatar']

            # 內建User, create_user方法建立用戶，不使用save()
            user = User.objects.create_user(
                username=username, password=password, email=email)

            # 存userprofile
            userinfo = form.save(commit=False)
            userinfo.user = user
            userinfo.save()

            # 轉址到登入畫面
            return redirect("/userctl/login")

    return render(request, 'Userregister.html', {'form': form})


@login_required
def ProfileEdit(request):
    if not request.session.get('is_login', None):
        return redirect("/userctl/login")

    # get取得模型
    userinfo = UserInformation.objects.get(pk=request.session['user_id'])
    form = ProfileForm(request.POST or None,
                       request.FILES or None, instance=userinfo)
    if request.method == 'POST':
        if form.is_valid():
            # 使用者資料更新
            form.save()
            # userinfo = UserInformation.objects.filter(user=user)
            # userinfo.update(fullname=form.cleaned_data['fullname'])
            # userinfo.update(email=form.cleaned_data['email'])
            # userinfo.update(birthday=form.cleaned_data['birthday'])
            # if form.cleaned_data['avatar'] is not None:
            #     userinfo.update(avatar=form.cleaned_data['avatar'])

            return redirect("/userctl/profile", locals())

    return render(request, 'UserProfile.html', locals())


def PasswordEdit(request):
    if not request.session.get('is_login', None):
        return redirect("/userctl/login")

    userinfo = UserInformation.objects.get(pk=request.session['user_id'])
    user = get_object_or_404(User, username=userinfo.user)
    # filter取得 queryset模型集合
    userinfo = UserInformation.objects.filter(user=user)

    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            # 舊密碼驗證，應該要改成在modelform執行驗證
            password = form.cleaned_data['old_password']
            username = user.username
            user = auth.authenticate(username=username, password=password)
            # 密碼更新，
            if user is not None and user.is_active:
                # 模型: 使用者資料
                userinfo.update(password=form.cleaned_data['password2'])
                # 模型: 使用者帳戶
                new_password = form.cleaned_data['password2']
                user.set_password(new_password)
                user.save()
                message = '修改成功'
            else:
                form.add_error("password1", "舊密碼錯誤，請重新輸入")
                # message = '舊密碼錯誤，請重新輸入'
            return render(request, 'UserPassword.html', locals())

    else:
        form = PasswordForm()

    return render(request, 'UserPassword.html', locals())
