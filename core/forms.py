from django import forms
from .models import ResumeSubmission

class Resume(forms.ModelForm):
    class Meta:
        model = ResumeSubmission
        fields = ['name', 'email', 'resume_file']
