from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    # Home & Search
    path('', views.index, name='index'),
    
    # Job Details
    path('job/<int:pk>/', views.job_detail, name='job_detail'),
    path('company/<int:pk>/', views.company_detail, name='company_detail'),
    
    # Job Management
    path('job/create/', views.create_job, name='create_job'),
    path('job/<int:pk>/edit/', views.edit_job, name='edit_job'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # User Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('my-bookmarks/', views.my_bookmarks, name='my_bookmarks'),
    
    # Job Application
    path('apply/<int:pk>/', views.apply_job, name='apply_job'),
    path('job/<int:pk>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
]
