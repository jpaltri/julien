// static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    // Make post cards clickable
    document.querySelectorAll('.post-card').forEach(card => {
        card.addEventListener('click', function(e) {
            // Don't navigate if clicking on a share button or its child elements
            if (e.target.closest('.share-buttons') || e.target.closest('a')) {
                e.stopPropagation();
                return;
            }
            
            // Get the post URL from the first link in the card
            const link = this.querySelector('a');
            if (link) {
                window.location = link.href;
            }
        });
    });
    
    // Copy link to clipboard
    document.querySelectorAll('.copy-link').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const url = this.getAttribute('data-url');
            navigator.clipboard.writeText(url).then(() => {
                // Show success message
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-check"></i> Copied!';
                setTimeout(() => {
                    this.innerHTML = originalText;
                }, 2000);
            });
        });
    });
});