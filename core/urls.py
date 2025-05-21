from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('voice_interview/', views.voice_interview, name='voice_interview'),
    path('get_question/<str:level>/', views.get_question, name='get_question'),
    path('submit_answer/', views.submit_answer, name='submit_answer'),  
    path('latest-opportunities/', views.latest_opportunities, name='latest_opportunities'),
    path('opportunities/', views.all_opportunities, name='all_opportunities'),
    path('calm-zone/', views.calm_zone, name='calm_zone'),
    path('upload-resume/', views.upload_resume, name='upload_resume'),
   
    

]

