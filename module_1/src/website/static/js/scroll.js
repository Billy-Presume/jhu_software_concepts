// Makes the snap scrolling smooth when navigating to a section
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const section = document.querySelector(this.getAttribute('href'));
    section?.scrollIntoView({ behavior: 'smooth' });
  });
});

// Toggles the nav menu on Mobile
// Handles open/close on click & outside of modal when the
// Toggle nav menu is clicke on mobile
document.addEventListener("DOMContentLoaded", function () {
  const toggleButton = document.getElementById("mobile-toggle");
  const menu = document.getElementById("mobile-menu");

  // Ensure elements exist before attaching event listeners
  if (!toggleButton || !menu) return;

  // Toggle menu visibility on button click
  toggleButton.addEventListener("click", (e) => {
    e.stopPropagation(); // Prevent click from bubbling up to window
    const isHidden = menu.classList.toggle("hidden");
    toggleButton.setAttribute("aria-expanded", !isHidden);
  });

  // Close the menu when clicking outside
  window.addEventListener("click", (e) => {
    if (!menu.contains(e.target) && !toggleButton.contains(e.target)) {
      menu.classList.add("hidden");
      toggleButton.setAttribute("aria-expanded", "false");
    }
  });

  // Close menu when any mobile nav link is clicked
  menu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      menu.classList.add("hidden");
      toggleButton.setAttribute("aria-expanded", "false");
    });
  });

  // Close menu on Escape key press
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      menu.classList.add("hidden");
      toggleButton.setAttribute("aria-expanded", "false");
    }
  });
});
