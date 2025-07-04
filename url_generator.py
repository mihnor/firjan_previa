#!/usr/bin/env python3
# url_generator.py - Gera todas as URLs automaticamente para Figmin XR

import os
import json
from pathlib import Path

GITHUB_BASE = "https://raw.githubusercontent.com/mihnor/firjan_previa/main"

def generate_all_urls():
    """Gera todas as URLs para Figmin XR"""
    
    urls_data = {
        "images": [],
        "glb_models": [],
        "youtube_videos": [],
        "figmin_imports": []
    }
    
    # Board files mapping (baseado na estrutura atual)
    board_files = {
        "BOARD_01_PERGUNTA": [
            "BOARD_01_pergunta_de_onde_vem.png",
            "BOARD_01_pergunta_interrogacoes.png"
        ],
        "BOARD_02_GUTENBERG": [
            "BOARD_02_gutenberg_extra_001.png",
            "BOARD_02_gutenberg_historical_press.png",
            "BOARD_02_gutenberg_invencao_contexto.png",
            "BOARD_02_gutenberg_lettering.png",
            "BOARD_02_gutenberg_printing_press.png"
        ],
        "BOARD_03_TIPOGRAFIA": [
            "BOARD_03_tipografia_curso.png",
            "BOARD_03_tipografia_extra_001.png",
            "BOARD_03_tipografia_industria_grafica.png"
        ],
        "BOARD_04_ESCRITORES": [
            "BOARD_04_escritores_dicionario_industria.png",
            "BOARD_04_escritores_homem_maquina_escrever.png",
            "BOARD_04_escritores_mulher_computador.png",
            "BOARD_04_escritores_pexels_scene.png",
            "BOARD_04_escritores_profile_scene.png"
        ],
        "BOARD_05_PARQUES": [
            "BOARD_05_parques_csm_scene.png",
            "BOARD_05_parques_desafios_oportunidades.png",
            "BOARD_05_parques_print_publishing.png"
        ],
        "BOARD_06_CENOGRAFIA": [
            "BOARD_06_cenografia_visual_electric.png"
        ],
        "BOARD_09_EXPERIENCIA": [
            "BOARD_09_experiencia_diy_scene.png"
        ],
        "BOARD_10_VISUAL_ELECTRIC": [
            "BOARD_10_visual_electric_main.png"
        ],
        "BOARD_11_VISUAL_ELECTRIC_ALT": [
            "BOARD_11_visual_electric_alt.png"
        ],
        "BOARD_12_CASA_FIRJAN": [
            "BOARD_12_casa_firjan_lettering.png"
        ]
    }
    
    print("🚀 FIRJAN XR → URL Generator")
    print("=" * 60)
    
    # Generate URLs for all boards
    for board_name, files in board_files.items():
        print(f"\n🎯 {board_name}:")
        
        for file in files:
            url = f"{GITHUB_BASE}/BOARDS/{board_name}/{file}"
            figmin_name = f"{board_name}_{Path(file).stem}"
            
            urls_data["images"].append({
                "board": board_name,
                "file": file,
                "url": url,
                "figmin_name": figmin_name
            })
            print(f"   📷 {file}")
            print(f"       URL: {url}")
    
    # Audio/YouTube URLs
    urls_data["youtube_videos"] = [
        {
            "name": "Guta_Voiceover",
            "description": "Narração principal da Guta",
            "youtube_url": "https://youtu.be/YOUR_VIDEO_ID_HERE",
            "figmin_name": "FIRJAN_Guta_Audio",
            "audio_file": "FIRJAN_tour_virtual_guta_voiceover.mp3"
        }
    ]
    
    # Generate copy-paste list for Figmin XR
    print("\n" + "=" * 60)
    print("📋 COPY & PASTE PARA FIGMIN XR:")
    print("=" * 60)
    
    for i, img in enumerate(urls_data["images"], 1):
        print(f"\n{i:02d}. NOME: {img['figmin_name']}")
        print(f"    URL:  {img['url']}")
    
    # Save to files
    with open("figmin_urls.json", "w", encoding="utf-8") as f:
        json.dump(urls_data, f, indent=2, ensure_ascii=False)
    
    # Create simple text file for copy-paste
    with open("figmin_urls_simple.txt", "w", encoding="utf-8") as f:
        f.write("FIRJAN XR - URLs para Figmin XR\n")
        f.write("=" * 50 + "\n\n")
        
        for img in urls_data["images"]:
            f.write(f"NOME: {img['figmin_name']}\n")
            f.write(f"URL:  {img['url']}\n\n")
    
    print(f"\n✅ Arquivos gerados:")
    print(f"   📄 figmin_urls.json (dados completos)")
    print(f"   📝 figmin_urls_simple.txt (copy/paste)")
    
    return urls_data

def generate_figmin_checklist():
    """Gera checklist organizado para Figmin XR"""
    
    checklist = """# 📋 CHECKLIST FIGMIN XR - FIRJAN

## ✅ ORDEM DE IMPORT (20 min total):

### 1. SETUP INICIAL (2 min)
- [ ] Abrir Figmin XR
- [ ] Create New → "FIRJAN_Teaser"
- [ ] Environment: Studio Space
- [ ] Lighting: Soft Natural
- [ ] Scale: Room Scale (3x3m)

### 2. IMPORT BOARDS (15 min)
Use o arquivo: figmin_urls_simple.txt

#### Sequência Narrativa:
- [ ] 01. BOARD_01_PERGUNTA_BOARD_01_pergunta_de_onde_vem
- [ ] 02. BOARD_01_PERGUNTA_BOARD_01_pergunta_interrogacoes
- [ ] 03. BOARD_02_GUTENBERG_BOARD_02_gutenberg_lettering
- [ ] 04. BOARD_02_GUTENBERG_BOARD_02_gutenberg_printing_press
- [ ] 05. BOARD_03_TIPOGRAFIA_BOARD_03_tipografia_industria_grafica
- [ ] 06. BOARD_04_ESCRITORES_BOARD_04_escritores_mulher_computador
- [ ] 07. BOARD_05_PARQUES_BOARD_05_parques_print_publishing
- [ ] 08. BOARD_06_CENOGRAFIA_BOARD_06_cenografia_visual_electric
- [ ] 09. BOARD_09_EXPERIENCIA_BOARD_09_experiencia_diy_scene
- [ ] 10. BOARD_10_VISUAL_ELECTRIC_BOARD_10_visual_electric_main
- [ ] 11. BOARD_11_VISUAL_ELECTRIC_ALT_BOARD_11_visual_electric_alt
- [ ] 12. BOARD_12_CASA_FIRJAN_BOARD_12_casa_firjan_lettering

### 3. ÁUDIO YOUTUBE (3 min)
- [ ] Upload vídeo: FIRJAN_Guta_Voiceover_YT.mp4
- [ ] Configurar como: Unlisted
- [ ] Copiar URL: https://youtu.be/YOUR_ID
- [ ] Import no Figmin XR
- [ ] NOME: "Guta_Audio"
- [ ] Position: (0, 0, 0)
- [ ] Scale: (0.01, 0.01, 0.01)

### 4. LAYOUT ESPACIAL
- [ ] Organizar boards em sequência
- [ ] Testar navegação
- [ ] Ajustar posições
- [ ] Teste final

## 🚀 DICAS RÁPIDAS:
- Ctrl+C / Ctrl+V para URLs
- Import ordem sequencial
- Nomear consistente
- Testar cada etapa

## ⚡ ATALHOS FIGMIN XR:
- Spacebar: Play/Pause
- R: Reset view
- G: Grab/Move objects
- S: Scale objects
"""
    
    with open("figmin_checklist.md", "w", encoding="utf-8") as f:
        f.write(checklist)
    
    print(f"📋 Checklist criado: figmin_checklist.md")

if __name__ == "__main__":
    print("🎯 Iniciando geração automática...")
    
    # Generate URLs
    urls = generate_all_urls()
    
    # Generate checklist
    generate_figmin_checklist()
    
    print(f"\n🎉 PROCESSO CONCLUÍDO!")
    print(f"📊 Total de imagens: {len(urls['images'])}")
    print(f"🎵 Total de vídeos: {len(urls['youtube_videos'])}")
    print(f"\n📁 Arquivos gerados:")
    print(f"   - figmin_urls.json")
    print(f"   - figmin_urls_simple.txt")
    print(f"   - figmin_checklist.md")
    print(f"\n🚀 Próximo passo: Execute ./convert_audio.sh") 