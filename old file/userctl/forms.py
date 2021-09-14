from django import forms
from .models import UserInformation
from django.contrib.auth.models import User
from django.contrib import auth


class LoginForm(forms.ModelForm):
    class Meta:
        model = UserInformation
        fields = ('account', 'password')
        widgets = {
            'account': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Account'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        }
        labels = {
            'account': 'Account',
            'password': 'Password',
        }

    def clean_account(self):
        username = self.cleaned_data.get('account')
        filter_result = User.objects.filter(username__exact=username)
        if not filter_result:
            raise forms.ValidationError('Account is not exist.')

        return username

    def clean_password(self):
        username = self.cleaned_data.get('account')
        password = self.cleaned_data.get('password')
        user = auth.authenticate(
            username=username, password=password)
        filter_result = User.objects.filter(username__exact=username)
        if user is None and filter_result:
            raise forms.ValidationError('Password is wrong.')

        return password


class RegisterForm(forms.ModelForm):
    class Meta:
        model = UserInformation
        exclude = ['user']
        widgets = {
            'account': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Account'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Confirmation'}),
            'fullname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control', 'id': 'birthdatepicker'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'mail@anyserver.com'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
        labels = {
            'account': '帳號',
            'password': '密碼',
            'password2': '密碼驗證',
            'fullname': '姓名',
            'email': '信箱',
            'avatar': '頭像',
            'birthday': '生日',
            'sex': '性別',
        }

    def clean_account(self):
        account = self.cleaned_data.get('account')
        if len(account) < 3:
            raise forms.ValidationError(
                "account must be at least 3 characters log")
        elif len(account) > 15:
            raise forms.ValidationError("account is too long")
        else:
            filter_result = User.objects.filter(username__exact=account)
            if len(filter_result) > 0:
                raise forms.ValidationError('account already exists')

        return account

    def clean_password(self):
        password1 = self.cleaned_data.get('password')
        if len(password1) < 3:
            raise forms.ValidationError("password is too short")
        elif len(password1) > 15:
            raise forms.ValidationError("password is too long")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                'Password mismatch. Please enter again')

        return password2


class ProfileForm(RegisterForm):
    class Meta(RegisterForm.Meta):
        exclude = ('user', 'account', 'password', 'password2',)
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control', 'id': 'birthdatepicker'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control-file'}),
        }


class PasswordForm(forms.Form):
    old_password = forms.CharField(
        label='舊密碼', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '舊密碼'}))

    password1 = forms.CharField(
        label='新密碼', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '新密碼'}))
    password2 = forms.CharField(
        label='新密碼驗證', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '新密碼驗證'}))

    # use clean methods to define custom validation rules

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        # password = self.cleaned_data.get('password')
        # user = auth.authenticate(
        #     username=username, password=password1)
        # filter_result = User.objects.filter(username__exact=username)
        # if user is None and filter_result:
        #     raise forms.ValidationError('Password is wrong.')

        if len(password1) < 3:
            raise forms.ValidationError("your password is too short")
        elif len(password1) > 15:
            raise forms.ValidationError("your password is too long")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password mismatch Please enter again")

        return password2
