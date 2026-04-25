# Padroes de Animacao

## AOS (Animate on Scroll)

**Nunca no hero. Apenas em secoes de scroll.**

```javascript
AOS.init({
  once: true,
  duration: 600,
  disableMutationObserver: true, // CRITICO: previne CLS 0.7+
});
```

```html
<div data-aos="fade-up">Conteudo</div>
<div data-aos="fade-up" data-aos-delay="100">Com delay</div>
```

CDN:
```html
<link href="https://unpkg.com/aos@2.3.4/dist/aos.css" rel="stylesheet">
<script src="https://unpkg.com/aos@2.3.4/dist/aos.js" defer></script>
```

## IntersectionObserver (alternativa ao AOS)

Mais controle, sem dependencia externa:

```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('revealed');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });

cards.forEach((card, i) => {
  card.style.transitionDelay = `${i * 120}ms`;
  observer.observe(card);
});
```

CSS:
```css
.card { opacity: 0; transform: translateY(20px); transition: all 0.5s cubic-bezier(0.16,1,0.3,1); }
.card.revealed { opacity: 1; transform: translateY(0); }
```

## Typing Animation (terminal)

```javascript
function initTerminalTyping() {
  const lines = document.querySelectorAll('.terminal__line');
  lines.forEach(line => { line.style.opacity = '0'; line.style.transform = 'translateY(4px)'; });
  let delay = 400;
  lines.forEach(line => {
    const isBlank = line.classList.contains('terminal__line--blank');
    setTimeout(() => {
      line.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
      line.style.opacity = '1';
      line.style.transform = 'translateY(0)';
    }, delay);
    delay += isBlank ? 200 : 300 + Math.random() * 200;
  });
}
```

## Glitch Effect (text-shadow RGB split)

```css
.glitch {
  animation: glitch-text 4s infinite;
}

@keyframes glitch-text {
  0%, 78%, 100% { text-shadow: none; transform: none; }
  79% { text-shadow: -6px 0 #4ade80, 6px 0 #60a5fa; transform: translateX(-4px) skewX(-3deg); }
  80% { text-shadow: 5px 0 #4ade80, -5px 0 #60a5fa; transform: translateX(5px) skewX(2deg); }
  82% { text-shadow: none; transform: none; }
  90% { text-shadow: 7px 0 #4ade80, -7px 0 #60a5fa; transform: translateX(4px) skewX(-2deg); }
  93% { text-shadow: none; transform: none; }
}
```

## Cursor Piscante

```css
.cursor { animation: blink 1s step-end infinite; }
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
```

## Pulse (badges, indicadores)

```css
.dot { animation: pulse 2s ease infinite; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
```

## Scripts Pesados (Dynamic Import)

Nunca linkar Three.js, GSAP etc no HTML. Sempre lazy load:

```javascript
function lazyLoadModule(selector, loadFn) {
  const el = document.querySelector(selector);
  if (!el) return;
  const obs = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) { obs.disconnect(); loadFn(); }
  }, { rootMargin: '200px' });
  obs.observe(el);
}

lazyLoadModule('#secao-3d', async () => {
  const THREE = await import('three');
});
```

## Acessibilidade

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```
