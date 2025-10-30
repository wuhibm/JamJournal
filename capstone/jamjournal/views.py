from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from dotenv import load_dotenv
import os
import base64
import json
from requests import post, get
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Review, Follow, User, Reply
from math import ceil
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from .tokens import account_activation_token

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization" : "Basic " + auth_base64,
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header():
    token = get_token()
    return {"Authorization" : "Bearer "+token}

# Create your views here.
def index(request):
    page_num = int(request.GET.get('page', 1))
    if page_num < 1 or page_num > 6: page_num = 1
    limit = 18
    offset = (page_num-1)*limit
    url = f"https://api.spotify.com/v1/browse/new-releases/?limit={limit}&offset={offset}"
    headers = get_auth_header()
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return render(request, "jamjournal/index.html", {
        "albums" : json_result["albums"]["items"],
        "page_num":page_num,
        "num_pages": range(6),
        "previous":page_num-1,
        "title":"Featured Albums"
    })

def featured_albums(request):
    url = "https://api.spotify.com/v1/browse/new-releases"
    headers = get_auth_header()
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return JsonResponse(json_result, status=201)

def search(request):
    #TODO: Split up different search types, e.g. artists etc
    if request.method == "POST":
        query = request.POST["query"]
        album_url = f"https://api.spotify.com/v1/search?q={query}&type=album"
        artist_url = f"https://api.spotify.com/v1/search?q={query}&type=artist"
        headers = get_auth_header()
        album_result = get(album_url, headers=headers)
        album_json_result = json.loads(album_result.content)
        albums = album_json_result["albums"]["items"]
        artist_result = get(artist_url, headers=headers)
        artist_json_result = json.loads(artist_result.content)
        artists = artist_json_result["artists"]["items"]
        all_users = User.objects.all()
        users =[]
        for user in all_users:
            if query in user.username:
                users.append(user)
        return render(request, "jamjournal/search.html", {
            "albums" : albums,
            "artists" : artists,
            "users": users,
            "user_results": len(users) > 0
        })
    
def artist(request, artist_id):
    #TODO: pass name instead of api call
    artist_name_url = f"https://api.spotify.com/v1/artists/{artist_id}"
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    headers = get_auth_header()
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    name_result = get(artist_name_url, headers=headers)
    name_json = json.loads(name_result.content)
    return render(request, "jamjournal/index.html", {
        "title": name_json["name"],
        "albums" : json_result["items"],
    })


def album(request, album_id):
    url = f"https://api.spotify.com/v1/albums/{album_id}"
    headers = get_auth_header()
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    reviews = Review.objects.filter(album=album_id)
    average = average_grade(album_id)
    return render(request, "jamjournal/album.html",{
            "album": json_result,
            "reviews": reviews,
            "average": average
        })




@login_required
def user(request):
    user = User.objects.get(username=request.user.username)
    return JsonResponse({"user": user.pk}, status=201)

@login_required
def follow(request, id):
    currUser = User.objects.get(username=request.user.username)
    user = User.objects.get(id=id)
    try:
        relation = Follow.objects.get(follower=currUser, following=user)
        relation.delete()
    except Follow.DoesNotExist:
        new_follow = Follow(follower=currUser, following=user)
        new_follow.save()
    return JsonResponse({"success": True}, status = 204)
    
def follows(request, id):
    user = User.objects.get(pk=id)
    followers = Follow.objects.filter(following= user)
    following = Follow.objects.filter(follower=user)
    return JsonResponse({
        "followers": len(followers),
        "following": len(following)
    }, status=201)


    

@login_required
def review(request, album_id):
    #TODO: Make sure it's one review per album per user
    url = f"https://api.spotify.com/v1/albums/{album_id}"
    headers = get_auth_header()
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        content = request.POST["content"]
        grade = request.POST["grade"]
        if len(content) < 1000:
            Review.objects.create(album=album_id, content=content,grade=grade,reviewer=user)
            return HttpResponseRedirect(reverse("reviews"))
    else:
        return render(request, "jamjournal/review.html",{
            "album": json_result,
            "choices": list(Review.GRADE_CHOICES.keys())
        })
    
def edit(request, review_id):
    review = Review.objects.get(id=review_id)
    if request.method == "POST":
        new_review = request.POST["content"]
        new_grade = request.POST["grade"]
        review.content = new_review
        review.grade = new_grade
        review.save()
        return HttpResponseRedirect(reverse("reviews"))
    else:
        album_id = review.album
        url = f"https://api.spotify.com/v1/albums/{album_id}"
        headers = get_auth_header()
        result = get(url, headers=headers)
        json_result = json.loads(result.content)
        return render(request, "jamjournal/review.html",{
            "album": json_result,
            "content": review.content,
            "grade": review.grade,
            "choices": list(Review.GRADE_CHOICES.keys())
        })
    
def view_review(request, review_id):
    review = Review.objects.get(id=review_id)
    replies = Reply.objects.filter(review=review)
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        if user == None:
            return
        else:
            content = request.POST["content"]
            if len(content) < 1000:
                Reply.objects.create(review=review, replier=user,content=content)
                return HttpResponseRedirect(reverse("view_review", kwargs={'review_id':review_id}))
    else:
        album_id = review.album
        url = f"https://api.spotify.com/v1/albums/{album_id}"
        headers = get_auth_header()
        result = get(url, headers=headers)
        json_result = json.loads(result.content)
        return render(request, "jamjournal/view_review.html", {
            "review": review,
            "album": json_result,
            "replies": replies,
        })

@login_required        
def liked_reviews(request):
    user = User.objects.get(username=request.user.username)
    reviews = Review.objects.all()
    review_ids = []
    for review in reviews:
        if review.likes.contains(user):
            review_ids.append(review.id)
    return JsonResponse(review_ids, safe=False)

def likes(request, review_id):
    review = Review.objects.get(id=review_id)
    likes = review.likes.count()
    return JsonResponse({"likes": likes}, status=201)

@csrf_exempt
@login_required
def like(request):
    if request.method == "POST":
        data = json.loads(request.body)
        review = Review.objects.get(id=int(data["id"]))
        liker = User.objects.get(username=request.user.username)
        if review.likes.contains(liker):
            review.likes.remove(liker)
        else:
            review.likes.add(liker)
        return HttpResponse(status = 204)
    else:
        return HttpResponse(status = 404)

@login_required
def reply(request, review_id):
    pass

#NOTE: ALL RENDER REVIEWS

@login_required
def following(request):
    currUser = User.objects.get(username=request.user.username)
    followed_users = Follow.objects.filter(follower=currUser)
    users = []
    for user in followed_users:
        users.append(user.following)
    all_reviews = get_reviews(users)
    return render(request, "jamjournal/following.html",{
            "all_reviews": all_reviews
        })

@login_required
def my_reviews(request):
    user = User.objects.get(username=request.user.username)
    reviews = Review.objects.filter(reviewer=user)
    all_reviews = get_reviews(user)
    return render(request, "jamjournal/my_reviews.html",{
            "all_reviews": all_reviews
        })

def all_reviews(request):
    reviews = Review.objects.all()
    all_reviews = get_reviews(None)
    return render(request, "jamjournal/all_reviews.html",{
            "reviews": reviews,
            "all_reviews": all_reviews
        })

def profile(request, id):
    #TODO
    user = User.objects.get(id=id)
    reviews = get_reviews(user)
    try:
        currUser = User.objects.get(username=request.user.username)
    except:
        currUser = None
    try:
        followers = len(Follow.objects.filter(following=user))
        following = len(Follow.objects.filter(follower=user))
    except:
        followers = 0
        following = 0 
    if currUser != None: 
        usrFollowing = Follow.objects.filter(follower=currUser, following=user).exists()
    else:
        usrFollowing = False
    flag = currUser != user and currUser != None
    return render(request, "jamjournal/profile.html", {
        "all_reviews": reviews,
        "username": user.username,
        "followers": followers,
        "following":following,
        "flag":flag,
        "usrFollowing": usrFollowing,
    })

def get_reviews(user):
    #TODO: pagination, adjust for rate limit
    reviews = []
    if user == None:
        reviews = Review.objects.all()
    elif type(user) == User:
        reviews = Review.objects.filter(reviewer=user)
    else:
        for review in Review.objects.all():
            if review.reviewer in user:
                reviews.append(review)
    full_reviews = []
    for review in reviews:
        url = f"https://api.spotify.com/v1/albums/{review.album}"
        headers = get_auth_header()
        result = get(url, headers=headers)
        json_result = json.loads(result.content)
        full_reviews.append({
            "review":review,
            "album":json_result,
        })
    return full_reviews

def get_tracks(tracks, total):
    #TODO: Given json result of the tracks of an album, return a list of up to 100 songs
    if total <= 20:
        return tracks
    elif total <=100:
        out_tracks = []
        for i in range(ceil(total/20)):
            next_url = tracks["next"]
            for track in tracks["items"]:
                out_tracks.append(track)
    else:
        pass
    
@login_required
def delete_review(request, review_id):
    currUser = User.objects.get(username=request.user.username)
    review = Review.objects.get(id=review_id)
    if review.reviewer == currUser:
        review.delete()
        return JsonResponse({"success": True},status=201)
    else:
        return JsonResponse({"error": "Cannot delete other people's reviews"}, status=403)

def sendEmail(request, user, to_email):
    mail_subject = "Confirm your email"
    message = f"Hi {user.username} \n Please click on the link below to confirm your registration: \n {"https" if request.is_secure() else "http"}://{get_current_site(request).domain}/activate/{urlsafe_base64_encode(force_bytes(user.pk))}/{account_activation_token.make_token(user)}"
    print(get_current_site(request))
    email = send_mail(mail_subject, message, "jamjournal613@gmail.com",[to_email], fail_silently=False)
    return email


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "jamjournal/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.is_active = False
            user.save()
            if sendEmail(request, user, email):
                return render(request, "jamjournal/confirmation_sent.html")
            else:
                return render(request, "jamjournal/confirmation_error.html", {
                "message": "Could not send confirmation link"
                })
        except IntegrityError:
            return render(request, "jamjournal/register.html", {
                "message": "Username already taken."
            })
        except :
            return render(request, "jamjournal/confirmation_error.html", {
            "message": "Could not send confirmation link"
        })
    else:
        return render(request, "jamjournal/register.html")
    
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active = True
        user.save()
        return render(request, "jamjournal/confirmed.html")
    else:
        return render(request, "jamjournal/confirmation_error.html", {
            "message": "Confirmation link is invalid"
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
            return render(request, "jamjournal/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "jamjournal/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def average_grade(album):
    reviews = Review.objects.filter(album=album)
    if len(reviews) > 0:
        conversions = ["F", "D-", "D", "D+", "C-", "C", "C+", "B-", "B", "B+", "A-", "A", "A+"]
        grades = []
        for review in reviews:
            grades.append(conversions.index(review.grade)+1)
        average = round(sum(grades) / len(grades))
        return conversions[average-1]
    else:
        return "No reviews yet"