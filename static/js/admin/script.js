document.addEventListener('DOMContentLoaded', function() {
    // Fetch and insert the sidebar.html content
    fetch('sidebar.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('sidebar-container').innerHTML = data;

            // After loading the sidebar, set up the event listeners
            const menuBtn = document.querySelector('.menu-btn');
            const sidebar = document.querySelector('.sidebar');
            const closeBtn = document.querySelector('.sidebar-close-btn');

            // Open sidebar
            menuBtn.addEventListener('click', function() {
                sidebar.classList.add('active');
            });

            // Close sidebar
            closeBtn.addEventListener('click', function() {
                sidebar.classList.remove('active');
            });

            // Close sidebar when clicking outside
            document.addEventListener('click', function(event) {
                if (!sidebar.contains(event.target) && !menuBtn.contains(event.target)) {
                    sidebar.classList.remove('active');
                }
            });

            // Keyboard accessibility: close with Escape key
            document.addEventListener('keydown', function(event) {
                if (event.key === 'Escape' && sidebar.classList.contains('active')) {
                    sidebar.classList.remove('active');
                }
            });
        })
        .catch(error => console.error('Error loading sidebar:', error));
});