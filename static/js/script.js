document.addEventListener('DOMContentLoaded', ()=>{
  const themeToggle = document.getElementById('themeToggle');
  const scrollBtn = document.getElementById('scrollTopBtn');
  const root = document.documentElement;
  const savedTheme = localStorage.getItem('renthome-theme');

  if (savedTheme === 'dark') {
    document.body.classList.add('dark-mode');
    if (themeToggle) themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
  }

  themeToggle?.addEventListener('click', ()=>{
    document.body.classList.toggle('dark-mode');
    const enabled = document.body.classList.contains('dark-mode');
    themeToggle.innerHTML = enabled ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
    localStorage.setItem('renthome-theme', enabled ? 'dark' : 'light');
  });

  window.addEventListener('scroll', ()=>{
    if (window.scrollY > 320) {
      scrollBtn?.classList.add('visible');
    } else {
      scrollBtn?.classList.remove('visible');
    }
  });

  scrollBtn?.addEventListener('click', ()=>{
    window.scrollTo({top:0,behavior:'smooth'});
  });
});
