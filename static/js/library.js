// static/js/blog.js
// This file is optional as we've included JavaScript directly in the blog.html template
// You can move the JavaScript logic here if you prefer to separate concerns

// static/js/library.js
document.addEventListener('DOMContentLoaded', function() {
    // Filter books by category
    const categoryLinks = document.querySelectorAll('.category-filter');
    categoryLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const category = this.dataset.category;
            window.location.href = `/library?category=${category}`;
        });
    });
});

// static/css/main.css
/* Additional custom styles can be added here if needed */