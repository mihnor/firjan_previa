#!/bin/bash
# FIRJAN XR - Complete Video Generation Script
# ==========================================
# Gera vídeos para todos os boards usando letterings numerados + narração

echo "🎬 FIRJAN XR - Gerando todos os vídeos..."
echo "======================================="

# Configurações globais
AUDIO_FILE="../Casa Firjan - tour virtual locução - Tratamento.wav"
RESOLUTION="1920x1080"
FPS="30"
IMAGE_DURATION="4"  # segundos por imagem

# Função para gerar vídeo de um board
generate_board_video() {
    local board_path="$1"
    local board_name=$(basename "$board_path")
    local output_file="$board_path/${board_name}_VIDEO.mp4"
    
    echo "🎥 Processando $board_name..."
    
    # Buscar todos os PNGs no board (letterings + assets)
    local images=($(find "$board_path" -name "*.png" | sort))
    local image_count=${#images[@]}
    
    if [ $image_count -eq 0 ]; then
        echo "  ⚠️  Nenhuma imagem encontrada em $board_name"
        return 1
    fi
    
    echo "  📸 Encontradas $image_count imagens"
    
    # Criar lista temporária para FFmpeg
    local filelist="$board_path/temp_filelist.txt"
    > "$filelist"  # Limpar arquivo
    
    for img in "${images[@]}"; do
        # Usar caminho absoluto para evitar problemas
        abs_img=$(realpath "$img")
        echo "file '$abs_img'" >> "$filelist"
        echo "duration $IMAGE_DURATION" >> "$filelist"
    done
    
    # Comando FFmpeg
    if [ -f "$AUDIO_FILE" ]; then
        echo "  🎵 Adicionando narração..."
        ffmpeg -y \
            -f concat -safe 0 -i "$filelist" \
            -i "$AUDIO_FILE" \
            -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1" \
            -c:v libx264 -pix_fmt yuv420p -r $FPS \
            -c:a aac -b:a 128k \
            -shortest \
            "$output_file"
    else
        echo "  🔇 Sem áudio - apenas slideshow"
        ffmpeg -y \
            -f concat -safe 0 -i "$filelist" \
            -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1" \
            -c:v libx264 -pix_fmt yuv420p -r $FPS \
            "$output_file"
    fi
    
    # Limpar arquivo temporário
    rm "$filelist"
    
    if [ $? -eq 0 ]; then
        local file_size=$(du -h "$output_file" | cut -f1)
        echo "  ✅ $board_name concluído! ($file_size)"
        return 0
    else
        echo "  ❌ Erro ao gerar $board_name"
        return 1
    fi
}

# Verificar se FFmpeg está instalado
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ FFmpeg não encontrado. Instale com:"
    echo "   macOS: brew install ffmpeg"
    echo "   Ubuntu: sudo apt install ffmpeg"
    exit 1
fi

# Verificar se o áudio existe
if [ ! -f "$AUDIO_FILE" ]; then
    echo "⚠️  Arquivo de áudio não encontrado: $AUDIO_FILE"
    echo "   Vídeos serão gerados sem narração"
fi

# Processar todos os boards
SUCCESS_COUNT=0
TOTAL_COUNT=0

for board_dir in BOARDS/BOARD_*; do
    if [ -d "$board_dir" ]; then
        ((TOTAL_COUNT++))
        if generate_board_video "$board_dir"; then
            ((SUCCESS_COUNT++))
        fi
        echo ""
    fi
done

# Sumário final
echo "======================================="
echo "✅ Processamento concluído!"
echo "📊 Sucesso: $SUCCESS_COUNT/$TOTAL_COUNT boards"
echo ""

# Listar vídeos gerados
echo "🎬 Vídeos gerados:"
find BOARDS -name "*_VIDEO.mp4" -exec ls -lh {} \; | awk '{print "  📹 " $9 " (" $5 ")"}'

echo ""
echo "🔧 Próximos passos:"
echo "1. Revisar os vídeos gerados"
echo "2. Fazer upload para o GitHub"
echo "3. Integrar com Figmin XR" 