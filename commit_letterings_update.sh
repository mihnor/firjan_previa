#!/bin/bash
# FIRJAN XR - GitHub Update Script
# ===============================
# Atualiza letterings numerados e estrutura de boards no GitHub

echo "🔄 FIRJAN XR - Atualizando GitHub..."
echo "===================================="

# Verificar se estamos em um repositório git
if [ ! -d .git ]; then
    echo "❌ Não é um repositório Git. Execute 'git init' primeiro."
    exit 1
fi

# Verificar status atual
echo "📊 Status atual do repositório:"
git status --porcelain

echo ""
echo "📁 Adicionando letterings numerados..."

# Adicionar todos os letterings organizados
git add FIRJAN_XR_ASSETS/BOARDS/BOARD_01_PERGUNTA/01_*.png
git add FIRJAN_XR_ASSETS/BOARDS/BOARD_02_GUTENBERG/02_*.png  
git add FIRJAN_XR_ASSETS/BOARDS/BOARD_03_TIPOGRAFIA/03_*.png
git add FIRJAN_XR_ASSETS/BOARDS/BOARD_04_ESCRITORES/04_*.png
git add FIRJAN_XR_ASSETS/BOARDS/BOARD_05_PARQUES/05_*.png
git add FIRJAN_XR_ASSETS/BOARDS/BOARD_06_CENOGRAFIA/06_*.png
git add FIRJAN_XR_ASSETS/BOARDS/BOARD_09_EXPERIENCIA/09_*.png
git add FIRJAN_XR_ASSETS/BOARDS/BOARD_12_CASA_FIRJAN/12_*.png

# Adicionar scripts
git add generate_all_videos.sh
git add commit_letterings_update.sh

# Adicionar arquivos de configuração e relatórios
git add FIRJAN_XR_ASSETS/update_*.py
git add FIRJAN_XR_ASSETS/*.json

echo "✅ Arquivos adicionados ao staging"

# Verificar o que será commitado
echo ""
echo "📋 Arquivos que serão commitados:"
git diff --cached --name-only | sed 's/^/  ✓ /'

echo ""
read -p "🤔 Continuar com o commit? (y/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Fazer commit
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    TOTAL_FILES=$(git diff --cached --name-only | wc -l | tr -d ' ')
    
    echo "💾 Fazendo commit..."
    git commit -m "Add letterings numerados organization

📁 Files organized: $TOTAL_FILES
🎯 Boards updated: 8 boards  
🎬 Video generation script added
⏰ Updated: $TIMESTAMP

- Board 01: 3 letterings (pergunta)
- Board 02: 2 letterings (gutenberg)  
- Board 03: 1 lettering (tipografia)
- Board 04: 1 lettering (escritores)
- Board 05: 1 lettering (parques)
- Board 06: 2 letterings (cenografia)
- Board 09: 1 lettering (experiencia)
- Board 12: 1 lettering (casa firjan)

Ready for video generation and XR integration!"

    if [ $? -eq 0 ]; then
        echo "✅ Commit realizado com sucesso!"
        
        echo ""
        read -p "🚀 Fazer push para o GitHub? (y/N): " -n 1 -r
        echo
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "📤 Fazendo push..."
            git push origin $(git branch --show-current)
            
            if [ $? -eq 0 ]; then
                echo "🎉 Push concluído! Letterings atualizados no GitHub!"
            else
                echo "❌ Erro no push. Verifique a conexão e permissões."
            fi
        else
            echo "⏸️  Push cancelado. Execute 'git push' manualmente quando pronto."
        fi
    else
        echo "❌ Erro no commit."
        exit 1
    fi
else
    echo "❌ Commit cancelado."
    exit 1
fi

echo ""
echo "📈 Estatísticas finais:"
echo "  📁 Total de boards: $(find FIRJAN_XR_ASSETS/BOARDS -name "BOARD_*" -type d | wc -l | tr -d ' ')"
echo "  🖼️  Total de letterings: $(find FIRJAN_XR_ASSETS/BOARDS -name "[0-9][0-9]_*.png" | wc -l | tr -d ' ')"
echo "  📊 Tamanho total: $(du -sh FIRJAN_XR_ASSETS/BOARDS | cut -f1)"

echo ""
echo "🔧 Próximos passos:"
echo "1. 🎬 Execute: ./generate_all_videos.sh"
echo "2. 🌐 Integre com Figmin XR"
echo "3. 🧪 Teste em ambiente XR" 