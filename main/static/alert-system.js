// Enhanced Global Message System
const MessageSystem = {
    init() {
        // Create messages container if it doesn't exist
        if (!document.querySelector('.messages')) {
            const container = document.createElement('div');
            container.className = 'messages';
            // Insert after header or at the start of body
            const header = document.querySelector('header');
            if (header) {
                header.after(container);
            } else {
                document.body.prepend(container);
            }
        }
    },

    getIcon(type) {
        const icons = {
            'success': 'fas fa-check-circle',
            'error': 'fas fa-exclamation-circle',
            'warning': 'fas fa-exclamation-triangle',
            'info': 'fas fa-info-circle'
        };
        return icons[type] || icons['info'];
    },

    show(message, type = 'info', duration = 5000) {
        this.init();
        const container = document.querySelector('.messages');
        
        // Create alert element with enhanced styling
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} enhanced-alert`;
        alert.innerHTML = `
            <div class="alert-content">
                <i class="${this.getIcon(type)} alert-icon"></i>
                <span class="alert-message">${message}</span>
            </div>
            <button type="button" class="close-btn" onclick="this.parentElement.remove();">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        // Add slide-in effect from top
        alert.style.transform = 'translateY(-100%)';
        alert.style.opacity = '0';
        container.appendChild(alert);
        
        // Trigger slide in animation
        setTimeout(() => {
            alert.style.transform = 'translateY(0)';
            alert.style.opacity = '1';
        }, 10);
        
        // Auto dismiss after specified duration
        if (duration > 0) {
            setTimeout(() => {
                this.dismiss(alert);
            }, duration);
        }
    },

    dismiss(alert) {
        alert.style.transform = 'translateY(-100%)';
        alert.style.opacity = '0';
        setTimeout(() => {
            alert.remove();
        }, 300);
    },

    // Convenience methods for different alert types
    success(message, duration = 4000) {
        this.show(message, 'success', duration);
    },

    error(message, duration = 6000) {
        this.show(message, 'error', duration);
    },

    warning(message, duration = 5000) {
        this.show(message, 'warning', duration);
    },

    info(message, duration = 4000) {
        this.show(message, 'info', duration);
    }
};

// Make it available globally
window.showMessage = MessageSystem.show.bind(MessageSystem);
window.showSuccess = MessageSystem.success.bind(MessageSystem);
window.showError = MessageSystem.error.bind(MessageSystem);
window.showWarning = MessageSystem.warning.bind(MessageSystem);
window.showInfo = MessageSystem.info.bind(MessageSystem);

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.book form').forEach(function(form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const url = form.action;
            const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Remove the book from the UI
                    form.closest('.book').remove();
                }
                window.showAjaxMessage(data.message, data.status);
                // Optionally update the borrowing status count
                const statusElem = document.querySelector('.borrowing-status p');
                if (statusElem) {
                    let count = document.querySelectorAll('.book').length;
                    let max = statusElem.textContent.match(/out of (\d+)/);
                    if (max) {
                        statusElem.textContent = `You have borrowed ${count} out of ${max[1]} allowed books.`;
                    }
                }
                // If no books left, show the empty message
                if (document.querySelectorAll('.book').length === 0) {
                    const container = document.querySelector('.book-container');
                    if (container) {
                        container.innerHTML = '<p class="no-books">You haven\'t borrowed any books yet.</p>';
                    }
                }
            })
            .catch(() => {
                window.showAjaxMessage('An error occurred. Please try again.', 'error');
            });
        });
    });
}); 