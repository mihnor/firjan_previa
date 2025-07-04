#!/bin/bash
# convert_audio.sh - Converte áudio MP3 para vídeo YouTube automaticamente

echo "🎬 FIRJAN Audio → YouTube Video Converter"
echo "==========================================="

# Configurações
AUDIO_FILE="AUDIO/VOICEOVER/FIRJAN_tour_virtual_guta_voiceover.mp3"
OUTPUT_VIDEO="FIRJAN_Guta_Voiceover_YT.mp4"
LOGO_FILE="firjan_logo_small.png"

# Verificar se o arquivo de áudio existe
if [ ! -f "$AUDIO_FILE" ]; then
    echo "❌ Erro: Arquivo de áudio não encontrado: $AUDIO_FILE"
    echo "📂 Verifique se o arquivo está no local correto."
    exit 1
fi

echo "✅ Arquivo de áudio encontrado: $AUDIO_FILE"

# Criar logo pequeno se não existir (imagem preta mínima)
if [ ! -f "$LOGO_FILE" ]; then
    echo "🎨 Criando logo mínimo para o vídeo..."
    
    # Criar imagem preta 640x360 usando ImageMagick ou ffmpeg
    if command -v convert &> /dev/null; then
        # Usando ImageMagick
        convert -size 640x360 xc:black -fill white -gravity center \
                -pointsize 24 -annotate +0+0 "FIRJAN" "$LOGO_FILE"
        echo "✅ Logo criado com ImageMagick"
    else
        # Criar com ffmpeg (fallback)
        ffmpeg -f lavfi -i color=black:size=640x360:duration=1 \
               -vf "drawtext=text='FIRJAN':fontsize=24:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2" \
               -frames:v 1 "$LOGO_FILE" -y 2>/dev/null
        echo "✅ Logo criado com FFmpeg"
    fi
fi

# Verificar se FFmpeg está instalado
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ FFmpeg não está instalado!"
    echo "📦 Para instalar no macOS: brew install ffmpeg"
    echo "📦 Para instalar no Ubuntu: sudo apt install ffmpeg"
    exit 1
fi

echo "🔄 Convertendo áudio para vídeo YouTube..."
echo "📄 Input:  $AUDIO_FILE"
echo "🎬 Output: $OUTPUT_VIDEO"

# Converter MP3 + imagem estática para vídeo MP4
ffmpeg -loop 1 -i "$LOGO_FILE" \
       -i "$AUDIO_FILE" \
       -c:v libx264 \
       -tune stillimage \
       -c:a aac \
       -b:a 128k \
       -pix_fmt yuv420p \
       -shortest \
       -vf "scale=640:360" \
       -movflags +faststart \
       "$OUTPUT_VIDEO" -y

# Verificar se a conversão foi bem-sucedida
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 CONVERSÃO CONCLUÍDA COM SUCESSO!"
    echo "=================================="
    echo "📁 Arquivo criado: $OUTPUT_VIDEO"
    
    # Obter informações do arquivo
    FILE_SIZE=$(du -h "$OUTPUT_VIDEO" | cut -f1)
    DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$OUTPUT_VIDEO" 2>/dev/null | cut -d. -f1)
    
    echo "📊 Tamanho: $FILE_SIZE"
    echo "⏱️  Duração: ${DURATION}s"
    echo ""
    echo "🚀 PRÓXIMOS PASSOS:"
    echo "=================="
    echo "1. 📤 Upload no YouTube:"
    echo "   - Acesse: https://youtube.com/upload"
    echo "   - Arquivo: $OUTPUT_VIDEO"
    echo "   - Título: 'FIRJAN Guta Voiceover - XR Experience'"
    echo "   - Visibilidade: 'Não listado' (Unlisted)"
    echo ""
    echo "2. 🔗 Copie a URL do YouTube"
    echo "3. 🎯 Use no Figmin XR:"
    echo "   - Import web content → YouTube"
    echo "   - Nome: 'Guta_Audio'"
    echo "   - Scale: 0.01 (invisível)"
    echo "   - Position: center (0,0,0)"
    echo ""
    echo "4. 🎮 Continue com figmin_checklist.md"
    
    # Abrir YouTube upload automaticamente (macOS)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo ""
        echo "🌐 Abrindo YouTube Upload..."
        open "https://youtube.com/upload"
    fi
    
else
    echo "❌ Erro na conversão!"
    echo "🔍 Verifique se todos os arquivos estão disponíveis."
    exit 1
fi 