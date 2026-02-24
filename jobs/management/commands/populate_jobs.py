from django.core.management.base import BaseCommand
from jobs.models import Company, Job
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Populate the database with sample jobs and companies'

    def handle(self, *args, **options):
        # Create sample companies
        companies_data = [
            {
                'name': 'Tech Corp',
                'description': 'A leading technology company specializing in software solutions',
                'website': 'https://techcorp.com',
                'email': 'hr@techcorp.com',
                'phone': '+1-800-TECH-123',
                'location': 'San Francisco, CA'
            },
            {
                'name': 'DataWave Inc',
                'description': 'Big data and analytics platform provider',
                'website': 'https://datawave.io',
                'email': 'careers@datawave.io',
                'phone': '+1-800-DATA-456',
                'location': 'New York, NY'
            },
            {
                'name': 'CloudSync Solutions',
                'description': 'Cloud infrastructure and DevOps services',
                'website': 'https://cloudsync.dev',
                'email': 'jobs@cloudsync.dev',
                'phone': '+1-800-CLOUD-789',
                'location': 'Seattle, WA'
            },
            {
                'name': 'AI Innovations',
                'description': 'Artificial Intelligence and Machine Learning research',
                'website': 'https://aiinno.com',
                'email': 'recruit@aiinno.com',
                'phone': '+1-800-AI-JOBS',
                'location': 'Boston, MA'
            },
        ]

        companies = {}
        for company_data in companies_data:
            company, created = Company.objects.get_or_create(
                name=company_data['name'],
                defaults=company_data
            )
            companies[company_data['name']] = company
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created company: {company.name}'))
            else:
                self.stdout.write(f'Company already exists: {company.name}')

        # Create sample jobs
        jobs_data = [
            {
                'title': 'Senior Python Developer',
                'company': 'Tech Corp',
                'location': 'San Francisco, CA',
                'description': 'We are looking for an experienced Python developer to join our team. You will be responsible for developing and maintaining our backend services.',
                'requirements': '5+ years Python experience\nDjango/FastAPI knowledge\nPostgreSQL proficiency\nREST API design',
                'salary_min': 120000,
                'salary_max': 160000,
                'job_type': 'Full-time',
                'experience_level': 'Senior',
                'deadline': datetime.now().date() + timedelta(days=30),
            },
            {
                'title': 'Frontend React Developer',
                'company': 'Tech Corp',
                'location': 'San Francisco, CA',
                'description': 'Join our frontend team and help us build beautiful, responsive web applications using React and modern JavaScript.',
                'requirements': '3+ years React experience\nTypeScript knowledge\nHTML/CSS expertise\nState management (Redux/Zustand)',
                'salary_min': 100000,
                'salary_max': 140000,
                'job_type': 'Full-time',
                'experience_level': 'Mid',
                'deadline': datetime.now().date() + timedelta(days=25),
            },
            {
                'title': 'Data Engineer',
                'company': 'DataWave Inc',
                'location': 'New York, NY',
                'description': 'Build scalable data pipelines and infrastructure for our analytics platform. Work with big data technologies and cloud services.',
                'requirements': 'Strong Python/Scala skills\nSpark/Hadoop experience\nSQL proficiency\nCloud platforms (AWS/GCP)',
                'salary_min': 110000,
                'salary_max': 150000,
                'job_type': 'Full-time',
                'experience_level': 'Mid',
                'deadline': datetime.now().date() + timedelta(days=28),
            },
            {
                'title': 'DevOps Engineer',
                'company': 'CloudSync Solutions',
                'location': 'Seattle, WA',
                'description': 'Manage and optimize our cloud infrastructure. Implement CI/CD pipelines and ensure system reliability.',
                'requirements': 'Docker/Kubernetes expertise\nCI/CD tools (Jenkins, GitLab CI)\nLinux administration\nInfrastructure as Code (Terraform)',
                'salary_min': 115000,
                'salary_max': 155000,
                'job_type': 'Full-time',
                'experience_level': 'Senior',
                'deadline': datetime.now().date() + timedelta(days=35),
            },
            {
                'title': 'Machine Learning Engineer',
                'company': 'AI Innovations',
                'location': 'Boston, MA',
                'description': 'Develop and deploy machine learning models for real-world applications. Collaborate with data scientists and product teams.',
                'requirements': 'Python, TensorFlow/PyTorch\nDeep Learning knowledge\nExperience with ML pipelines\nSQL and distributed computing',
                'salary_min': 130000,
                'salary_max': 180000,
                'job_type': 'Full-time',
                'experience_level': 'Senior',
                'deadline': datetime.now().date() + timedelta(days=40),
            },
            {
                'title': 'Junior Web Developer',
                'company': 'Tech Corp',
                'location': 'San Francisco, CA',
                'description': 'Start your career as a full-stack developer. You will work on various projects and learn from experienced mentors.',
                'requirements': 'HTML/CSS/JavaScript basics\nWilling to learn\nGit basics\nProblem-solving skills',
                'salary_min': 70000,
                'salary_max': 90000,
                'job_type': 'Full-time',
                'experience_level': 'Entry',
                'deadline': datetime.now().date() + timedelta(days=20),
            },
            {
                'title': 'Database Administrator',
                'company': 'DataWave Inc',
                'location': 'New York, NY',
                'description': 'Manage and maintain our database infrastructure. Ensure performance, security, and availability.',
                'requirements': 'PostgreSQL/MySQL expertise\nBackup and recovery knowledge\nPerformance tuning\nMonitoring tools experience',
                'salary_min': 105000,
                'salary_max': 145000,
                'job_type': 'Full-time',
                'experience_level': 'Mid',
                'deadline': datetime.now().date() + timedelta(days=32),
            },
            {
                'title': 'Product Manager (Part-time)',
                'company': 'CloudSync Solutions',
                'location': 'Seattle, WA',
                'description': 'Lead product strategy and roadmap for our cloud services. Work closely with engineering and design teams.',
                'requirements': 'Product management experience\nTech background preferred\nData-driven decision making\nStakeholder communication',
                'salary_min': 80000,
                'salary_max': 110000,
                'job_type': 'Part-time',
                'experience_level': 'Mid',
                'deadline': datetime.now().date() + timedelta(days=27),
            },
            {
                'title': 'Security Engineer',
                'company': 'Tech Corp',
                'location': 'San Francisco, CA',
                'description': 'Protect our systems and data. Identify vulnerabilities and implement security best practices.',
                'requirements': 'Network security knowledge\nPenetration testing experience\nCryptography basics\nSecurity compliance (OWASP)',
                'salary_min': 125000,
                'salary_max': 165000,
                'job_type': 'Full-time',
                'experience_level': 'Senior',
                'deadline': datetime.now().date() + timedelta(days=33),
            },
            {
                'title': 'Technical Writer',
                'company': 'AI Innovations',
                'location': 'Remote',
                'description': 'Create comprehensive documentation for our AI products. Make complex concepts easy to understand.',
                'requirements': 'Strong writing skills\nTechnical background\nDocumentation tools (Markdown, Sphinx)\nVersion control basics',
                'salary_min': 75000,
                'salary_max': 100000,
                'job_type': 'Remote',
                'experience_level': 'Mid',
                'deadline': datetime.now().date() + timedelta(days=29),
            },
        ]

        for job_data in jobs_data:
            company_name = job_data.pop('company')
            company = companies[company_name]
            
            job, created = Job.objects.get_or_create(
                title=job_data['title'],
                company=company,
                defaults={**job_data, 'is_active': True}
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created job: {job.title} at {company.name}'))
            else:
                self.stdout.write(f'Job already exists: {job.title}')

        self.stdout.write(self.style.SUCCESS('\n✅ Successfully populated the database with sample jobs!'))
