document.addEventListener('DOMContentLoaded', () => {
    const docsLink = document.getElementById('docs-link');

    docsLink.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the default link behavior

        // Add fade-out class to body
        document.body.classList.add('fade-out');

        // Wait for the animation to complete before navigating
        setTimeout(() => {
            window.location.href = this.href;
        }, 500); // Duration should match the CSS animation duration
    });
});