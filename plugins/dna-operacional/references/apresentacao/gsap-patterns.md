# GSAP Patterns — /apresentacao

Padrões de animação GSAP 3.12.5 usados pela skill `/apresentacao`. Referência rápida: a skill consulta esse arquivo ao gerar `main.js` e escolhe snippets por tipo de cena.

**Plugins obrigatórios:**
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/Observer.min.js"></script>
```

```js
gsap.registerPlugin(ScrollTrigger, Observer);
```

---

## 1. Z-Axis Scene Transition (coração do engine)

Cenas não deslizam lado a lado — elas fazem zoom in/out em Z.

```js
const transitionToScene = (from, to, direction = 'next') => {
  State.isAnimating = true;
  const fromEl = scenes[from];
  const toEl = scenes[to];

  const tl = gsap.timeline({
    onComplete: () => { fromEl.classList.remove('active'); State.isAnimating = false; State.currIndex = to; }
  });

  // Leave: zoom out (escala 1 → 0.2, opacity 1 → 0, Z -800)
  tl.to(fromEl, {
    scale: direction === 'next' ? 0.2 : 5,
    opacity: 0,
    z: direction === 'next' ? -800 : 800,
    duration: 0.8,
    ease: 'power3.inOut'
  }, 0);

  // Enter: zoom in (escala 5 → 1, opacity 0 → 1, Z 800 → 0)
  toEl.classList.add('active');
  tl.fromTo(toEl, {
    scale: direction === 'next' ? 5 : 0.2,
    opacity: 0,
    z: direction === 'next' ? 800 : -800
  }, {
    scale: 1,
    opacity: 1,
    z: 0,
    duration: 0.8,
    ease: 'power3.inOut'
  }, 0);

  return tl;
};
```

---

## 2. Neon Flicker (Hero title)

Sequência 4-fase: scare → attempt → ignition → stabilize.

```js
const neonFlickerIn = (titleEl) => {
  const tl = gsap.timeline();
  // Phase 1: Scare (quick blink)
  tl.set(titleEl, { className: 'mega-title split-chars neon-on' })
    .to(titleEl, { duration: 0.2, onComplete: () => titleEl.classList.remove('neon-on') })
    .set(titleEl, { className: 'mega-title split-chars neon-off' }, '+=0.3');

  // Phase 2: Attempt
  tl.to(titleEl, { opacity: 0.5, duration: 0.1 })
    .to(titleEl, { opacity: 0.1, duration: 0.2 });

  // Phase 3: Ignition (random strobe 6x)
  for (let i = 0; i < 6; i++) {
    tl.set(titleEl, { className: `mega-title split-chars neon-${Math.random() > 0.5 ? 'on' : 'off'}` })
      .to(titleEl, { opacity: 0.2 + Math.random() * 0.6, duration: 0.05 + Math.random() * 0.1 });
  }

  // Phase 4: Stabilize
  tl.set(titleEl, { className: 'mega-title split-chars neon-on' })
    .to(titleEl, { opacity: 1, duration: 0.3, ease: 'power2.out' });

  return tl;
};
```

---

## 3. Glitch RGB Loop (Hazard scene)

Random triggers de .active em glitch-layer.

```js
const startGlitchLoop = (layerEl) => {
  const trigger = () => {
    layerEl.classList.add('active');
    gsap.delayedCall(0.3 + Math.random() * 0.2, () => layerEl.classList.remove('active'));
  };
  const interval = setInterval(trigger, 2500 + Math.random() * 2000);
  return () => clearInterval(interval); // cleanup function
};
```

---

## 4. Marquee Infinite Scroll

Track duplicado (50% width cada), translate -50% loop.

```js
const startMarquee = (trackEl, duration = 15, reverse = false) => {
  return gsap.to(trackEl, {
    xPercent: reverse ? 50 : -50,
    duration,
    ease: 'none',
    repeat: -1
  });
};
```

---

## 5. Tilt Card on Hover (3D)

Segue mouse. Usado em `cards` e `pipeline-node`.

```js
const enableTiltCard = (cardEl) => {
  const handler = (e) => {
    const rect = cardEl.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width - 0.5;
    const y = (e.clientY - rect.top) / rect.height - 0.5;
    gsap.to(cardEl, {
      rotationY: x * 15,
      rotationX: -y * 15,
      duration: 0.4,
      ease: 'power2.out',
      transformPerspective: 1000
    });
  };
  const reset = () => gsap.to(cardEl, { rotationY: 0, rotationX: 0, duration: 0.6, ease: 'elastic.out(1, 0.4)' });
  cardEl.addEventListener('mousemove', handler);
  cardEl.addEventListener('mouseleave', reset);
  return () => { cardEl.removeEventListener('mousemove', handler); cardEl.removeEventListener('mouseleave', reset); };
};
```

---

## 6. Parallax Background (Radar sweep)

Rotação contínua linear em elemento com `conic-gradient`.

```js
const startRadarSweep = (radarEl) => {
  return gsap.to(radarEl, {
    rotation: 360,
    duration: 4,
    ease: 'none',
    repeat: -1,
    transformOrigin: '50% 50%'
  });
};
```

---

## 7. Scroll Trap — Pipeline Horizontal

Observer consome delta até `progress` sair de [0, 1]. Enquanto dentro, anima track. Fora, libera pra próxima cena.

```js
const createPipelineTrap = (sceneEl, trackEl) => {
  let progress = 0;
  const totalWidth = trackEl.scrollWidth - window.innerWidth;

  return Observer.create({
    target: sceneEl,
    type: 'wheel,touch',
    onChange: (self) => {
      if (State.isAnimating) return;
      const delta = self.deltaY || -self.deltaX;
      const step = 0.05;
      const newProg = progress + (delta * step / 100);

      if (newProg < 0) {
        // Libera pra cena anterior
        transitionToScene(State.currIndex, State.currIndex - 1, 'prev');
        return;
      }
      if (newProg > 1) {
        transitionToScene(State.currIndex, State.currIndex + 1, 'next');
        return;
      }

      progress = newProg;
      gsap.to(trackEl, { x: -progress * totalWidth, duration: 0.5, ease: 'power2.out' });
    }
  });
};
```

---

## 8. Scroll Trap — Methodology 3D Stack

Placas empilhadas em Z. Cada scroll-tick ativa próxima placa.

```js
const createMethodologyStack = (sceneEl, plates) => {
  let activeIdx = 0;
  plates.forEach((plate, i) => {
    gsap.set(plate, {
      z: -i * 200,
      opacity: i === 0 ? 1 : 0.3,
      scale: 1 - i * 0.08
    });
  });

  return Observer.create({
    target: sceneEl,
    type: 'wheel,touch',
    onChange: (self) => {
      if (State.isAnimating) return;
      const delta = self.deltaY;
      const nextIdx = activeIdx + (delta > 0 ? 1 : -1);
      if (nextIdx < 0 || nextIdx >= plates.length) {
        const dir = delta > 0 ? 'next' : 'prev';
        transitionToScene(State.currIndex, State.currIndex + (dir === 'next' ? 1 : -1), dir);
        return;
      }
      activeIdx = nextIdx;
      plates.forEach((plate, i) => {
        gsap.to(plate, {
          z: -(i - activeIdx) * 200,
          opacity: i === activeIdx ? 1 : 0.3,
          scale: i === activeIdx ? 1 : 1 - Math.abs(i - activeIdx) * 0.08,
          duration: 0.6,
          ease: 'power3.inOut'
        });
      });
    }
  });
};
```

---

## 9. splitText Char-by-Char Reveal

Helper `splitText()` quebra innerText em spans. Depois anima cada span.

```js
const revealCharsByChars = (el, stagger = 0.03) => {
  const chars = el.querySelectorAll('span');
  return gsap.fromTo(chars,
    { opacity: 0, y: 40, rotationX: -90 },
    { opacity: 1, y: 0, rotationX: 0, duration: 0.6, stagger, ease: 'back.out(1.5)' }
  );
};
```

---

## 10. countUp Animated Number

Helper já em `main.js`. Usado em `kpi-number`, `savings-percent`, `new-price`.

```js
const countUp = (el, duration = 1.5) => {
  const target = parseInt(el.getAttribute('data-count'), 10);
  if (isNaN(target)) { el.textContent = el.getAttribute('data-count') || ''; return; }
  const start = performance.now();
  const update = (now) => {
    const p = Math.min((now - start) / (duration * 1000), 1);
    el.textContent = Math.floor((1 - Math.pow(1 - p, 3)) * target).toLocaleString('pt-BR');
    if (p < 1) requestAnimationFrame(update);
    else el.textContent = target.toLocaleString('pt-BR');
  };
  requestAnimationFrame(update);
};
```

---

## 11. Custom Cursor Follow

Dot instantâneo, ring com lag (smooth).

```js
const initCustomCursor = () => {
  const dot = document.querySelector('.cursor-dot');
  const ring = document.querySelector('.cursor-ring');
  const xTo = gsap.quickTo(ring, 'x', { duration: 0.4, ease: 'power2' });
  const yTo = gsap.quickTo(ring, 'y', { duration: 0.4, ease: 'power2' });
  const xDot = gsap.quickTo(dot, 'x', { duration: 0.1, ease: 'power2' });
  const yDot = gsap.quickTo(dot, 'y', { duration: 0.1, ease: 'power2' });

  window.addEventListener('mousemove', (e) => {
    xTo(e.clientX); yTo(e.clientY);
    xDot(e.clientX); yDot(e.clientY);
  });
};
```

---

## 12. Stamp Seal Explosive Entrance

```js
const stampEntrance = (stampEl) => {
  gsap.fromTo(stampEl,
    { scale: 3, rotation: -45, opacity: 0 },
    { scale: 1, rotation: -15, opacity: 1, duration: 0.6, ease: 'elastic.out(1, 0.3)' }
  );
};
```

---

## 13. Cleanup Pattern (obrigatório em cada cena)

Toda cena com animação contínua (marquee, glitch loop, radar) DEVE retornar cleanup.

```js
const sceneAnimations = {
  hazard: {
    enter: (el) => {
      const marqueeTween = startMarquee(el.querySelector('.marquee-track'));
      const stopGlitch = startGlitchLoop(el.querySelector('.glitch-layer'));
      return () => { marqueeTween.kill(); stopGlitch(); };
    }
  }
};

// No leave da cena:
const cleanup = sceneCleanups.get(sceneId);
if (cleanup) { cleanup(); sceneCleanups.delete(sceneId); }
```

**Regra ferro:** `gsap.killTweensOf(target)` em leave pra evitar memory leak.

---

## 14. Observer (input unificado)

Wheel + touch + keyboard em um handler.

```js
Observer.create({
  type: 'wheel,touch,pointer',
  wheelSpeed: -1,
  onUp: () => handleNavigation('prev'),
  onDown: () => handleNavigation('next'),
  tolerance: 10,
  preventDefault: true
});

window.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') handleNavigation('next');
  if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') handleNavigation('prev');
});
```
