# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import Post, Photos
from .forms import PostModelForm, PostPhotoForm
from datetime import datetime


def Mainpage(request):
    post = Post.objects.all()
    return render(request, 'Mainpage.html', {'post_list': post})


def Daily_detail(request, num):
    post = get_object_or_404(Post, id=num)
    return render(request, 'post_detail.html', {'post': post})


def Add_New(request):
    posts = Post.objects.all()  # 查詢所有資料
    form = PostModelForm()
    if request.method == "POST":
        form = PostModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/trips/AddNew")

    return render(request, 'AddNew.html', {'post_list': posts, 'form': form})


def Update(request, num):
    post = get_object_or_404(Post, id=num)
    form = PostModelForm(instance=post)

    if request.method == 'POST':
        form = PostModelForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("/trips/AddNew")
    context = {'form': form}
    return render(request, 'Update.html', context)


def Delete(request, num):
    post = get_object_or_404(Post, id=num)

    if request.method == "POST":
        post.delete()
        return redirect("/trips/AddNew")

    context = {'posts_item': post}
    return render(request, 'Delete.html', context)


def Test(request):
    return render(request, 'Test.html')


def ImageView(request):
    form = PostPhotoForm()
    images = Photos.objects.all()  # 查詢所有資料
    if request.method == "POST":
        form = PostPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/trips/ImgCtl')

    context = {'form': form,
               'photos': images}
    return render(request, 'ImgCtl.html', context)
