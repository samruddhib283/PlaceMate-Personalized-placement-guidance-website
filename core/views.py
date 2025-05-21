from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
import random
from .models import InterviewResponse
from .models import SuccessStory

def home(request):
    return render(request, 'core/home.html')

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        
        messages.success(request, "Account created successfully!")
        return redirect('dashboard')
    return render(request, 'core/signup.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('login')
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')  


from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    return render(request, 'core/dashboard.html')


def voice_interview(request):
    return render(request, 'core/voice_interview.html')

from django.http import JsonResponse
import random

questions = {
    'easy': [
        "What is Python?",
        "Explain the difference between a list and a tuple.",
        "What is a function?"
    ],
    'medium': [
        "What are the four pillars of Object Oriented Programming?",
        "Explain database normalization.",
        "What is REST API?"
    ],
    'hard': [
        "Explain multithreading and multiprocessing in Python.",
        "How does Django ORM work internally?",
        "Design a scalable system for an online exam portal."
    ]
}

def get_question(request, level):
    selected_questions = questions.get(level.lower(), [])
    if selected_questions:
        question = random.choice(selected_questions)
        return JsonResponse({'question': question})
    else:
        return JsonResponse({'question': 'No questions found for this level.'})



# Handle Submitted Answer
def submit_answer(request):
    if request.method == 'POST':
        user_answer = request.POST.get('answer')
        question = request.POST.get('question')
        level = request.POST.get('level')

        # Save to database
        InterviewResponse.objects.create(
            user=request.user,
            question=question,
            answer=user_answer,
            level=level
        )

        return redirect('dashboard')
    else:
        return redirect('dashboard')
    

# views.py
from .models import Opportunity
from datetime import date

def latest_opportunities(request):
    today = date.today()
    opportunities = Opportunity.objects.filter(last_date__gte=today).order_by('last_date')[:5]
    return render(request, 'core/latest_opportunities.html', {
        'opportunities': opportunities
    })

def all_opportunities(request):
    today = date.today()
    opportunities = Opportunity.objects.filter(last_date__gte=today).order_by('last_date')
    return render(request, 'core/all_opportunities.html', {
        'opportunities': opportunities
    })


def dashboard_view(request):
    stories = SuccessStory.objects.order_by('-created_at')[:5]  # Last 5 stories
    return render(request, 'core/dashboard.html', {'stories': stories})

def calm_zone(request):
    return render(request, 'core/calm_zone.html')



from django.shortcuts import render, redirect
from .forms import ResumeSubmission

def upload_resume(request):
    feedback = None

    if request.method == 'POST':
        form = ResumeSubmission(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            # Simple AI-like feedback (placeholder)
            feedback = [
                "Consider adding an 'Objective' or 'Professional Summary'.",
                "Highlight key technical and soft skills.",
                "Add projects or internships with bullet points.",
                "Include quantified achievements if any.",
                "Make sure formatting is consistent and clean."
            ]
    else:
        form = ResumeSubmission()

    return render(request, 'core/resume_review.html', {'form': form, 'feedback': feedback})


