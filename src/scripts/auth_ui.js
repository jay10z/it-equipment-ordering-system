/**
 * ProTech Solutions - UI State Manager
 * Handles global UI updates like Navbar Login/Logout state
 */

document.addEventListener('DOMContentLoaded', () => {
    updateAuthUI();
});

function updateAuthUI() {
    if (typeof ApiClient === 'undefined') return;

    const token = ApiClient.getToken();
    const userStr = localStorage.getItem('user');

    // Find Login buttons
    // We look for links pointing to login.html or with class 'auth-link'
    const authLinks = document.querySelectorAll('a[href="login.html"]');

    if (token && userStr) {
        const user = JSON.parse(userStr);

        authLinks.forEach(link => {
            link.textContent = 'Logout';
            link.href = '#';
            link.classList.add('logout-link'); // Add identifier

            // Remove old listeners to avoid duplicates if re-run
            const newLink = link.cloneNode(true);
            link.parentNode.replaceChild(newLink, link);

            newLink.addEventListener('click', (e) => {
                e.preventDefault();
                ApiClient.logout();
            });

            // Add Admin Dashboard link if user is admin
            if (user.is_admin) {
                const dashboardLink = document.createElement('a');
                dashboardLink.href = 'Admin.html';
                dashboardLink.textContent = 'Dashboard';
                dashboardLink.className = 'cta';
                dashboardLink.style.marginRight = '10px';
                dashboardLink.style.borderColor = 'var(--accent-color)';
                dashboardLink.style.color = 'var(--accent-color)';
                newLink.parentNode.insertBefore(dashboardLink, newLink);
            }
        });

        // If on login/register page, redirect to home
        const path = window.location.pathname;
        if (path.includes('login.html') || path.includes('register.html')) {
            // Optional: Redirect away from auth pages if already logged in
            // window.location.href = 'index.html'; 
        }
    }
}
