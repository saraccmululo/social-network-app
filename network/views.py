from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.db.models import Count
from .models import User, Post, Follow, Like

def index(request):
  if request.method == "POST":
      if not request.user.is_authenticated:
        return redirect("login")
      
      #get data from form
      content=request.POST.get("content").strip()

      #validate data
      if not content:
        messages.error(request, "content cannot be empty")
      if messages.get_messages(request):
        return redirect("index")
      
      #create new post object and save data in db
      Post.objects.create(
          content=content,
          user=request.user
      )
      return redirect("index")
  
  all_posts=Post.objects.annotate(likes_count=Count('likes_received')).order_by("-timestamp")
  
  # Add a "liked" attribute for each post
  for post in all_posts:
    if request.user.is_authenticated:
      post.liked = post.likes_received.filter(user=request.user).exists()
    else:
        post.liked = False
      
  #pagination
  paginator=Paginator(all_posts, 10)
  page_number = request.GET.get('page')
  posts_page = paginator.get_page(page_number)

  return render(request, "network/index.html", {
    "posts_page": posts_page
  })

def profile(request, username):
  #display current profile posts (including like counts)
  current_profile=User.objects.get(username=username)
  user_posts=Post.objects.filter(user=current_profile).annotate(likes_count=Count('likes_received')).order_by("-timestamp")

# Add a "liked" attribute for each post
  for post in user_posts:
    if request.user.is_authenticated:
      post.liked = post.likes_received.filter(user=request.user).exists()
    else:
        post.liked = False

  #filter follow for that profile
  following=Follow.objects.filter(follower=current_profile)
  follower=Follow.objects.filter(following=current_profile)

  #default value for logged-in user not follow itself
  is_following = False

  #check if user follows current_profile
  user=request.user
  if user.is_authenticated and user != current_profile:
      following_check=Follow.objects.filter(follower=user, following=current_profile)
      if following_check.exists():
        is_following=True
      else:
        is_following=False

  #pagination
  paginator=Paginator(user_posts, 10)
  page_number = request.GET.get('page')
  posts_page = paginator.get_page(page_number)

  return render(request, "network/profile.html", {
    "posts_page": posts_page,
    "current_profile": current_profile,
    "following_count": following.count(),
    "followers_count": follower.count(),
    "is_following": is_following
  })

@login_required
def toggle_follow(request, username):
  if request.method == "POST":
    current_profile=User.objects.get(username=username)
    user=request.user

    #check if user=current profile
    if user == current_profile:
      return redirect("profile", username=username)
    
    #check if user follows current_profile
    follow_check=Follow.objects.filter(follower=user, following=current_profile)
    if follow_check.exists():
      #unfollow
      follow_check.delete()
    else:
      #follow
      Follow.objects.create(
         follower=user,
         following=current_profile
      )
    return redirect("profile", username=username)
  
@login_required
def following_feed(request):
  #get all following obj the user follows
  following_objs=Follow.objects.filter(follower=request.user)

  #extract the user profiles the user is following
  following_profiles=[]
  for f in following_objs:
    following_profiles.append(f.following)

  #get all the posts from those profiles (including like counts) 
  posts=Post.objects.filter(user__in=following_profiles).annotate(likes_count=Count('likes_received')).order_by("-timestamp") #user__in = SQL WHERE user_id IN (...).

  # Add a "liked" attribute for each post
  for post in posts:
    post.liked = post.likes_received.filter(user=request.user).exists()

  #pagination
  paginator=Paginator(posts, 10)
  page_number = request.GET.get('page')
  posts_page = paginator.get_page(page_number)

  return render(request, "network/following_feed.html", {
    "posts_page": posts_page
  })

@csrf_exempt
@login_required
def edit(request, post_id):
  if request.method =="PUT":

    #try getting the post (if it exists)
    try:
      post=Post.objects.get(id=post_id)
    except Post.DoesNotExist:
      return JsonResponse({"error": "Post not found"}, status=404)
    
    #Only author can edit post
    if post.user != request.user:
        return JsonResponse({"error": "Only the author can edit this post"})
    
    #Parse incoming json
    try:
      data = json.loads(request.body)
      content=data.get("content", "").strip()
    except:
      return HttpResponseBadRequest("Invalid JSON.")

    if content == "":
       return JsonResponse({"error": "Post content cannot be empty."})
    
    #Save updated content to the db
    post.content = content
    post.save()

    return JsonResponse({"message": "Post updated sucessfully."}, status=200)
  
@csrf_exempt
@login_required
def toggle_like(request, post_id):
  if request.method=="PUT":
    #getting the post with that id
    post = Post.objects.get(id=post_id)

    #check if user already liked the post
    like_check= Like.objects.filter(user=request.user, post=post)

    #toggle logic
    if like_check.exists():
      #unlike
      like_check.delete()
      liked=False
    else:
      #like
      Like.objects.create(user=request.user, post=post)
      liked=True
    
    #count likes
    likes_count=post.likes_received.count()

    return JsonResponse({
      "liked": liked,
      "likes_count": likes_count
    }, status=200)
  
  return JsonResponse({"error": "PUT request required."}, status=400)


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


  
