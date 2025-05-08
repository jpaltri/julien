document.addEventListener('DOMContentLoaded', function() {
    // Filter books by category
    const categoryLinks = document.querySelectorAll('.category-filter');
    categoryLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const category = this.dataset.category;
            window.location.href = `/blog?category=${category}`;
        });
    });
});