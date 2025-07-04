#!/bin/bash

# Script para gerar vídeos .mp4 a partir dos arquivos de áudio .mp3
# Para uso no Figmin XR e YouTube

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== FIRJAN XR - Gerador de Vídeos para Voiceover ===${NC}"
echo -e "${YELLOW}Convertendo arquivos .mp3 para .mp4 com fundo do logotipo Firjan${NC}"

# Definir caminhos
AUDIO_DIR="."
LOGO_PATH="../../../firjan_logo_small.png"
OUTPUT_DIR="./videos"

# Criar diretório de saída se não existir
mkdir -p "$OUTPUT_DIR"

# Verificar se o ffmpeg está instalado
if ! command -v ffmpeg &> /dev/null; then
    echo -e "${RED}ERRO: ffmpeg não está instalado!${NC}"
    echo -e "${YELLOW}Instale o ffmpeg:${NC}"
    echo "  macOS: brew install ffmpeg"
    echo "  Ubuntu/Debian: sudo apt install ffmpeg"
    echo "  Windows: baixe de https://ffmpeg.org/download.html"
    exit 1
fi

# Verificar se o logo existe
if [ ! -f "$LOGO_PATH" ]; then
    echo -e "${RED}ERRO: Logo não encontrado em $LOGO_PATH${NC}"
    echo -e "${YELLOW}Usando fundo preto simples${NC}"
    LOGO_PATH=""
fi

# Contador para acompanhar progresso
counter=0
total=$(ls -1 *.mp3 2>/dev/null | wc -l)

echo -e "${GREEN}Encontrados $total arquivos .mp3${NC}"
echo ""

# Processar cada arquivo .mp3
for audio_file in *.mp3; do
    # Verificar se existem arquivos .mp3
    if [ ! -f "$audio_file" ]; then
        echo -e "${RED}Nenhum arquivo .mp3 encontrado!${NC}"
        exit 1
    fi
    
    counter=$((counter + 1))
    
    # Gerar nome do arquivo de saída
    base_name=$(basename "$audio_file" .mp3)
    output_file="$OUTPUT_DIR/${base_name}.mp4"
    
    echo -e "${BLUE}[$counter/$total] Processando: $audio_file${NC}"
    
    # Comando ffmpeg base
    if [ -n "$LOGO_PATH" ]; then
        # Com logo como fundo
        ffmpeg -loop 1 -i "$LOGO_PATH" -i "$audio_file" \
            -c:v libx264 -tune stillimage -c:a aac -b:a 192k \
            -pix_fmt yuv420p -shortest \
            -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black" \
            "$output_file" \
            -y -loglevel error
    else
        # Com fundo preto
        ffmpeg -f lavfi -i color=black:size=1920x1080:rate=30 -i "$audio_file" \
            -c:v libx264 -c:a aac -b:a 192k \
            -pix_fmt yuv420p -shortest \
            "$output_file" \
            -y -loglevel error
    fi
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Sucesso: $output_file${NC}"
        
        # Mostrar informações do arquivo gerado
        duration=$(ffprobe -v quiet -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$output_file" 2>/dev/null)
        if [ -n "$duration" ]; then
            duration_formatted=$(printf "%.2f" "$duration")
            echo -e "${YELLOW}  Duração: ${duration_formatted}s${NC}"
        fi
        
        size=$(du -h "$output_file" | cut -f1)
        echo -e "${YELLOW}  Tamanho: $size${NC}"
        
    else
        echo -e "${RED}✗ Erro ao processar: $audio_file${NC}"
    fi
    
    echo ""
done

echo -e "${GREEN}=== Processamento Concluído ===${NC}"
echo -e "${BLUE}Vídeos gerados em: $OUTPUT_DIR${NC}"
echo ""
echo -e "${YELLOW}Arquivos gerados:${NC}"
ls -la "$OUTPUT_DIR"/*.mp4 2>/dev/null || echo -e "${RED}Nenhum vídeo foi gerado${NC}"

echo ""
echo -e "${BLUE}=== Próximos Passos ===${NC}"
echo -e "${YELLOW}1. Faça upload dos vídeos para o YouTube${NC}"
echo -e "${YELLOW}2. Copie os URLs dos vídeos do YouTube${NC}"
echo -e "${YELLOW}3. Atualize o arquivo figmin_urls.json com os novos URLs${NC}"
echo -e "${YELLOW}4. Teste no Figmin XR${NC}" 