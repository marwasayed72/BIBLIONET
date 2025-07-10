document.addEventListener('DOMContentLoaded', function() {
    // Get all alert messages
    const alerts = document.querySelectorAll('.alert');
    
    // Function to remove an alert with enhanced animation
    function removeAlert(alert) {
        alert.style.transform = 'translateY(-100%)';
        alert.style.opacity = '0';
        setTimeout(() => {
            alert.remove();
        }, 400); // Wait for slide out animation
    }

    // Add enhanced animations to alerts
    alerts.forEach((alert, index) => {
        // Add transition for smooth animations
        alert.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
        
        // Stagger the entrance animation
        setTimeout(() => {
            alert.style.transform = 'translateY(0)';
            alert.style.opacity = '1';
        }, index * 100);
        
        // Auto dismiss after 5 seconds (longer for errors)
        const duration = alert.classList.contains('alert-error') ? 7000 : 5000;
        setTimeout(() => {
            removeAlert(alert);
        }, duration);

        // Close button click handler
        const closeBtn = alert.querySelector('.close-btn');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                removeAlert(alert);
            });
        }
        
        // Add hover effect to pause auto-dismiss
        let dismissTimeout;
        const resetDismissTimer = () => {
            clearTimeout(dismissTimeout);
            dismissTimeout = setTimeout(() => {
                removeAlert(alert);
            }, duration);
        };
        
        alert.addEventListener('mouseenter', () => {
            clearTimeout(dismissTimeout);
        });
        
        alert.addEventListener('mouseleave', resetDismissTimer);
    });

    // Auto-dismiss messages after 4 seconds with fade-out
    document.querySelectorAll('.auto-dismiss').forEach(function(alert) {
        setTimeout(function() {
            alert.classList.add('fade-out');
            setTimeout(function() {
                if (alert.parentNode) alert.parentNode.removeChild(alert);
            }, 500); // match CSS transition
        }, 4000);
    });
});

// Function to show a message dynamically (for AJAX)
window.showAjaxMessage = function(message, status) {
    // Remove existing alerts
    document.querySelectorAll('.simple-alert').forEach(alert => alert.remove());

    // Find or create the .messages container
    let messagesContainer = document.querySelector('.messages');
    if (!messagesContainer) {
        messagesContainer = document.createElement('div');
        messagesContainer.className = 'messages';
        document.body.prepend(messagesContainer);
    }

    // Create simple alert div
    const alertDiv = document.createElement('div');
    alertDiv.className = 'simple-alert';
    alertDiv.innerHTML = `
        <span>${message}</span>
        <button type="button" class="close-btn">×</button>
    `;
    messagesContainer.appendChild(alertDiv);

    // Add close button handler
    alertDiv.querySelector('.close-btn').addEventListener('click', function() {
        alertDiv.remove();
    });

    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}; 