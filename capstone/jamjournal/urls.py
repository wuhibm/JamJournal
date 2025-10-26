from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("featured", views.featured_albums, name="featured"),
    path("review/<str:album_id>", views.review, name="review"),
    path("my_reviews", views.my_reviews, name="my_reviews"),
    path("reviews", views.all_reviews, name="reviews"),
    path("search", views.search, name="search"),
    path("album/<str:album_id>", views.album, name="album"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("artist/<str:artist_id>", views.artist, name="artist"),
    path("following", views.following, name="following"),
    path("edit/<int:review_id>", views.edit, name="edit"),
    path("view_review/<int:review_id>", views.view_review, name="view_review"),
    path("activate/<uidb64>/<token>", views.activate, name="activate"),

    #API endpoints
    path('user', views.user, name="user"),
    path('follows/<int:id>', views.follows, name="follows"),
    path('follow/<int:id>', views.follow, name="follow"),
    path('delete/<int:review_id>', views.delete_review, name="delete"),
    path('like', views.like, name="like"),
    path('likes/<int:review_id>', views.likes, name="likes"),
    path('liked_reviews', views.liked_reviews, name="liked_reviews"),
]