#!/usr/bin/env bash
# sync-skills.sh — sincroniza skills bundled do plugin com a versão global do autor.
#
# USO:
#   ./bin/sync-skills.sh         # sync + sanitize
#   ./bin/sync-skills.sh --dry   # mostra o que mudaria sem aplicar
#
# O QUE FAZ:
# 1. Copia ~/.claude/skills/{landing-page-builder,taste-skill,ui-ux-pro-max,proposta}
#    → plugins/dna-operacional/skills/
# 2. Aplica sanitização (remove refs hardcoded a Ahoy/Flavio/dados pessoais)
# 3. Limpa __pycache__ e arquivos temporários
# 4. Faz scan final pra confirmar 0 leaks
#
# RODAR ANTES DE BUMPAR VERSÃO DO PLUGIN.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_SRC="$HOME/.claude/skills"
SKILLS_DST="$PLUGIN_ROOT/plugins/dna-operacional/skills"

DRY_RUN=0
[[ "${1:-}" == "--dry" ]] && DRY_RUN=1

SKILLS=("landing-page-builder" "taste-skill" "ui-ux-pro-max" "proposta")

echo "→ sync-skills.sh"
echo "  src: $SKILLS_SRC"
echo "  dst: $SKILLS_DST"
[[ $DRY_RUN -eq 1 ]] && echo "  ⚠ DRY RUN — nada será modificado"
echo ""

# 1. Validar que skills existem na global
for skill in "${SKILLS[@]}"; do
  if [[ ! -d "$SKILLS_SRC/$skill" ]]; then
    echo "❌ ~/.claude/skills/$skill não existe. Não posso sincronizar."
    exit 1
  fi
done

# 2. Copiar
if [[ $DRY_RUN -eq 0 ]]; then
  mkdir -p "$SKILLS_DST"
  for skill in "${SKILLS[@]}"; do
    rm -rf "$SKILLS_DST/$skill"
    cp -R "$SKILLS_SRC/$skill" "$SKILLS_DST/"
    echo "  ✓ copiado: $skill"
  done
else
  for skill in "${SKILLS[@]}"; do
    echo "  [dry] copiaria: $skill"
  done
fi

# 3. Limpar pycache e .DS_Store
if [[ $DRY_RUN -eq 0 ]]; then
  find "$SKILLS_DST" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
  find "$SKILLS_DST" \( -name "*.pyc" -o -name "*.pyo" -o -name ".DS_Store" \) -delete 2>/dev/null || true
fi

# 4. Sanitizar (substituições em massa)
if [[ $DRY_RUN -eq 0 ]]; then
  echo ""
  echo "→ Sanitizando..."

  for skill in "${SKILLS[@]}"; do
    find "$SKILLS_DST/$skill" -type f \( -name "*.md" -o -name "*.txt" \) | while read -r f; do
      sed -i '' \
        -e 's|/Users/flavioahoy/Documents/projects/propostas/|${PROPOSTAS_DIR}/|g' \
        -e 's|/Users/flavioahoy/Documents/projects/landing-pages/consultoria-ia/|<diretório original do framework no projeto fonte>|g' \
        -e 's|contato@ahoydigital\.com\.br|{{EMAIL_EMPRESA}}|g' \
        -e 's|contato@ahoydigital\.ag|{{EMAIL_EMPRESA}}|g' \
        -e 's|flavio@ahoy\.digital|{{EMAIL_EMPRESA}}|g' \
        -e 's|@flavioahoy|{{HANDLE}}|g' \
        -e 's|AHOY DIGITAL-SVG/Ahoy Digital_10\.svg|{{LOGO_DARK_PATH}}|g' \
        -e 's|AHOY%20DIGITAL-SVG/Ahoy%20Digital_10\.svg|{{LOGO_DARK_PATH}}|g' \
        -e 's|AHOY DIGITAL-SVG/Ahoy Digital_8\.svg|{{LOGO_LIGHT_PATH}}|g' \
        -e 's|AHOY%20DIGITAL-SVG/Ahoy%20Digital_8\.svg|{{LOGO_LIGHT_PATH}}|g' \
        -e 's|nofex-expanded-sans-serif-2026-03-05-01-41-51-utc/Web-TT/Nofex\.woff2|{{FONT_HEADLINE_PATH_WOFF2}}|g' \
        -e 's|nofex-expanded-sans-serif-2026-03-05-01-41-51-utc/Web-TT/Nofex\.woff|{{FONT_HEADLINE_PATH_WOFF}}|g' \
        -e "s|font-family: 'Nofex'|font-family: '{{FONT_HEADLINE_NAME}}'|g" \
        -e "s|'Nofex',|'{{FONT_HEADLINE_NAME}}',|g" \
        -e 's|Nofex (|{{FONT_HEADLINE_NAME}} (|g' \
        -e 's|Ahoy Digital Ltda\.|{{EMPRESA_RAZAO_SOCIAL}}|g' \
        -e 's|Ahoy Digital|{{EMPRESA}}|g' \
        -e 's|fonte NOFEX|fonte {{FONT_HEADLINE_NAME}}|g' \
        -e 's|branding Ahoy|branding configurável|g' \
        -e 's|Propostas Ahoy|Propostas {{EMPRESA}}|g' \
        -e 's|Ahoy AI|{{EMPRESA}}|g' \
        -e 's|interno Ahoy|interno {{EMPRESA}}|g' \
        -e 's|Custos Ahoy|Custos {{EMPRESA}}|g' \
        -e 's|Kestra (orquestração de workflows)|Ferramenta interna A (orquestração de workflows)|g' \
        -e 's|Kestra (orquestração)|Ferramenta interna A (orquestração)|g' \
        -e 's|Questra (automação)|Ferramenta interna B (automação)|g' \
        -e 's|Mastra (framework de agentes IA)|Ferramenta interna C (framework de agentes IA)|g' \
        -e 's|terracotta/coral faz parte da identidade visual da marca (como Ahoy Digital #e25e3e)|terracotta/coral faz parte da identidade visual da marca|g' \
        -e 's|quem é a Ahoy|quem é a {{EMPRESA}}|g' \
        -e 's|Introdução da Ahoy|Introdução da {{EMPRESA}}|g' \
        -e 's|{{FRASE_DESTAQUE_AHOY}}|{{FRASE_DESTAQUE}}|g' \
        -e 's|Kestra/Questra pelo nome (ferramenta interna da Ahoy)|nomes de ferramentas internas da empresa|g' \
        -e 's|{{SOLUÇÃO_AHOY_NOME}}|{{SOLUCAO_NOME}}|g' \
        -e 's|{{SOLUÇÃO_AHOY}}|{{SOLUCAO}}|g' \
        -e 's|{{VALOR_AHOY}}|{{VALOR_PROPOSTA}}|g' \
        "$f"
    done
  done

  # Sanitizar paleta hardcoded em design-system.md da proposta (se houver)
  PROPOSTA_DS="$SKILLS_DST/proposta/references/design-system.md"
  if [[ -f "$PROPOSTA_DS" ]]; then
    sed -i '' \
      -e 's|--dark: #010B12; --green: #2BC20E; --green-bright: #39FF13;|--dark: {{COR_PRIMARIA}}; --green: {{COR_DESTAQUE}}; --green-bright: {{COR_DESTAQUE_BRIGHT}};|g' \
      -e 's|--lime: #9CFF00; --light: #F2F2F2;|--lime: {{COR_LIME}}; --light: {{COR_FUNDO_CLARO}};|g' \
      "$PROPOSTA_DS"
  fi

  echo "  ✓ sanitização aplicada"
fi

# 5. Adicionar .gitignore
if [[ $DRY_RUN -eq 0 ]]; then
  cat > "$SKILLS_DST/.gitignore" <<'EOF'
__pycache__/
*.pyc
*.pyo
.DS_Store
EOF
fi

# 6. Scan final — falhar se sobrar referência não-autoria
echo ""
echo "→ Scan de leaks..."
LEAKS=$(grep -ric -E "ahoy|flavio|@flavioahoy|nofex" "$SKILLS_DST" 2>/dev/null \
  | grep -v ":0$" \
  | grep -vE "(orquestração|orquestração)" \
  || true)

if [[ -n "$LEAKS" ]]; then
  echo "⚠️ Possíveis leaks detectados (revisa manualmente):"
  echo "$LEAKS"
  echo ""
  echo "Use 'grep -nEo \"ahoy|flavio|nofex\" -i <arquivo>' pra ver o match exato."
  echo "Falsos positivos comuns: 'orQUESTRAção', 'ManiFESTOS'."
  exit 2
fi

echo "✅ 0 leaks. Skills bundled estão limpos."
echo ""
echo "Próximos passos:"
echo "  1. git status (ver mudanças)"
echo "  2. git diff plugins/dna-operacional/skills/ (revisar)"
echo "  3. Bumpar versão em plugin.json"
echo "  4. Commit + tag"
