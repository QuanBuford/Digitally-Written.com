from django.db import models
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField(default='Default comment text')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comments') 
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1) 
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50] 

    # def __str__(self):
    #     return f"Comment by {self.author} on {self.post.title}"
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    is_moderator = models.BooleanField(default=False)  # Moderator status
    is_blocked = models.BooleanField(default=False)    # Blocked status
    blocked_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="blocked_users")  # Track who blocked the user
    def __str__(self):
        return f"{self.user.username}'s Profile"