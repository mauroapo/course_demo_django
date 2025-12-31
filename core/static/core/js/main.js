// Hamburger menu toggle
document.addEventListener('DOMContentLoaded', function () {
    const hamburger = document.querySelector('.hamburger');
    const sidebar = document.querySelector('.sidebar');

    if (hamburger && sidebar) {
        hamburger.addEventListener('click', function () {
            sidebar.classList.toggle('active');
        });

        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', function (event) {
            if (window.innerWidth <= 768) {
                if (!sidebar.contains(event.target) && !hamburger.contains(event.target)) {
                    sidebar.classList.remove('active');
                }
            }
        });
    }

    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('.message');
    messages.forEach(function (message) {
        setTimeout(function () {
            message.style.animation = 'slideOut 0.3s ease';
            setTimeout(function () {
                message.remove();
            }, 300);
        }, 5000);
    });
});

// Slide out animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
