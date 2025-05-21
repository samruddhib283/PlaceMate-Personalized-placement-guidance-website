from django.db import models
from django.contrib.auth.models import User


class InterviewResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    level = models.CharField(max_length=20)  # easy, medium, hard
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.level} - {self.timestamp.strftime('%d-%m-%Y %H:%M')}"


from django.db import models

class Opportunity(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    apply_link = models.URLField()
    last_date = models.DateField()

    def __str__(self):
        return self.title


from django.db import models

class SuccessStory(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    story = models.TextField()
    image = models.ImageField(upload_to='stories/', blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.position}"

class ResumeSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    resume_file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Resume"

