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

// Dynamically updates selected nav item on scroll
document.addEventListener("DOMContentLoaded", () => {
    // Only nav links inside <ul> (ignores logo)
    const navLinks = document.querySelectorAll('ul a[href^="#"]');
    const sections = Array.from(navLinks).map(link => document.querySelector(link.getAttribute("href")));

    function clearActiveClasses() {
      navLinks.forEach(link => {
        link.classList.remove('px-4', 'py-2', 'bg-blue-600', 'text-white', 'rounded-lg', 'hover:bg-blue-900');
        link.classList.add('hover:text-blue-600'); // Restore default hover
      });
    }

    function setActive(link) {
      clearActiveClasses();
      link.classList.remove('hover:text-blue-600');
      link.classList.add('px-4', 'py-2', 'bg-blue-600', 'text-white', 'rounded-lg', 'hover:bg-blue-900');
    }

    const observer = new IntersectionObserver(
      entries => {
        const visibleSections = entries.filter(entry => entry.isIntersecting);
        if (visibleSections.length > 0) {
          const topSection = visibleSections.sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top)[0];
          const activeLink = Array.from(navLinks).find(link => link.getAttribute("href") === `#${topSection.target.id}`);
          if (activeLink) setActive(activeLink);
        }
      },
      {
        root: null,
        rootMargin: '0px',
        threshold: 0.6
      }
    );

    sections.forEach(section => {
      if (section) observer.observe(section);
    });

    // Default selection: Profile
    const defaultLink = document.querySelector('ul a[href="#profile"]');
    if (defaultLink) setActive(defaultLink);
  });