// Makes the snap scrolling smooth when navigating to a section
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const section = document.querySelector(this.getAttribute('href'));
    section?.scrollIntoView({ behavior: 'smooth' });
  });
});

// Toggles the nav menu on Mobile
document.querySelector('[data-collapse-toggle]').addEventListener('click', function () {
  const menu = document.getElementById('navbar-default');
  menu.classList.toggle('hidden');
});

// Dynamically generates the year for the copyright element
document.getElementById('year').textContent = new Date().getFullYear();