from django import forms
from .models import ResumeSubmission


class ResumeUploadForm(forms.Form):
    resume_file = forms.FileField(
        label="Upload Resume",
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.docx'
        })
    )

