document.addEventListener("DOMContentLoaded", function () {

    // Clone nav links into mobile menu
    const navLinks = document.getElementById('navLinks');
    const mobileMenu = document.getElementById('mobileMenu');
    if (navLinks && mobileMenu) {
        mobileMenu.innerHTML = navLinks.innerHTML;
    }

    // Mobile menu toggle
    window.toggleMenu = function() {
        if (mobileMenu) {
            mobileMenu.classList.toggle('open');
        }
    }

    // Messages auto-hide after 10 seconds
    let messages = document.querySelectorAll("[id^='msg']");
    messages.forEach(function (msg) {
        setTimeout(() => {
            msg.style.display = "none";
        }, 10000);
    });

    // Profile Dropdown
    const profileToggle = document.getElementById('profileToggle');
    const profileDropdown = document.getElementById('profileDropdown');

    if (profileToggle && profileDropdown) {
        profileToggle.addEventListener('click', () => {
            profileDropdown.classList.toggle('show');
        });
    }
});
