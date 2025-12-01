// --- DATA ---
const PROJECTS = [
  { id: 1, type: 'photo', src: "https://images.unsplash.com/photo-1441986300917-64674bd600d8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80", caption: "RESERVA GO — NOV 24", client: "Reserva", essence: "Estética urbana crua.", result: "Engajamento recorde." },
  { id: 2, type: 'photo', src: "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80", caption: "VOGUE BR — CONCRETE", client: "Vogue", essence: "Styling monocromático.", result: "Capa digital." },
  { id: 3, type: 'photo', src: "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80", caption: "ANITTA — MILVECES", client: "Anitta", essence: "Cyberpunk low-fi.", result: "10M+ views orgânicas." },
  { id: 4, type: 'photo', src: "https://images.unsplash.com/photo-1539109136881-3be0616acf4b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80", caption: "OSKLEN — VERÃO 25", client: "Osklen", essence: "Luz natural orgânica.", result: "Coleção esgotada." }
];

const VIDEOS = [
  { id: 5, thumb: "https://images.pexels.com/videos/3045163/free-video-3045163.jpg?auto=compress&cs=tinysrgb&dpr=2&w=1000", src: "https://videos.pexels.com/video-files/3045163/3045163-uhd_2560_1440_25fps.mp4", title: "LUZ VERMELHA", client: "Sevenn Originals", essence: "Tensão monocromática.", result: "Referência visual." },
  { id: 6, thumb: "https://images.pexels.com/videos/2491284/free-video-2491284.jpg?auto=compress&cs=tinysrgb&dpr=2&w=1000", src: "https://videos.pexels.com/video-files/2491284/2491284-uhd_2560_1440_25fps.mp4", title: "NOIR MOTION", client: "Osklen", essence: "Slow motion 120fps.", result: "Campanha renovada." },
  { id: 7, thumb: "https://images.pexels.com/videos/1448735/free-video-1448735.jpg?auto=compress&cs=tinysrgb&dpr=2&w=1000", src: "https://videos.pexels.com/video-files/1448735/1448735-uhd_2560_1440_25fps.mp4", title: "URBAN BEAT", client: "Forum", essence: "Câmera run-and-gun.", result: "Viralização Reels." }
];

const LOGOS = [
  { name: "Osklen", quote: "O mood definiu a coleção. Job fechado.", src: "https://images.unsplash.com/photo-1561070791-2526d30994b5?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80" },
  { name: "Forum", quote: "Light insano, campanha rolou viral.", src: "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80" },
  { name: "Vogue", quote: "Visual impecável.", src: "https://images.unsplash.com/photo-1561070791-2526d30994b5?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80" },
  { name: "Reserva", quote: "CTR Recorde.", src: "https://images.unsplash.com/photo-1441986300917-64674bd600d8?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80" },
  { name: "Sevenn", quote: "Originals.", src: "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80" },
  { name: "Anitta", quote: "10M Views.", src: "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80" },
  { name: "Elle", quote: "Editorial.", src: "https://images.unsplash.com/photo-1561070791-2526d30994b5?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80" },
  { name: "Nike", quote: "Campaign.", src: "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80" }
];

const TESTIMONIALS = [
  { text: "Light insano, campanha rolou viral.", author: "Direção", from: "de Forum", avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=200&q=80" },
  { text: "O mood definiu a coleção. Job fechado.", author: "Criativo", from: "de Osklen", avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-4.0.3&auto=format&fit=crop&w=200&q=80" },
  { text: "Narrativa visual de outro nível.", author: "Mkt", from: "de Reserva", avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-4.0.3&auto=format&fit=crop&w=200&q=80" }
];

// --- COMBINE DATA ---
const ALL_PROJECTS = [...PROJECTS, ...VIDEOS.map(v => ({ ...v, type: 'video' }))];

// --- SVG SPRITE ---
const SVG_SPRITE = {
  arrow: '<line x1="7" y1="17" x2="17" y2="7"></line><polyline points="7 7 17 7 17 17"></polyline>',
  play: '<polygon points="5 3 19 12 5 21 5 3"></polygon>',
  close: '<line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line>',
  calendar: '<rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line>',
  lock: '<rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path>',
  check: '<polyline points="20 6 9 17 4 12"></polyline>'
};

function createSVG(name, size = 14, className = '') {
  return `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="${className}">${SVG_SPRITE[name]}</svg>`;
}

// --- TEMPLATES ---
function renderPortfolio() {
  const grid = document.querySelector('.portfolio-grid');
  if (!grid) return;

  grid.innerHTML = PROJECTS.map((project, i) => `
    <article class="portfolio-item reveal-item" data-delay="${i * 100}">
      <button class="portfolio-card" data-project-id="${project.id}" aria-label="Ver projeto: ${project.client}">
        <div class="portfolio-image-wrapper">
          <img src="${project.src}" alt="${project.caption}" loading="lazy" decoding="async">
        </div>
        <div class="portfolio-info">
          <p class="portfolio-caption">${project.caption}</p>
          ${createSVG('arrow', 14, 'portfolio-arrow')}
        </div>
      </button>
    </article>
  `).join('');
}

function renderVideos() {
  const grid = document.querySelector('.video-grid');
  if (!grid) return;

  grid.innerHTML = VIDEOS.map((video, i) => `
    <article class="video-item reveal-item" data-delay="${i * 150}">
      <button class="video-card" data-video-id="${video.id}" aria-label="Assistir vídeo: ${video.title}">
        <div class="video-thumb-wrapper">
          <img src="${video.thumb}" alt="${video.title}" loading="lazy" decoding="async">
          <div class="video-play-overlay">
            ${createSVG('play', 20)}
          </div>
        </div>
      </button>
    </article>
  `).join('');
}

function renderLogos() {
  const carousel = document.querySelector('.logo-carousel');
  if (!carousel) return;

  // Duplicar apenas 2x - CSS animation faz loop infinito
  const logosDuplicated = [...LOGOS, ...LOGOS];

  carousel.innerHTML = logosDuplicated.map((logo, i) => `
    <div class="logo-item" data-logo-index="${i % LOGOS.length}">
      <img src="${logo.src}" alt="${logo.name}" loading="lazy">
      <div class="logo-modal" data-logo-index="${i % LOGOS.length}">
        <p class="logo-name">${logo.name}</p>
        <p class="logo-quote">"${logo.quote}"</p>
        <button class="logo-cta" data-form-preset="similar">Projeto Similar</button>
      </div>
    </div>
  `).join('');
}

function renderTestimonials() {
  const grid = document.querySelector('.testimonials-grid');
  if (!grid) return;

  grid.innerHTML = TESTIMONIALS.map((t, i) => `
    <article class="testimonial-card reveal-item" data-delay="${i * 100}">
      <div class="testimonial-header">
        <div class="testimonial-avatar">
          <img src="${t.avatar}" alt="${t.author} ${t.from}" loading="lazy" decoding="async">
        </div>
        <blockquote class="testimonial-text">"${t.text}"</blockquote>
      </div>
      <p class="testimonial-author">${t.author} <span class="testimonial-from">${t.from}</span></p>
    </article>
  `).join('');
}

// --- SCROLL REVEAL ---
function initScrollReveal() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

  document.querySelectorAll('.reveal-item').forEach(item => {
    const delay = item.dataset.delay || 0;
    item.style.transitionDelay = `${delay}ms`;
    item.style.opacity = '0';
    item.style.transform = 'translateY(64px)';
    observer.observe(item);
  });
}

// --- EXIT INTENT ---
function initExitIntent() {
  if (sessionStorage.getItem('exitIntentTriggered')) return;

  const handleExitIntent = (e) => {
    if (e.clientY <= 0) {
      openForm('');
      sessionStorage.setItem('exitIntentTriggered', 'true');
      document.removeEventListener('mouseleave', handleExitIntent);
    }
  };

  document.addEventListener('mouseleave', handleExitIntent);
}

// --- PROJECT MODAL ---
function openProject(id) {
  if (!id || isNaN(id) || id <= 0) return;

  const project = ALL_PROJECTS.find(p => p.id === id);
  if (!project) return;

  const modal = document.getElementById('project-modal');
  const modalImage = document.getElementById('modal-image');
  const modalVideo = document.getElementById('modal-video');
  const modalTitle = document.getElementById('modal-title');
  const modalEssence = document.getElementById('modal-essence');
  const modalResult = document.getElementById('modal-result');

  if (!modal || !modalImage || !modalVideo || !modalTitle || !modalEssence || !modalResult) return;

  modalTitle.textContent = project.client || '';
  modalEssence.textContent = project.essence || '';
  modalResult.textContent = project.result || '';

  if (project.type === 'video') {
    modalImage.style.display = 'none';
    modalVideo.style.display = 'block';
    modalVideo.src = project.src || '';
    modalVideo.onerror = () => {
      // Fallback: mostrar thumbnail como imagem se vídeo falhar
      modalVideo.style.display = 'none';
      modalImage.style.display = 'block';
      modalImage.src = project.thumb || '';
      modalImage.alt = project.title || '';
    };
    modalVideo.play().catch(() => {
      // Autoplay blocked - user interaction required
      // Video will play when user clicks
    });
  } else {
    modalVideo.style.display = 'none';
    modalImage.style.display = 'block';
    modalImage.src = project.src || '';
    modalImage.alt = project.client || '';
  }

  modal.style.display = 'flex';
  document.body.style.overflow = 'hidden';

  const firstFocusable = modal.querySelector('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
  firstFocusable?.focus();
}

function closeProject() {
  const modal = document.getElementById('project-modal');
  if (!modal) return;

  const modalVideo = document.getElementById('modal-video');
  if (modalVideo) {
    modalVideo.pause();
    modalVideo.src = '';
  }

  modal.style.display = 'none';
  document.body.style.overflow = '';
}

function closeProjectAndOpenForm(preset) {
  closeProject();
  setTimeout(() => openForm(preset), 300);
}

// --- LEAD FORM ---
function openForm(preset = '') {
  const modal = document.getElementById('lead-form-modal');
  if (!modal) return;

  const budgetSelect = document.getElementById('budget');
  const formStep1 = document.getElementById('form-step-1');
  const formStep2 = document.getElementById('form-step-2');
  const leadForm = document.getElementById('lead-form');
  const nameInput = document.getElementById('name');

  if (!formStep1 || !formStep2 || !leadForm) return;

  if (budgetSelect) {
    if (preset === 'custom') {
      budgetSelect.value = 'custom';
    } else if (preset === 'similar') {
      budgetSelect.value = '10k-50k';
    }
  }

  modal.style.display = 'flex';
  document.body.style.overflow = 'hidden';

  formStep1.style.display = 'block';
  formStep2.style.display = 'none';
  leadForm.reset();

  nameInput?.focus();
}

function closeForm() {
  const modal = document.getElementById('lead-form-modal');
  if (!modal) return;

  modal.style.display = 'none';
  document.body.style.overflow = '';
}

// Form submission state guard
let isSubmitting = false;
let formTimeoutId = null;

function validateEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

async function handleFormSubmit(e) {
  e.preventDefault();

  if (isSubmitting) return;

  const submitBtn = document.getElementById('form-submit-btn');
  const formStep1 = document.getElementById('form-step-1');
  const formStep2 = document.getElementById('form-step-2');
  const leadForm = document.getElementById('lead-form');

  if (!submitBtn || !formStep1 || !formStep2 || !leadForm) return;

  const formData = new FormData(leadForm);
  const data = Object.fromEntries(formData);

  // Validate email
  if (data.email && !validateEmail(data.email)) {
    const emailInput = document.getElementById('email');
    if (emailInput) {
      emailInput.focus();
      emailInput.setCustomValidity('Por favor, insira um email válido');
      emailInput.reportValidity();
      setTimeout(() => emailInput.setCustomValidity(''), 3000);
    }
    return;
  }

  isSubmitting = true;
  submitBtn.disabled = true;
  submitBtn.textContent = 'Enviando...';

  // Clear any existing timeout
  if (formTimeoutId) {
    clearTimeout(formTimeoutId);
    formTimeoutId = null;
  }

  try {
    await new Promise(resolve => setTimeout(resolve, 1500));

    // Check if modal is still open before updating UI
    const modal = document.getElementById('lead-form-modal');
    if (!modal || modal.style.display !== 'flex') {
      isSubmitting = false;
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Solicite Proposta';
      }
      return;
    }

    // Form submission - API integration pending
    // Data captured: name, email, budget
    // TODO: Integrate with backend API when available

    formStep1.style.display = 'none';
    formStep2.style.display = 'block';

    formTimeoutId = setTimeout(() => {
      const currentModal = document.getElementById('lead-form-modal');
      if (currentModal && currentModal.style.display === 'flex') {
        closeForm();
      }
      if (formStep1) formStep1.style.display = 'block';
      if (formStep2) formStep2.style.display = 'none';
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Solicite Proposta';
      }
      isSubmitting = false;
      formTimeoutId = null;
    }, 4000);
  } catch (error) {
    // Silent error handling - reset form state
    isSubmitting = false;
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Solicite Proposta';
    }
    // Show error state to user
    if (formStep1) formStep1.style.display = 'block';
    if (formStep2) formStep2.style.display = 'none';
  }
}

// --- LOGO MODAL ---
let activeLogoIndex = null;

function toggleLogoModal(index) {
  if (index === undefined || index === null || isNaN(index)) return;

  const modals = document.querySelectorAll('.logo-modal');
  const currentModal = document.querySelector(`.logo-modal[data-logo-index="${index}"]`);

  if (activeLogoIndex === index) {
    currentModal?.classList.remove('active');
    activeLogoIndex = null;
  } else {
    modals.forEach(m => m.classList.remove('active'));
    if (currentModal) {
      currentModal.classList.add('active');
      activeLogoIndex = index;
    }
  }
}

// --- EVENT DELEGATION ---
function parseId(value) {
  const id = parseInt(value, 10);
  return (!isNaN(id) && id > 0) ? id : null;
}

function initEventDelegation() {
  // Single click handler
  document.addEventListener('click', (e) => {
    const target = e.target;

    // Portfolio & Videos
    const projectBtn = target.closest('.portfolio-card');
    const videoBtn = target.closest('.video-card');
    if (projectBtn) {
      const id = parseId(projectBtn.dataset.projectId);
      if (id) {
        openProject(id);
        return;
      }
    }
    if (videoBtn) {
      const id = parseId(videoBtn.dataset.videoId);
      if (id) {
        openProject(id);
        return;
      }
    }

    // Logo CTA (check before logo-item to prevent event bubbling)
    const logoCta = target.closest('.logo-cta');
    if (logoCta) {
      e.stopPropagation();
      openForm(logoCta.dataset.formPreset || 'similar');
      return;
    }

    // Logo modals
    const logoItem = target.closest('.logo-item');
    if (logoItem) {
      const index = parseId(logoItem.dataset.logoIndex);
      if (index !== null) {
        toggleLogoModal(index);
        return;
      }
    }

    // CTA buttons
    if (target.matches('.cta-link, .contact-cta')) {
      openForm(target.dataset.formPreset || 'custom');
      return;
    }

    // Modal CTA
    if (target.matches('.modal-cta')) {
      closeProjectAndOpenForm(target.dataset.formPreset || 'similar');
      return;
    }

    // Modal close buttons
    if (target.closest('.modal-close')) {
      closeProject();
      return;
    }
    if (target.closest('.form-close')) {
      closeForm();
      return;
    }

    // Hero calendar button
    if (target.closest('.hero-cta')) {
      // Calendly URL pending - placeholder opens form instead
      openForm('custom');
      return;
    }

    // Modal overlay clicks
    const projectModal = document.getElementById('project-modal');
    const formModal = document.getElementById('lead-form-modal');
    if (target === projectModal) {
      closeProject();
      return;
    }
    if (target === formModal) {
      closeForm();
      return;
    }

    // Close logo modals on outside click
    if (!target.closest('.logo-modal')) {
      document.querySelectorAll('.logo-modal').forEach(m => m.classList.remove('active'));
      activeLogoIndex = null;
    }
  });

  // Keyboard handler
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeProject();
      closeForm();
    }
  });

  // Form submit
  const leadForm = document.getElementById('lead-form');
  leadForm?.addEventListener('submit', handleFormSubmit);
}

// --- RENDER STATIC SVGs ---
function renderStaticSVGs() {
  const heroCta = document.getElementById('hero-cta-btn');
  if (heroCta) {
    heroCta.innerHTML = createSVG('calendar', 14) + ' Agende conversa estratégica';
  }

  const contactUrgency = document.getElementById('contact-urgency');
  if (contactUrgency) {
    contactUrgency.innerHTML = createSVG('lock', 12) + '<p>Vagas limitadas para Q1 2026</p>';
  }

  const projectModalClose = document.getElementById('project-modal-close');
  if (projectModalClose) {
    projectModalClose.innerHTML = createSVG('close', 32);
  }

  const formClose = document.getElementById('form-close-btn');
  if (formClose) {
    formClose.innerHTML = createSVG('close', 24);
  }

  const formSuccessIcon = document.getElementById('form-success-icon');
  if (formSuccessIcon) {
    formSuccessIcon.innerHTML = createSVG('check', 48);
  }
}

// --- INIT ---
document.addEventListener('DOMContentLoaded', () => {
  // Hero video fallback
  const heroVideo = document.getElementById('hero-video');
  if (heroVideo) {
    heroVideo.onerror = () => {
      // Fallback: usar poster como background se vídeo falhar
      heroVideo.style.display = 'none';
      const heroSection = heroVideo.closest('.hero-section');
      if (heroSection) {
        heroSection.style.backgroundImage = `url('${heroVideo.poster}')`;
        heroSection.style.backgroundSize = 'cover';
        heroSection.style.backgroundPosition = 'center';
      }
    };
  }

  renderPortfolio();
  renderVideos();
  renderLogos();
  renderTestimonials();
  renderStaticSVGs();

  initScrollReveal();
  initExitIntent();
  initEventDelegation();

  const projectModal = document.getElementById('project-modal');
  const leadFormModal = document.getElementById('lead-form-modal');
  if (projectModal) projectModal.style.display = 'none';
  if (leadFormModal) leadFormModal.style.display = 'none';

  // --- NEW FORM LOGIC ---
  const inlineForm = document.getElementById('contact-form-inline');
  if (inlineForm) {
    inlineForm.addEventListener('submit', function (e) {
      e.preventDefault();

      const btn = this.querySelector('button');
      const originalText = btn.innerText;
      btn.innerText = 'Enviando...';
      btn.disabled = true;

      // Simulação de envio
      setTimeout(() => {
        // Hide form, Show success
        const formView = document.getElementById('form-view');
        const thankYouView = document.getElementById('thank-you-view');

        if (formView) formView.style.display = 'none';
        if (thankYouView) thankYouView.style.display = 'block';

        console.log("Lead capturado:", {
          name: this.name.value,
          contact: this.contact.value,
          message: this.message.value
        });

        // Scroll suave para o topo da mensagem de sucesso
        const contactSection = document.getElementById('contact');
        if (contactSection) contactSection.scrollIntoView({ behavior: 'smooth' });
      }, 1500);
    });
  }
});
