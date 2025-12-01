#!/bin/sh
# Build script simples para Docker (shell compatível)
# Minifica CSS e JS usando sed/tr (ferramentas básicas do Alpine)
# AVISO: Regex simples - pode quebrar em edge cases

echo "Minificando arquivos..."

# Minificar CSS
if [ -f /tmp/styles.css ]; then
  cat /tmp/styles.css | \
    sed 's|/\*[^*]*\*\/||g' | \
    tr -s ' ' | \
    sed 's/[[:space:]]*{[[:space:]]*/{/g' | \
    sed 's/[[:space:]]*}[[:space:]]*/}/g' | \
    sed 's/[[:space:]]*;[[:space:]]*/;/g' | \
    sed 's/[[:space:]]*:[[:space:]]*/:/g' | \
    sed 's/[[:space:]]*,[[:space:]]*/,/g' | \
    tr -d '\n' > /tmp/styles.min.css
  echo "✓ styles.min.css criado"
fi

# Minificar JS (cuidado: pode quebrar strings com //)
if [ -f /tmp/app.js ]; then
  cat /tmp/app.js | \
    sed 's|/\*[^*]*\*\/||g' | \
    sed 's|//.*||g' | \
    tr -s ' ' | \
    sed 's/[[:space:]]*{[[:space:]]*/{/g' | \
    sed 's/[[:space:]]*}[[:space:]]*/}/g' | \
    sed 's/[[:space:]]*;[[:space:]]*/;/g' | \
    sed 's/[[:space:]]*,[[:space:]]*/,/g' | \
    tr -d '\n' > /tmp/app.min.js
  echo "✓ app.min.js criado"
fi

echo "Build completo!"

