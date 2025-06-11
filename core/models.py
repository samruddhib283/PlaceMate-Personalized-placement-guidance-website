from django.db import models
from django.contrib.auth.models import User

class InterviewQuestion(models.Model):
    question = models.TextField()
    level = models.CharField(max_length=20)  # easy, medium, hard
    keywords = models.TextField(help_text="Comma-separated keywords")

    def get_keywords_list(self):
        return [kw.strip().lower() for kw in self.keywords.split(',') if kw.strip()]

    def __str__(self):
        return f"{self.level.title()} - {self.question[:50]}"

class InterviewResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    level = models.CharField(max_length=20)  # easy, medium, hard
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.level} - {self.timestamp.strftime('%d-%m-%Y %H:%M')}"

class Opportunity(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    apply_link = models.URLField()
    last_date = models.DateField()

    def __str__(self):
        return self.title

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Fix: link to user for identifying owner
    name = models.CharField(max_length=100)
    email = models.EmailField()
    resume_file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Resume"
