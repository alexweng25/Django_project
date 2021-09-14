# -*- coding:utf-8 -*-
from django import forms
from .models import Post, Photos

class PostModelForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = '__all__'
		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control'}),
			'content': forms.TextInput(attrs={'class': 'form-control'}),
			'location': forms.TextInput(attrs={'class': 'form-control'}),	
		}
		labels = {
			'title': 'Title',
			'content': 'Content',
			'location': 'Location',
		}

class PostPhotoForm(forms.ModelForm):
	class Meta:
		model = Photos
		fields = ('image',)
		widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control-file' }),
        }
		error_messages = {
            'cover':{
                'invalid_image':'請上傳正確格式的圖片～～',
            },
        }