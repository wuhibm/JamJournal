from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(blank=False, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

class Review(models.Model):
    GRADE_CHOICES = {
        "A+":"A+",
        "A":"A",
        "A-":"A-",
        "B+":"B+",
        "B":"B",
        "B-":"B-",
        "C+":"C+",
        "C":"C",
        "C-":"C-",
        "D+":"D+",
        "D":"D",
        "D-":"D-",
        "F":"F"
    }
    album = models.CharField(max_length=100)
    content = models.CharField(max_length=15000)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    likes = models.ManyToManyField(User, blank=True, related_name="liked")
    timestamp = models.DateTimeField(auto_now_add=True)
    grade = models.CharField(choices=GRADE_CHOICES, max_length=3)

    def edit(self, new_content):
        self.content = new_content

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    
class Reply(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="replies")
    replier = models.ForeignKey(User, on_delete=models.CASCADE, related_name="replies")
    content = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
