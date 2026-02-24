from django.contrib import admin
from .models import Company, Job, Application, Bookmark, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_employer', 'company', 'phone', 'created_date')
    list_filter = ('is_employer', 'created_date')
    search_fields = ('user__username', 'user__email', 'company__name')
    readonly_fields = ('user', 'created_date')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'email', 'created_date')
    list_filter = ('location', 'created_date')
    search_fields = ('name', 'location', 'email')
    ordering = ('-created_date',)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'job_type', 'experience_level', 'posted_by', 'posted_date', 'is_active', 'views_count')
    list_filter = ('job_type', 'experience_level', 'is_active', 'posted_date', 'company')
    search_fields = ('title', 'company__name', 'location', 'description', 'posted_by__username')
    readonly_fields = ('views_count', 'posted_date', 'posted_by')
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'company', 'location', 'job_type', 'experience_level', 'posted_by')
        }),
        ('Description', {
            'fields': ('description', 'requirements')
        }),
        ('Salary', {
            'fields': ('salary_min', 'salary_max', 'salary')
        }),
        ('Status', {
            'fields': ('is_active', 'deadline', 'posted_date', 'views_count')
        }),
    )
    ordering = ('-posted_date',)
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new job
            obj.posted_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'status', 'applied_date', 'updated_date')
    list_filter = ('status', 'applied_date', 'job__company')
    search_fields = ('user__username', 'user__email', 'job__title')
    readonly_fields = ('applied_date', 'updated_date', 'resume')
    fieldsets = (
        ('Application', {
            'fields': ('job', 'user', 'status')
        }),
        ('Documents', {
            'fields': ('resume', 'cover_letter')
        }),
        ('Dates', {
            'fields': ('applied_date', 'updated_date')
        }),
    )
    ordering = ('-applied_date',)


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'created_date')
    list_filter = ('created_date', 'job__company')
    search_fields = ('user__username', 'job__title')
    readonly_fields = ('created_date',)
    ordering = ('-created_date',)

