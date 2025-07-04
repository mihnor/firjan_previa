#!/bin/bash
# FIRJAN XR - Simple Video Generation Script (Working Version)
# ==========================================================

echo "🎬 FIRJAN XR - Gerando vídeos (versão simplificada)..."
echo "======================================================"

# Configurações globais
AUDIO_FILE="../Casa Firjan - tour virtual locução - Tratamento.wav"

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
        # Usar caminho absoluto
        abs_img=$(realpath "$img")
        echo "file '$abs_img'" >> "$filelist"
        echo "duration 3" >> "$filelist"
    done
    
    # Comando FFmpeg - versão que funciona
    echo "  🎬 Gerando vídeo..."
    if [ -f "$AUDIO_FILE" ]; then
        echo "  🎵 Com narração..."
        ffmpeg -y \
            -f concat -safe 0 -i "$filelist" \
            -i "$AUDIO_FILE" \
            -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" \
            -c:v libx264 -pix_fmt yuv420p -r 30 \
            -c:a aac -b:a 128k \
            -shortest \
            "$output_file" >/dev/null 2>&1
    else
        echo "  🔇 Sem áudio..."
        ffmpeg -y \
            -f concat -safe 0 -i "$filelist" \
            -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" \
            -c:v libx264 -pix_fmt yuv420p -r 30 \
            "$output_file" >/dev/null 2>&1
    fi
    
    # Limpar arquivo temporário
    rm -f "$filelist"
    
    # Verificar se funcionou
    if [ -f "$output_file" ] && [ -s "$output_file" ]; then
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
        # Pular boards vazios
        if [ -z "$(find "$board_dir" -name "*.png" -print -quit)" ]; then
            echo "⏭️  Pulando $board_dir (sem imagens)"
            continue
        fi
        
        ((TOTAL_COUNT++))
        if generate_board_video "$board_dir"; then
            ((SUCCESS_COUNT++))
        fi
        echo ""
    fi
done

# Sumário final
echo "======================================================"
echo "✅ Processamento concluído!"
echo "📊 Sucesso: $SUCCESS_COUNT/$TOTAL_COUNT boards"
echo ""

# Listar vídeos gerados
echo "🎬 Vídeos gerados com sucesso:"
find BOARDS -name "*_VIDEO.mp4" -size +0c -exec ls -lh {} \; | awk '{print "  📹 " $9 " (" $5 ")"}'

echo ""
echo "🔧 Próximos passos:"
echo "1. Verificar qualidade dos vídeos"
echo "2. Fazer upload para GitHub" 
echo "3. Integrar com Figmin XR" 