// ==================== Dark Mode Toggle ====================
const darkModeToggle = document.getElementById('darkModeToggle');

// Initialize dark mode from localStorage
if (localStorage.getItem('darkMode') === 'enabled') {
    document.body.classList.add('dark-mode');
    if (darkModeToggle) darkModeToggle.checked = true;
}

// Dark mode toggle event
if (darkModeToggle) {
    darkModeToggle.addEventListener('change', function() {
        document.body.classList.toggle('dark-mode');
        if (document.body.classList.contains('dark-mode')) {
            localStorage.setItem('darkMode', 'enabled');
        } else {
            localStorage.setItem('darkMode', 'disabled');
        }
    });
}

// ==================== DOM Elements ====================
const exploreBtn = document.getElementById('exploreBtn');
const jobCards = document.querySelectorAll('.job-card');

// ==================== Explore Button ====================
if (exploreBtn) {
    exploreBtn.addEventListener('click', function() {
        const jobsSection = document.getElementById('jobs');
        if (jobsSection) {
            jobsSection.scrollIntoView({ behavior: 'smooth' });
        }
    });
}

// ==================== Job Card Animations ====================
window.addEventListener('load', function() {
    jobCards.forEach((card, index) => {
        card.style.animation = `slideIn 0.5s ease forwards`;
        card.style.animationDelay = `${index * 0.1}s`;
    });
});

// ==================== Smooth Scroll for Navigation ====================
document.querySelectorAll('nav a, .auth-link a, .stat-link').forEach(link => {
    link.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href && href.startsWith('#')) {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        }
    });
});

// ==================== Dynamic CSS for Animations ====================
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }

    @keyframes bounce {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-10px);
        }
    }
`;
document.head.appendChild(style);

// ==================== Form Validation ====================
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        const inputs = this.querySelectorAll('input[required], textarea[required]');
        let isValid = true;

        inputs.forEach(input => {
            if (!input.value.trim()) {
                isValid = false;
                input.style.borderColor = '#e74c3c';
                let errorMsg = input.parentElement.querySelector('.error-message');
                if (!errorMsg) {
                    errorMsg = document.createElement('small');
                    errorMsg.className = 'error-message';
                    errorMsg.style.color = '#e74c3c';
                    errorMsg.textContent = 'This field is required';
                    input.parentElement.appendChild(errorMsg);
                }
            } else {
                input.style.borderColor = '';
                const errorMsg = input.parentElement.querySelector('.error-message');
                if (errorMsg) errorMsg.remove();
            }
        });

        if (!isValid) {
            e.preventDefault();
        }
    });
});

// ==================== Job Application Status Tracking ====================
function trackApplicationStatus(applicationId, newStatus) {
    console.log(`Application ${applicationId} status: ${newStatus}`);
    // This could be expanded to send updates to the server
}

// ==================== Bookmark Management ====================
function toggleBookmark(jobId) {
    fetch(`/job/${jobId}/bookmark/`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        const button = event.target.closest('button');
        if (button) {
            if (data.is_bookmarked) {
                button.innerHTML = '❤️ Bookmarked';
                button.style.color = '#e74c3c';
            } else {
                button.innerHTML = '🤍 Bookmark';
                button.style.color = '';
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to toggle bookmark');
    });
}

function removeBookmark(jobId) {
    if (confirm('Remove this bookmark?')) {
        fetch(`/job/${jobId}/bookmark/`, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            location.reload();
        })
        .catch(error => console.error('Error:', error));
    }
}

// ==================== CSRF Token Utility ====================
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// ==================== Page Load Logging ====================
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Job Portal loaded successfully');
    console.log(`📊 Total job cards: ${jobCards.length}`);
    console.log(`🌙 Dark mode: ${localStorage.getItem('darkMode')}`);
});

// ==================== Search Form Enhancement ====================
const searchForm = document.querySelector('.search-form');
if (searchForm) {
    const inputs = searchForm.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('change', function() {
            // Auto-save filter preferences
            localStorage.setItem(`filter_${input.name}`, input.value);
        });
    });

    // Restore filter preferences
    inputs.forEach(input => {
        const saved = localStorage.getItem(`filter_${input.name}`);
        if (saved && input.value === '') {
            input.value = saved;
        }
    });
}

// ==================== Scroll to Top Button ====================
const scrollTopBtn = document.createElement('button');
scrollTopBtn.innerHTML = '↑ Top';
scrollTopBtn.className = 'scroll-top-btn';
scrollTopBtn.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: #3498db;
    color: white;
    border: none;
    padding: 10px 15px;
    border-radius: 4px;
    cursor: pointer;
    display: none;
    z-index: 1000;
    transition: all 0.3s;
`;

document.body.appendChild(scrollTopBtn);

window.addEventListener('scroll', function() {
    if (window.pageYOffset > 300) {
        scrollTopBtn.style.display = 'block';
    } else {
        scrollTopBtn.style.display = 'none';
    }
});

scrollTopBtn.addEventListener('click', function() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// ==================== Tooltip Functionality ====================
document.querySelectorAll('[data-tooltip]').forEach(element => {
    const tooltip = element.getAttribute('data-tooltip');
    element.addEventListener('mouseenter', function() {
        const div = document.createElement('div');
        div.textContent = tooltip;
        div.style.cssText = `
            position: absolute;
            background-color: #333;
            color: white;
            padding: 5px 10px;
            border-radius: 3px;
            font-size: 12px;
            z-index: 1000;
        `;
        element.appendChild(div);
    });
    element.addEventListener('mouseleave', function() {
        const tooltips = element.querySelectorAll('div');
        tooltips.forEach(t => t.remove());
    });
});

// ==================== Responsive Menu ====================
document.addEventListener('DOMContentLoaded', function() {
    const navButton = document.createElement('button');
    if (window.innerWidth <= 768) {
        // Mobile menu could be added here
    }
});

// ==================== Console Welcome Message ====================
console.log('%c🚀 Welcome to Job Portal!', 'color: #3498db; font-size: 24px; font-weight: bold;');
console.log('%cBuilt with Django & Modern Web Technologies', 'color: #27ae60; font-size: 14px;');
