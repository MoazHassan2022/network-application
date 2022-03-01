from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, InvalidPage


def index(request):
    if not (request.user.is_authenticated):
        return HttpResponseRedirect(reverse("login"))
    else:
        postList = Post.objects.order_by('-realDate')
        paginator = Paginator(postList, 10)
        try:
            page = int(request.GET.get('page', '1'))
        except:
            page = 1

        try:
            posts = paginator.page(page)
        except(EmptyPage, InvalidPage):
            posts = paginator.page(paginator.num_pages)

        return render(request, "network/index.html", {
            "posts":posts,
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def createPost(request):
    if request.method == "POST":
        text = request.POST["Text"]
        poster = request.user.username
        date0 = datetime.now()
        date = date0.strftime("%B %d, %Y %H:%M:%S")
        newPost = Post(text=text, poster=poster, date=date, likesCount=0)
        newPost.save()
        request.user.posts.add(newPost)
        return HttpResponseRedirect(reverse("index"))

def Profile(request, username):
    us = User.objects.get(username=username)
    postList = us.posts.all().order_by('-realDate')
    other = False
    alreadyFollowed = False
    if request.user.username != username:
        other = True
    fList = request.user.followsList.all()
    for use in fList:
        if username == use.username:
            alreadyFollowed = True

    paginator = Paginator(postList, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        posts = paginator.page(page)
    except(EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)
    return render(request, "network/User's Profile Page.html", {
        "us":us,
        "posts":posts,
        "other":other,
        "alreadyFollowed":alreadyFollowed,
        "fList":fList
    })

def follow(request, username):

    us = User.objects.get(username=username)
    us.followersCount +=1
    us.save()
    request.user.followsList.add(us)
    request.user.followsCount += 1
    request.user.save()
    posts = us.posts.all().order_by('-realDate')
    other = False
    alreadyFollowed = False
    if request.user.username != username:
        other = True
    fList = request.user.followsList.all()
    for use in fList:
        if username == use.username:
            alreadyFollowed = True
    return render(request, "network/User's Profile Page.html", {
        "us": us,
        "posts": posts,
        "other": other,
        "alreadyFollowed": alreadyFollowed,
        "fList": fList
    })
def unfollow(request, username):
    us = User.objects.get(username=username)
    us.followersCount -= 1
    us.save()
    request.user.followsList.remove(us)
    request.user.followsCount -= 1
    request.user.save()
    posts = us.posts.all().order_by('-realDate')
    other = False
    alreadyFollowed = False
    if request.user.username != username:
        other = True
    fList = request.user.followsList.all()
    for use in fList:
        if username == use.username:
            alreadyFollowed = True
    return render(request, "network/User's Profile Page.html", {
        "us": us,
        "posts": posts,
        "other": other,
        "alreadyFollowed": alreadyFollowed,
        "fList": fList
    })

def following(request):
    fList = request.user.followsList.all()
    postList = []
    for f in fList:
        ps = f.posts.all().order_by('-realDate')
        for p in ps:
            postList.append(p)
    paginator = Paginator(postList, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        posts = paginator.page(page)
    except(EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)
    return render(request, "network/following.html", {
        "posts":posts
    })
def Edit(request, id):
    post = Post.objects.get(id=id)
    if request.method == "GET":
        return render(request, "network/Edit.html", {
            "post":post
        })
    elif request.method == "POST":
        post.text = request.POST["newContent"]
        post.save()
        return HttpResponseRedirect(reverse("index"))

def like(request, id):
    post = Post.objects.get(id=id)
    liked = request.user.LikedList.all()
    alreadyLiked = False
    for po in liked:
        if id == po.id:
            alreadyLiked = True
    if alreadyLiked == False:
        request.user.LikedList.add(post)
        post.likesCount += 1
        post.save()
    return HttpResponseRedirect(reverse("index"))

def unlike(request, id):
    post = Post.objects.get(id=id)
    liked = request.user.LikedList.all()
    alreadyLiked = False
    for po in liked:
        if id == po.id:
            alreadyLiked = True
    if alreadyLiked:
        request.user.LikedList.remove(post)
        post.likesCount -= 1
        post.save()
    return HttpResponseRedirect(reverse("index"))
def likeFollowing(request, id):
    post = Post.objects.get(id=id)
    liked = request.user.LikedList.all()
    alreadyLiked = False
    for po in liked:
        if id == po.id:
            alreadyLiked = True
    if alreadyLiked == False:
        request.user.LikedList.add(post)
        post.likesCount += 1
        post.save()
    return HttpResponseRedirect(reverse("following"))

def unlikeFollowing(request, id):
    post = Post.objects.get(id=id)
    liked = request.user.LikedList.all()
    alreadyLiked = False
    for po in liked:
        if id == po.id:
            alreadyLiked = True
    if alreadyLiked:
        request.user.LikedList.remove(post)
        post.likesCount -= 1
        post.save()
    return HttpResponseRedirect(reverse("following"))
