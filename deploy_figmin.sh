#!/bin/bash
# deploy_figmin.sh - Script principal para deploy automático FIRJAN → Figmin XR

clear
echo "🚀 FIRJAN XR → FIGMIN DEPLOY AUTOMATION"
echo "========================================"
echo "⚡ Otimização automática do processo completo"
echo ""

# Verificar dependências
echo "🔍 Verificando dependências..."

DEPS_OK=true

# Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado"
    DEPS_OK=false
else
    echo "✅ Python3 OK"
fi

# FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ FFmpeg não encontrado"
    echo "   📦 Install: brew install ffmpeg (macOS)"
    DEPS_OK=false
else
    echo "✅ FFmpeg OK"
fi

if [ "$DEPS_OK" = false ]; then
    echo ""
    echo "❌ Dependências faltando! Instale-as antes de continuar."
    exit 1
fi

echo ""
echo "🎯 INICIANDO PROCESSO AUTOMATIZADO..."
echo "====================================="

# Etapa 1: Gerar URLs
echo ""
echo "📝 ETAPA 1/4: Gerando URLs do GitHub..."
python3 url_generator.py

if [ $? -ne 0 ]; then
    echo "❌ Erro na geração de URLs!"
    exit 1
fi

echo "✅ URLs geradas com sucesso!"

# Etapa 2: Converter áudio
echo ""
echo "🎬 ETAPA 2/4: Convertendo áudio para YouTube..."
chmod +x convert_audio.sh
./convert_audio.sh

if [ $? -ne 0 ]; then
    echo "❌ Erro na conversão de áudio!"
    exit 1
fi

echo "✅ Vídeo YouTube criado!"

# Etapa 3: Abrir ferramentas necessárias
echo ""
echo "🌐 ETAPA 3/4: Abrindo ferramentas..."

# Abrir URLs necessárias (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "   📤 Abrindo YouTube Upload..."
    open "https://youtube.com/upload" 2>/dev/null
    
    echo "   🎮 Abrindo Figmin XR..."
    open "https://figminxr.com" 2>/dev/null
    
    echo "   📊 Abrindo repositório GitHub..."
    open "https://github.com/mihnor/firjan_previa" 2>/dev/null
    
    sleep 2
fi

# Abrir arquivos locais
echo "   📝 Abrindo arquivos de referência..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    open "figmin_urls_simple.txt" 2>/dev/null
    open "figmin_checklist.md" 2>/dev/null
else
    echo "   📄 figmin_urls_simple.txt (para copy/paste)"
    echo "   📋 figmin_checklist.md (checklist)"
fi

# Etapa 4: Instruções finais
echo ""
echo "✅ ETAPA 4/4: INSTRUÇÕES FINAIS"
echo "==============================="
echo ""
echo "🎯 SEU WORKFLOW OTIMIZADO (20 min total):"
echo ""
echo "1. 📤 UPLOAD YOUTUBE (5 min):"
echo "   - Arquivo: FIRJAN_Guta_Voiceover_YT.mp4"
echo "   - Título: 'FIRJAN Guta Voiceover - XR Experience'"
echo "   - Visibilidade: NÃO LISTADO (Unlisted)"
echo "   - Copiar URL: https://youtu.be/SEU_ID_AQUI"
echo ""
echo "2. 🎮 FIGMIN XR SETUP (15 min):"
echo "   - Abrir Figmin XR → Create New → 'FIRJAN_Teaser'"
echo "   - Environment: Studio Space"
echo "   - Use arquivo: figmin_urls_simple.txt"
echo "   - Seguir: figmin_checklist.md"
echo ""
echo "📋 ARQUIVOS GERADOS:"
echo "   📄 figmin_urls_simple.txt    ← URLs para copy/paste"
echo "   📋 figmin_checklist.md       ← Checklist passo-a-passo"
echo "   🎬 FIRJAN_Guta_Voiceover_YT.mp4 ← Vídeo para YouTube"
echo "   📊 figmin_urls.json          ← Dados completos (backup)"

# Mostrar resumo das URLs principais
echo ""
echo "🔗 PREVIEW DAS URLs (primeiras 5):"
echo "=================================="

if [ -f "figmin_urls_simple.txt" ]; then
    head -n 15 figmin_urls_simple.txt | tail -n 10
    echo "   ... (ver arquivo completo: figmin_urls_simple.txt)"
fi

echo ""
echo "🎉 PROCESSO AUTOMATIZADO CONCLUÍDO!"
echo "=================================="
echo "⏱️  Tempo economizado: ~2-3 horas → 20 min"
echo "🎯 Próximo: Seguir figmin_checklist.md"
echo "📞 Dúvidas? Verifique FIGMIN_XR_URL_GENERATOR.md"
echo ""
echo "🚀 BOA SORTE COM O FIGMIN XR!" 