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

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import InterviewResponse
import random
from openai import OpenAI
import tempfile

# Initialize OpenAI client
client = OpenAI(api_key = "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")  # Use env var in prod!)

#openai.api_key = "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"  # Use env var in prod!

questions = {
    'easy': [
        "What is Python?",
        "Explain the difference between a list and a tuple.",
        "What is a function?",
        "What are variables in Python?",
        "What is indentation in Python and why is it important?",
        "What are Python data types?",
        "What is the difference between '==' and 'is' in Python?",
        "How do you write a for loop in Python?",
        "What is the purpose of the 'len()' function?",
        "What is a dictionary in Python?"
    ],
    'medium': [
        "What are the four pillars of Object Oriented Programming?",
        "Explain database normalization.",
        "What is REST API?",
        "What are *args and **kwargs in Python?",
        "How does exception handling work in Python?",
        "Explain list comprehensions with an example.",
        "What is the difference between a shallow copy and a deep copy?",
        "How do you manage packages and dependencies in Python?",
        "What is a virtual environment in Python?",
        "Explain the concept of decorators with an example."
    ],
    'hard': [
        "Explain multithreading and multiprocessing in Python.",
        "How does Django ORM work internally?",
        "Design a scalable system for an online exam portal.",
        "Explain how Python's garbage collection works.",
        "What are metaclasses in Python and where would you use them?",
        "Describe how you would implement caching in a Django application.",
        "How do you ensure the security of a Django-based web app?",
        "What is the Global Interpreter Lock (GIL) in Python?",
        "Explain how to scale a Python web application to support thousands of users.",
        "How would you optimize a slow SQL query from Django?"
    ]
}

@login_required
def voice_interview(request):
    return render(request, 'core/voice_interview.html')


@login_required
def get_question(request, level):
    level = level.lower()
    selected_questions = questions.get(level, [])
    if not selected_questions:
        return JsonResponse({'question': 'No questions found for this level.'})
    question = random.choice(selected_questions)
    return JsonResponse({'question': question})


@csrf_exempt
@login_required
def submit_audio_answer(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        level = request.POST.get('level')

        transcript = None

        if 'audio' in request.FILES:
            audio_file = request.FILES['audio']
            try:
                # Save file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                    for chunk in audio_file.chunks():
                        temp_audio.write(chunk)
                    temp_audio_path = temp_audio.name

                transcript_response = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=open(temp_audio_path, "rb")
                )
                transcript = transcript_response.text.strip()

            except Exception as e:
                return JsonResponse({'feedback': f"Transcription failed: {str(e)}"})

        else:
            return JsonResponse({'feedback': 'No audio file uploaded.'})

        feedback = get_gpt_feedback(question, transcript)

        InterviewResponse.objects.create(
            user=request.user,
            question=question,
            answer=transcript,
            level=level
        )

        return JsonResponse({'feedback': feedback, 'transcript': transcript})

    return JsonResponse({'error': 'Invalid request method.'})


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
@login_required
def submit_answer(request):
    if request.method == "POST":
        # Expect JSON since frontend sends JSON via fetch
        import json
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        question = data.get("question")
        answer = data.get("answer")
        level = data.get("level")

        if not (question and answer and level):
            return JsonResponse({'error': 'Missing form data.'}, status=400)

        feedback = get_gpt_feedback(question, answer)

        InterviewResponse.objects.create(
            user=request.user,
            question=question,
            answer=answer,
            level=level
        )

        return JsonResponse({'feedback': feedback})

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

def get_gpt_feedback(question, answer):
    try:
        prompt = (
            f"You are an AI interviewer evaluating a candidate's answer.\n"
            f"Question: {question}\n"
            f"Candidate's Answer: {answer}\n\n"
            f"Instructions:\n"
            f"- Provide clear, structured feedback.\n"
            f"- Mention strengths, gaps, and improvement suggestions.\n"
            f"- If grammar, clarity, or structure is off (e.g., for transcribed audio), mention that too.\n"
            f"- Conclude with an overall rating: 'Excellent', 'Good', 'Needs Improvement', or 'Try Again'."
            f"- Make the summarized response in paragraph from user engaging and interactive "
        )
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use "gpt-4" or "gpt-4o" if desired
            messages=[
                {"role": "system", "content": "You are an expert technical interviewer who provides honest, clear feedback."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )

        feedback = response.choices[0].message.content.strip()
        return feedback

    except Exception as e:
        print(f"[ERROR] GPT Feedback Failed: {str(e)}")  # Log for server-side debugging
        return "⚠️ AI feedback generation failed. Please try again later."

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


import os
import openai
from django.conf import settings
from django.shortcuts import render
from .forms import ResumeUploadForm
from PyPDF2 import PdfReader
from docx import Document


client = OpenAI(api_key=settings.OPENAI_API_KEY)

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    return " ".join(page.extract_text() or "" for page in reader.pages)

def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join(p.text for p in doc.paragraphs)

def resume_review(request):
    feedback = None

    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['resume_file']
            if file.name.endswith('.pdf'):
                text = extract_text_from_pdf(file)
            elif file.name.endswith('.docx'):
                text = extract_text_from_docx(file)
            else:
                feedback = "Unsupported file format. Please upload PDF or DOCX."
                return render(request, 'core/resume_review.html', {'form': form, 'feedback': feedback})

            # Call OpenAI API
            prompt = f"Give professional resume feedback and suggestions for the following resume in 2 paragraph:\n\n{text}"
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                    {"role": "system", "content": "You're a career expert who gives resume review feedback."},
                    {"role": "user", "content": prompt}
                    ],
                    max_tokens=200
                )

                feedback = response.choices[0].message.content
            except Exception as e:
                feedback = f"Error generating feedback: {str(e)}"

    else:
        form = ResumeUploadForm()

    return render(request, 'core/resume_review.html', {'form': form, 'feedback': feedback})



#job search and results
import requests


def job_search_view(request):
    return render(request, 'core/job_results.html')

def job_results_view(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        job_type = request.POST.get('job_type')
        location = request.POST.get('location') or ""
        remote = request.POST.get('remote') or ""
        min_salary = request.POST.get('min_salary') or ""

        query = f"{role} {job_type} {remote} {location}"

        url = "https://jsearch.p.rapidapi.com/search"

        querystring = {
            "query": query,
            "country": "IN",
            "page": "1",
        }

        if min_salary:
            querystring["min_salary"] = min_salary

        headers = {
            "X-RapidAPI-Key": "6332cd49d6mshead4f7241f7a3a7p1ef956jsn481c1ce12933",
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        jobs = []
        if response.status_code == 200:
            data = response.json()
            jobs = data.get("data", [])
        else:
            print("Error:", response.status_code, response.text)

        return render(request, 'core/job_results.html', {
            'jobs': jobs,
            'role': role,
            'job_type': job_type,
            'location': location,
            'remote': remote,
            'min_salary': min_salary,
        })

    return render(request, 'core/job_search.html')