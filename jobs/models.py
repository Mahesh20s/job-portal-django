from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Extended user profile for job portal"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    is_employer = models.BooleanField(default=False, help_text='Is this user an employer/company?')
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


# Signal to create UserProfile when User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save user profile - only if it exists"""
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()


class Company(models.Model):
    """Company model for job portal"""
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    website = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=200)
    logo = models.URLField(blank=True, null=True, help_text='URL to company logo')
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Companies"
    
    def __str__(self):
        return self.name


class Job(models.Model):
    """Job listing model"""
    JOB_TYPE_CHOICES = [
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Contract', 'Contract'),
        ('Remote', 'Remote'),
    ]
    
    EXPERIENCE_LEVEL_CHOICES = [
        ('Entry', 'Entry Level'),
        ('Mid', 'Mid Level'),
        ('Senior', 'Senior Level'),
        ('Executive', 'Executive'),
    ]
    
    title = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='posted_jobs')
    location = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField(blank=True, null=True)
    salary_min = models.IntegerField(blank=True, null=True)
    salary_max = models.IntegerField(blank=True, null=True)
    salary = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES, default='Full-time')
    experience_level = models.CharField(max_length=50, choices=EXPERIENCE_LEVEL_CHOICES, default='Mid')
    posted_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-posted_date']
        verbose_name_plural = "Jobs"
    
    def __str__(self):
        return f"{self.title} at {self.company}"
    
    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])


class Application(models.Model):
    """Job application model"""
    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Reviewed', 'Reviewed'),
        ('Shortlisted', 'Shortlisted'),
        ('Interview', 'Interview'),
        ('Rejected', 'Rejected'),
        ('Accepted', 'Accepted'),
    ]
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Applied')
    applied_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-applied_date']
        unique_together = ('job', 'user')
    
    def __str__(self):
        return f"{self.user.username} applied for {self.job.title}"


class Bookmark(models.Model):
    """Bookmark/Wishlist model for saving jobs"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='bookmarks')
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_date']
        unique_together = ('user', 'job')
    
    def __str__(self):
        return f"{self.user.username} bookmarked {self.job.title}"
