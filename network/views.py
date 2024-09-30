from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Post, Comment, Like, Follow
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

post_list = []

def index(request):
    posts = Post.objects.all().order_by('-id')
    for post in posts:
        post.likes = Like.objects.filter(post=post).count()
        post.save()
    paginator = Paginator(posts, 10) #Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "current_user": request.user,
        "page_obj": page_obj,
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

def create(request):
    if request.method == 'POST':
        content = request.POST["entry"]
        poster = request.user
        post = Post(poster = poster, content = content)
        post.save()
        post.likes = Like.objects.filter(post=post).count()
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/create.html")
    
def profile(request, id):
    ## Get the user being followed ##
    user = User.objects.get(pk=id)
    followers = Follow.objects.filter(user2=user)
    following = Follow.objects.filter(user1=user)
    posts = Post.objects.filter(poster=id).order_by('-id')
    for post in posts:
        post.likes = Like.objects.filter(post=post).count()
        post.save()

    listofusers = []
    for follow in followers:
        listofusers.append(follow.user1)
    if request.user in listofusers:
        user_follows = True
    else:
        user_follows = False
    paginator = Paginator(posts, 10) #Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/profile.html", {
        "userr": user,
        "followers": followers,
        "following": following,
        "posts": posts,
        "user_follows": user_follows,
        "current_user": request.user,
        "page_obj": page_obj
    })

def follow(request, id):
    user = User.objects.get(pk=id)
    current_user = request.user
    if user != current_user:
        Follow(user1=current_user, user2=user).save()
    else:
        pass
    return HttpResponseRedirect(reverse(profile, kwargs={'id':id}))

def unfollow(request, id):
    user = User.objects.get(pk=id)
    current_user = request.user
    Follow.objects.get(user2=user, user1=request.user).delete()
    return HttpResponseRedirect(reverse(profile, kwargs={'id':id}))

@login_required
def following(request):
    # Get who the user follows
    users=[]
    loloposts=[]
    posts=[]
    user = request.user
    follows = Follow.objects.filter(user1=user)
    for follow in follows:
        users.append(follow.user2)
    for person in users:
        post=Post.objects.filter(poster=person)
        loloposts.append(post)

    # posts is a list of list of posts
    for lopost in loloposts:
        for post in lopost:
            posts.append(post)
    
    posts.reverse()
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
        
    return render(request, "network/following.html", {
        "page_obj": page_obj
    })

def post(request, id):
    post = Post.objects.get(pk=id)
    data = {
        'post_by': post.poster.username,
        'content': post.content
    }
    return JsonResponse(data)

@login_required
@csrf_exempt
def edit_post(request, id):
    try:
        post = Post.objects.get(pk=id)
        poster = post.poster
        if poster != request.user:
            return JsonResponse({"error": "You do not have access to edit this post!"})
        data = json.loads(request.body)
        new_input = data.get("new_input", "")
        post.content = new_input
        post.save()
        return JsonResponse({"message": "Changed Successfully!"})
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

'''
@login_required
@csrf_exempt
def like(request, id):
    user = request.user
    post = Post.objects.get(pk=id)
    data = json.loads(request.body)
    liked = data.get("liked", "").lower()
    if liked == "true":
        Like(post=post, liker=user).save()
        post.likes = Like.objects.filter(post=post).count()
        return JsonResponse({"message": "Liked successfully",
                             "status": "liked"})
    else:
        Like.objects.get(post=post, liker=user).delete()
        return JsonResponse({"message": "Unliked successfully",
                             "status": "unliked"})
'''

## edit this function to send a different response depending on if the user
## already liked the post or not. If the user already liked the post, then 
## it should unlike the post, then create something using javascript that changes
## the value of the button to like or unlike. 


@login_required
@csrf_exempt
def like(request, id):
    user = request.user
    post = Post.objects.get(pk=id)
    # Check if the like exists
    try:
        exists = Like.objects.filter(post=post, liker=user).exists()
        if (exists):
            Like.objects.get(post=post, liker=user).delete()
            post.likes = Like.objects.filter(post=post).count()
            return JsonResponse({"message": "Unliked successfully",
                                 "likes": f"{post.likes}"})
        else:
            Like(post=post, liker=user).save()
            post.likes = Like.objects.filter(post=post).count()
            return JsonResponse({"message" : "Liked successfully",
                                 "likes": f"{post.likes}"})
    except Post.DoesNotExist:
        return JsonResponse({"message":"Post does not exist"})
    

def liked(request, id):
    user = request.user
    post = Post.objects.get(pk=id)
    # Check if the like exists
    exists = Like.objects.filter(post=post, liker=user).exists()
    if (exists):
        post.likes = Like.objects.filter(post=post).count()
        return JsonResponse({"message": "true",
                             "likes": f"{post.likes}"})
    else:
        post.likes = Like.objects.filter(post=post).count()
        return JsonResponse({"message": "false",
                             "likes": f"{post.likes}"})