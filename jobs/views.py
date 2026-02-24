from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Job, Company, Application, Bookmark, UserProfile
from django.http import JsonResponse
from .forms import JobForm, CustomUserCreationForm, UserLoginForm


# ==================== Home & Search Views ====================

def index(request):
    """Display job portal homepage with search and filters"""
    jobs = Job.objects.filter(is_active=True).select_related('company')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) |
            Q(company__name__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    # Filter by job type
    job_type = request.GET.get('job_type', '')
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    
    # Filter by experience level
    experience = request.GET.get('experience', '')
    if experience:
        jobs = jobs.filter(experience_level=experience)
    
    # Filter by location
    location = request.GET.get('location', '')
    if location:
        jobs = jobs.filter(location__icontains=location)
    
    # Filter by salary range
    min_salary = request.GET.get('min_salary', '')
    max_salary = request.GET.get('max_salary', '')
    if min_salary:
        jobs = jobs.filter(salary_min__gte=int(min_salary))
    if max_salary:
        jobs = jobs.filter(salary_max__lte=int(max_salary))
    
    # Pagination
    paginator = Paginator(jobs, 6)  # 6 jobs per page
    page_number = request.GET.get('page', 1)
    jobs_page = paginator.get_page(page_number)
    
    # Get available filters for the form
    job_types = Job.objects.values_list('job_type', flat=True).distinct()
    experience_levels = Job.objects.values_list('experience_level', flat=True).distinct()
    locations = Job.objects.values_list('location', flat=True).distinct()
    
    context = {
        'jobs': jobs_page,
        'search_query': search_query,
        'job_types': job_types,
        'experience_levels': experience_levels,
        'locations': locations,
        'selected_type': job_type,
        'selected_experience': experience,
        'selected_location': location,
    }
    return render(request, 'jobs/index.html', context)


# ==================== Job Detail View ====================

def job_detail(request, pk):
    """Display individual job details"""
    job = get_object_or_404(Job, pk=pk, is_active=True)
    job.increment_views()  # Track view count
    
    # Check if user has bookmarked
    is_bookmarked = False
    has_applied = False
    
    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(user=request.user, job=job).exists()
        has_applied = Application.objects.filter(user=request.user, job=job).exists()
    
    # Get other jobs from same company
    related_jobs = job.company.jobs.filter(is_active=True).exclude(pk=pk)[:3]
    
    context = {
        'job': job,
        'company': job.company,
        'is_bookmarked': is_bookmarked,
        'has_applied': has_applied,
        'related_jobs': related_jobs,
    }
    return render(request, 'jobs/job_detail.html', context)


# ==================== Company Profile View ====================

def company_detail(request, pk):
    """Display company profile with all jobs"""
    company = get_object_or_404(Company, pk=pk)
    jobs = company.jobs.filter(is_active=True)
    
    # Pagination
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page', 1)
    jobs_page = paginator.get_page(page_number)
    
    # Company stats
    total_jobs = jobs.count()
    total_applications = Application.objects.filter(job__company=company).count()
    
    context = {
        'company': company,
        'jobs': jobs_page,
        'total_jobs': total_jobs,
        'total_applications': total_applications,
    }
    return render(request, 'jobs/company_detail.html', context)


# ==================== Authentication Views ====================

@require_http_methods(["GET", "POST"])
def register(request):
    """User registration view with form validation"""
    if request.user.is_authenticated:
        return redirect('jobs:index')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created.')
            return redirect('jobs:index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()
    
    context = {'form': form}
    return render(request, 'jobs/register.html', context)


@require_http_methods(["GET", "POST"])
def user_login(request):
    """User login view with form validation"""
    if request.user.is_authenticated:
        return redirect('jobs:index')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('jobs:index')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    context = {'form': form}
    return render(request, 'jobs/login.html', context)


@login_required(login_url='jobs:login')
def user_logout(request):
    """User logout view"""
    logout(request)
    return redirect('jobs:index')


# ==================== User Dashboard Views ====================

@login_required(login_url='jobs:login')
def my_applications(request):
    """View user's job applications"""
    applications = Application.objects.filter(user=request.user).select_related('job', 'job__company')
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(applications, 10)
    page_number = request.GET.get('page', 1)
    apps_page = paginator.get_page(page_number)
    
    context = {
        'applications': apps_page,
        'status_choices': Application.STATUS_CHOICES,
        'selected_status': status_filter,
    }
    return render(request, 'jobs/my_applications.html', context)


@login_required(login_url='jobs:login')
def my_bookmarks(request):
    """View user's bookmarked jobs"""
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('job', 'job__company')
    
    # Pagination
    paginator = Paginator(bookmarks, 10)
    page_number = request.GET.get('page', 1)
    bookmarks_page = paginator.get_page(page_number)
    
    context = {'bookmarks': bookmarks_page}
    return render(request, 'jobs/my_bookmarks.html', context)


# ==================== Application Views ====================

@login_required(login_url='jobs:login')
@require_http_methods(["GET", "POST"])
def apply_job(request, pk):
    """Apply for a job with email notification"""
    job = get_object_or_404(Job, pk=pk)
    
    # Check if already applied
    if Application.objects.filter(user=request.user, job=job).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('jobs:job_detail', pk=job.pk)
    
    if request.method == 'POST':
        resume = request.FILES.get('resume')
        cover_letter = request.POST.get('cover_letter', '')
        
        if not resume:
            messages.error(request, 'Resume is required.')
            return render(request, 'jobs/apply.html', {'job': job})
        
        # Create application
        application = Application.objects.create(
            user=request.user,
            job=job,
            resume=resume,
            cover_letter=cover_letter
        )
        
        # Send email notification to job poster
        if job.posted_by and job.posted_by.email:
            subject = f'New Application for {job.title}'
            message = f"""
Hi {job.posted_by.first_name or job.posted_by.username},

A new applicant has applied for your job posting: {job.title}

Applicant: {request.user.first_name} {request.user.last_name} ({request.user.username})
Email: {request.user.email}

You can view the application details in your dashboard.

Best regards,
Job Portal Team
            """
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [job.posted_by.email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Error sending email: {e}")
        
        messages.success(request, 'Your application has been submitted successfully!')
        return redirect('jobs:my_applications')
    
    return render(request, 'jobs/apply.html', {'job': job})


# ==================== Bookmark Views ====================

@login_required(login_url='jobs:login')
def toggle_bookmark(request, pk):
    """Toggle bookmark for a job"""
    job = get_object_or_404(Job, pk=pk)
    
    bookmark = Bookmark.objects.filter(user=request.user, job=job).first()
    
    if bookmark:
        bookmark.delete()
        is_bookmarked = False
    else:
        Bookmark.objects.create(user=request.user, job=job)
        is_bookmarked = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'is_bookmarked': is_bookmarked})
    
    return redirect('jobs:job_detail', pk=pk)


# ==================== Analytics/Dashboard Views ====================

@login_required(login_url='jobs:login')
def dashboard(request):
    """User/Admin dashboard with analytics"""
    user_stats = {
        'applications_count': Application.objects.filter(user=request.user).count(),
        'bookmarks_count': Bookmark.objects.filter(user=request.user).count(),
        'applied_jobs': Application.objects.filter(user=request.user).values('status').annotate(count=Count('id')),
    }
    
    # Popular jobs
    popular_jobs = Job.objects.filter(is_active=True).order_by('-views_count')[:5]
    
    # Recent jobs
    recent_jobs = Job.objects.filter(is_active=True).order_by('-posted_date')[:5]
    
    context = {
        'user_stats': user_stats,
        'popular_jobs': popular_jobs,
        'recent_jobs': recent_jobs,
    }
    return render(request, 'jobs/dashboard.html', context)


# ==================== Job Creation & Editing Views ====================

@login_required(login_url='jobs:login')
@require_http_methods(["GET", "POST"])
def create_job(request):
    """Create a new job posting - employers only"""
    # Ensure user has a UserProfile
    userprofile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if not userprofile.is_employer:
        messages.error(request, 'Only employers can post jobs. Please contact support to upgrade your account.')
        return redirect('jobs:index')
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            
            # Ensure the job is posted by the user's company if they have one
            if userprofile.company:
                job.company = userprofile.company
            
            job.save()
            messages.success(request, f'Job "{job.title}" posted successfully!')
            return redirect('jobs:job_detail', pk=job.pk)
    else:
        form = JobForm()
        # Filter companies to only show user's company if they have one
        if userprofile.company:
            form.fields['company'].queryset = Company.objects.filter(pk=userprofile.company.pk)
    
    context = {'form': form, 'title': 'Post a New Job'}
    return render(request, 'jobs/job_form.html', context)


@login_required(login_url='jobs:login')
@require_http_methods(["GET", "POST"])
def edit_job(request, pk):
    """Edit an existing job posting - only by the poster"""
    job = get_object_or_404(Job, pk=pk)
    
    # Permission check: only the user who posted the job can edit it
    if job.posted_by != request.user:
        messages.error(request, 'You can only edit jobs you posted.')
        return redirect('jobs:job_detail', pk=job.pk)
    
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, f'Job "{job.title}" updated successfully!')
            return redirect('jobs:job_detail', pk=job.pk)
    else:
        form = JobForm(instance=job)
    
    context = {'form': form, 'title': 'Edit Job', 'job': job}
    return render(request, 'jobs/job_form.html', context)
