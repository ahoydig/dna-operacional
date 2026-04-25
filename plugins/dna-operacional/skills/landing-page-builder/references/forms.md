# Padroes de Formulario

## Estrutura Base (Netlify Forms)

```html
<form name="NOME_UNICO" method="POST" data-netlify="true" netlify-honeypot="bot-field" data-form>
  <input type="hidden" name="form-name" value="NOME_UNICO">
  <p hidden><label>Nao preencha: <input name="bot-field"></label></p>

  <div class="form-group">
    <label class="form-label" for="nome">Nome</label>
    <input type="text" id="nome" name="nome" class="form-input" required autocomplete="name">
  </div>

  <div class="form-group">
    <label class="form-label" for="email">E-mail</label>
    <input type="email" id="email" name="email" class="form-input" required autocomplete="email">
  </div>

  <div class="form-group">
    <label class="form-label" for="telefone">WhatsApp</label>
    <input type="tel" id="telefone" name="telefone" class="form-input" required autocomplete="tel">
  </div>

  <div class="form-feedback"></div>
  <button type="submit" class="btn">CTA</button>
</form>
```

## Regras Criticas

- `form name` DEVE coincidir com `input[name="form-name"]`
- Atributo `data-form` obrigatorio (JS selector)
- IDs unicos na pagina (prefixar se multiplos forms)
- Netlify detecta forms no build (HTML deve ser estatico)

## intl-tel-input (CDN)

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/intl-tel-input@24.6.0/build/css/intlTelInput.css">
<script src="https://cdn.jsdelivr.net/npm/intl-tel-input@24.6.0/build/js/intlTelInput.min.js" defer></script>
```

```javascript
const iti = intlTelInput(tel, {
  initialCountry: 'br',
  preferredCountries: ['br', 'us', 'pt'],
  utilsScript: 'https://cdn.jsdelivr.net/npm/intl-tel-input@24.6.0/build/js/utils.js',
});

// Validacao
iti.isValidNumber(); // true/false
iti.getNumber();     // "+5511999999999" (E.164)
```

## Validacao de Email (bloqueia temp emails)

```javascript
const tempDomains = ['tempmail','guerrillamail','10minutemail','mailinator','yopmail','trashmail'];

function isValidEmail(email) {
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return false;
  const domain = email.split('@')[1].toLowerCase();
  return !tempDomains.some(temp => domain.includes(temp));
}
```

## Submit AJAX (Netlify)

```javascript
const res = await fetch(form.getAttribute('action') || '/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams(new FormData(form)).toString(),
});
```

Detalhes criticos:
- URL de `form.getAttribute('action')`, nunca hardcoded
- Content-Type `application/x-www-form-urlencoded`, nao JSON
- Capturar nome/email ANTES do `form.reset()`

## Integracoes Server-Side (Netlify Functions)

Para integracoes com CRMs (GHL, HubSpot), usar Netlify Functions:

```
netlify/functions/
  waitlist.js    ← recebe POST, cria contato no CRM
```

API key como env var no Netlify (nunca no frontend):
```bash
netlify env:set GHL_API_KEY "valor"
```

## Modal de Formulario

Form HTML deve ser estatico (Netlify detecta no build):

```html
<div class="modal-overlay" id="modal-form" role="dialog">
  <div class="modal-content">
    <button type="button" class="modal-close">&times;</button>
    <form name="modal-form" method="POST" data-netlify="true" data-form>
      <!-- IDs com prefixo: modal-nome, modal-email -->
    </form>
  </div>
</div>
```

Fechar com Escape, click no overlay ou botao X.

## Thank You (na mesma pagina)

```javascript
function showThankYou(container, firstName) {
  container.innerHTML = `
    <div class="thank-you">
      <svg><!-- checkmark icon --></svg>
      <h2>Voce esta na lista, ${firstName}!</h2>
      <p>Mensagem de confirmacao.</p>
    </div>
  `;
}
```
