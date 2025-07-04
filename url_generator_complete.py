#!/usr/bin/env python3
# url_generator_complete.py - Gera URLs completas para todos os arquivos multimídia

import os
import json
from pathlib import Path
from urllib.parse import quote

# Configuração do GitHub
GITHUB_BASE = "https://raw.githubusercontent.com/mihnor/firjan_previa/main"
GITHUB_REPO_PATH = "FIRJAN_XR_ASSETS"

def clean_name_for_figmin(name):
    """Limpa nome para uso no Figmin"""
    # Remove caracteres especiais e espaços
    name = name.replace(" ", "_")
    name = name.replace("-", "_")
    name = name.replace("(", "")
    name = name.replace(")", "")
    name = name.replace("'", "")
    name = name.replace('"', "")
    name = name.replace(",", "")
    name = name.replace("&", "and")
    name = name.replace("á", "a")
    name = name.replace("ã", "a")
    name = name.replace("ç", "c")
    name = name.replace("é", "e")
    name = name.replace("ê", "e")
    name = name.replace("í", "i")
    name = name.replace("ó", "o")
    name = name.replace("ô", "o")
    name = name.replace("õ", "o")
    name = name.replace("ú", "u")
    name = name.replace("ü", "u")
    return name

def scan_multimedia_files():
    """Escaneia todos os arquivos multimídia na pasta"""
    
    multimedia_extensions = {
        'images': ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp', '.avif'],
        'models': ['.glb', '.gltf', '.obj', '.fbx'],
        'audio': ['.mp3', '.wav', '.ogg', '.m4a', '.flac'],
        'video': ['.mp4', '.mov', '.avi', '.webm', '.mkv', '.m4v']
    }
    
    files_found = {
        'images': [],
        'models': [],
        'audio': [],
        'video': []
    }
    
    print("🔍 ESCANEANDO ARQUIVOS MULTIMÍDIA...")
    
    # Escanear todas as pastas
    for root, dirs, files in os.walk('.'):
        # Pular pastas do git e cache
        if '.git' in root or '__pycache__' in root:
            continue
        
        for file in files:
            if file.startswith('.'):
                continue
            
            file_path = os.path.join(root, file)
            file_ext = Path(file).suffix.lower()
            
            # Classificar por tipo
            for media_type, extensions in multimedia_extensions.items():
                if file_ext in extensions:
                    files_found[media_type].append({
                        'path': file_path,
                        'name': file,
                        'folder': os.path.basename(root),
                        'relative_path': file_path.replace('./', ''),
                        'extension': file_ext
                    })
                    break
    
    return files_found

def generate_github_url(file_path):
    """Gera URL do GitHub para um arquivo"""
    # Limpar o caminho
    clean_path = file_path.replace('./', '')
    
    # Codificar caracteres especiais na URL
    encoded_path = quote(clean_path, safe='/')
    
    return f"{GITHUB_BASE}/{GITHUB_REPO_PATH}/{encoded_path}"

def generate_figmin_name(file_info):
    """Gera nome apropriado para Figmin"""
    folder = file_info['folder']
    name = Path(file_info['name']).stem
    
    # Casos especiais
    if folder == 'GLB_EXPORTS':
        return f"MODEL_{clean_name_for_figmin(name)}"
    elif folder == 'VOICEOVER':
        return f"AUDIO_{clean_name_for_figmin(name)}"
    elif folder == 'videos':
        return f"VIDEO_{clean_name_for_figmin(name)}"
    elif folder == '360 images':
        return f"SPHERE360_{clean_name_for_figmin(name)}"
    elif folder.startswith('BOARD_'):
        return f"{folder}_{clean_name_for_figmin(name)}"
    else:
        return f"{clean_name_for_figmin(folder)}_{clean_name_for_figmin(name)}"

def generate_complete_urls():
    """Gera todas as URLs para todos os arquivos multimídia"""
    
    print("🚀 FIRJAN XR → GERADOR COMPLETO DE URLs")
    print("=" * 70)
    
    # Escanear arquivos
    files_found = scan_multimedia_files()
    
    # Estrutura de dados
    urls_data = {
        "images": [],
        "models_3d": [],
        "audio_files": [],
        "video_files": [],
        "spheres_360": [],
        "youtube_videos": [],
        "figmin_imports": [],
        "summary": {
            "total_files": 0,
            "total_images": 0,
            "total_models": 0,
            "total_audio": 0,
            "total_video": 0,
            "generation_date": "2025-07-04"
        }
    }
    
    # Processar IMAGENS
    print(f"\n📷 PROCESSANDO IMAGENS ({len(files_found['images'])} arquivos):")
    for file_info in files_found['images']:
        # Separar imagens 360°
        if '360 images' in file_info['path']:
            urls_data["spheres_360"].append({
                "name": file_info['name'],
                "folder": file_info['folder'],
                "url": generate_github_url(file_info['relative_path']),
                "figmin_name": generate_figmin_name(file_info),
                "file_path": file_info['relative_path']
            })
        else:
            urls_data["images"].append({
                "name": file_info['name'],
                "folder": file_info['folder'],
                "url": generate_github_url(file_info['relative_path']),
                "figmin_name": generate_figmin_name(file_info),
                "file_path": file_info['relative_path']
            })
        
        print(f"   ✓ {file_info['name']} → {file_info['folder']}")
    
    # Processar MODELOS 3D
    print(f"\n🎲 PROCESSANDO MODELOS 3D ({len(files_found['models'])} arquivos):")
    for file_info in files_found['models']:
        urls_data["models_3d"].append({
            "name": file_info['name'],
            "folder": file_info['folder'],
            "url": generate_github_url(file_info['relative_path']),
            "figmin_name": generate_figmin_name(file_info),
            "file_path": file_info['relative_path'],
            "size_mb": round(os.path.getsize(file_info['path']) / (1024*1024), 1)
        })
        print(f"   ✓ {file_info['name']} → {file_info['folder']}")
    
    # Processar ÁUDIOS
    print(f"\n🎵 PROCESSANDO ÁUDIOS ({len(files_found['audio'])} arquivos):")
    for file_info in files_found['audio']:
        urls_data["audio_files"].append({
            "name": file_info['name'],
            "folder": file_info['folder'],
            "url": generate_github_url(file_info['relative_path']),
            "figmin_name": generate_figmin_name(file_info),
            "file_path": file_info['relative_path'],
            "size_mb": round(os.path.getsize(file_info['path']) / (1024*1024), 1)
        })
        print(f"   ✓ {file_info['name']} → {file_info['folder']}")
    
    # Processar VÍDEOS
    print(f"\n🎬 PROCESSANDO VÍDEOS ({len(files_found['video'])} arquivos):")
    for file_info in files_found['video']:
        urls_data["video_files"].append({
            "name": file_info['name'],
            "folder": file_info['folder'],
            "url": generate_github_url(file_info['relative_path']),
            "figmin_name": generate_figmin_name(file_info),
            "file_path": file_info['relative_path'],
            "size_mb": round(os.path.getsize(file_info['path']) / (1024*1024), 1)
        })
        print(f"   ✓ {file_info['name']} → {file_info['folder']}")
    
    # Atualizar summary
    urls_data["summary"]["total_files"] = len(files_found['images']) + len(files_found['models']) + len(files_found['audio']) + len(files_found['video'])
    urls_data["summary"]["total_images"] = len(files_found['images'])
    urls_data["summary"]["total_models"] = len(files_found['models'])
    urls_data["summary"]["total_audio"] = len(files_found['audio'])
    urls_data["summary"]["total_video"] = len(files_found['video'])
    
    # Salvar arquivos JSON
    with open("figmin_urls_complete.json", "w", encoding="utf-8") as f:
        json.dump(urls_data, f, indent=2, ensure_ascii=False)
    
    # Gerar arquivo de texto organizado
    generate_figmin_text_file(urls_data)
    
    # Gerar checklist atualizado
    generate_figmin_checklist_complete(urls_data)
    
    print("\n" + "=" * 70)
    print("📊 RESUMO FINAL:")
    print("=" * 70)
    print(f"📷 Imagens: {urls_data['summary']['total_images']}")
    print(f"🎲 Modelos 3D: {urls_data['summary']['total_models']}")
    print(f"🎵 Áudios: {urls_data['summary']['total_audio']}")
    print(f"🎬 Vídeos: {urls_data['summary']['total_video']}")
    print(f"🌐 Esferas 360°: {len(urls_data['spheres_360'])}")
    print(f"📁 Total: {urls_data['summary']['total_files']} arquivos")
    
    print(f"\n✅ ARQUIVOS GERADOS:")
    print(f"   📄 figmin_urls_complete.json")
    print(f"   📝 figmin_urls_organized.txt")
    print(f"   📋 figmin_checklist_complete.md")
    
    return urls_data

def generate_figmin_text_file(urls_data):
    """Gera arquivo de texto organizado para copy-paste"""
    
    with open("figmin_urls_organized.txt", "w", encoding="utf-8") as f:
        f.write("FIRJAN XR - URLs COMPLETAS PARA FIGMIN\n")
        f.write("=" * 60 + "\n\n")
        
        # IMAGENS
        f.write("📷 IMAGENS\n")
        f.write("-" * 30 + "\n")
        for i, img in enumerate(urls_data["images"], 1):
            f.write(f"{i:02d}. NOME: {img['figmin_name']}\n")
            f.write(f"    URL:  {img['url']}\n")
            f.write(f"    PASTA: {img['folder']}\n\n")
        
        # MODELOS 3D
        f.write("\n🎲 MODELOS 3D GLB\n")
        f.write("-" * 30 + "\n")
        for i, model in enumerate(urls_data["models_3d"], 1):
            f.write(f"{i:02d}. NOME: {model['figmin_name']}\n")
            f.write(f"    URL:  {model['url']}\n")
            f.write(f"    TAMANHO: {model['size_mb']} MB\n\n")
        
        # ESFERAS 360°
        f.write("\n🌐 ESFERAS 360°\n")
        f.write("-" * 30 + "\n")
        for i, sphere in enumerate(urls_data["spheres_360"], 1):
            f.write(f"{i:02d}. NOME: {sphere['figmin_name']}\n")
            f.write(f"    URL:  {sphere['url']}\n\n")
        
        # ÁUDIOS
        f.write("\n🎵 ÁUDIOS\n")
        f.write("-" * 30 + "\n")
        for i, audio in enumerate(urls_data["audio_files"], 1):
            f.write(f"{i:02d}. NOME: {audio['figmin_name']}\n")
            f.write(f"    URL:  {audio['url']}\n")
            f.write(f"    TAMANHO: {audio['size_mb']} MB\n\n")
        
        # VÍDEOS
        f.write("\n🎬 VÍDEOS\n")
        f.write("-" * 30 + "\n")
        for i, video in enumerate(urls_data["video_files"], 1):
            f.write(f"{i:02d}. NOME: {video['figmin_name']}\n")
            f.write(f"    URL:  {video['url']}\n")
            f.write(f"    TAMANHO: {video['size_mb']} MB\n\n")

def generate_figmin_checklist_complete(urls_data):
    """Gera checklist completo para Figmin XR"""
    
    checklist = f"""# 📋 FIGMIN XR - CHECKLIST COMPLETO ATUALIZADO

## 📊 RESUMO DOS ARQUIVOS:
- 📷 **Imagens**: {len(urls_data['images'])} arquivos
- 🎲 **Modelos 3D**: {len(urls_data['models_3d'])} arquivos GLB
- 🌐 **Esferas 360°**: {len(urls_data['spheres_360'])} arquivos
- 🎵 **Áudios**: {len(urls_data['audio_files'])} arquivos MP3
- 🎬 **Vídeos**: {len(urls_data['video_files'])} arquivos MP4

## ✅ PROCESSO DE IMPORTAÇÃO:

### 1. SETUP INICIAL (3 min)
- [ ] Abrir Figmin XR
- [ ] Create New → "FIRJAN_XR_Complete"
- [ ] Environment: Studio Space ou Custom
- [ ] Lighting: Soft Natural
- [ ] Scale: Room Scale (5x5m para comportar todos os elementos)

### 2. IMPORTAR MODELOS 3D PRINCIPAIS (10 min)
Use o arquivo: figmin_urls_organized.txt - Seção MODELOS 3D

**Modelos Essenciais:**
- [ ] MODEL_FIRJAN_XR_Collections_1_4 (10 MB)
- [ ] MODEL_FIRJAN_XR_Collections_5_8 (17 MB)
- [ ] MODEL_prensa_de_guttenberg (5.8 MB)

**Esferas 360° (Experiência Imersiva):**
- [ ] MODEL_FIRJAN_XR_All_Spheres_360 (8 MB)
- [ ] Ou importar individualmente: Sphere_360_00 a 03

### 3. IMPORTAR IMAGENS PRINCIPAIS (15 min)
**Boards Principais (sequência narrativa):**
- [ ] BOARD_01_PERGUNTA_BOARD_01_pergunta_de_onde_vem
- [ ] BOARD_02_GUTENBERG_BOARD_02_gutenberg_lettering
- [ ] BOARD_03_TIPOGRAFIA_BOARD_03_tipografia_industria_grafica
- [ ] BOARD_04_ESCRITORES_BOARD_04_escritores_mulher_computador
- [ ] BOARD_05_PARQUES_BOARD_05_parques_print_publishing
- [ ] BOARD_06_CENOGRAFIA_BOARD_06_cenografia_visual_electric
- [ ] BOARD_12_CASA_FIRJAN_BOARD_12_casa_firjan_lettering

**Letterings Numerados:**
- [ ] LETTERINGS_NUMERADOS_01_let_de_onde_vem
- [ ] LETTERINGS_NUMERADOS_02_let_gutenberg
- [ ] LETTERINGS_NUMERADOS_12_let_casa_firjan

### 4. IMPORTAR ÁUDIOS (5 min)
- [ ] AUDIO_FIRJAN_tour_virtual_guta_voiceover (3.8 MB)
- [ ] AUDIO_ElevenLabs_2025_07_04T10_50_20__s50_v3 (2.1 MB)
- [ ] AUDIO_ElevenLabs_2025_07_04T10_53_15_James (2.5 MB)

### 5. IMPORTAR VÍDEOS (5 min)
- [ ] VIDEO_FIRJAN_Guta_Voiceover_YT (2.7 MB)
- [ ] VIDEO_Video_Ready_Printing_Press (2.6 MB)
- [ ] VIDEO_Vídeo_Guttenberg_e_a_Bíblia (1.3 MB)

### 6. LAYOUT ESPACIAL (10 min)
- [ ] Posicionar modelos 3D principais
- [ ] Organizar boards em sequência narrativa
- [ ] Configurar esferas 360° para experiência imersiva
- [ ] Posicionar áudios e vídeos
- [ ] Testar navegação e interações

### 7. OTIMIZAÇÕES (5 min)
- [ ] Ajustar LOD (Level of Detail) para modelos grandes
- [ ] Configurar triggers para áudios/vídeos
- [ ] Testar performance em diferentes dispositivos
- [ ] Configurar pontos de teleporte/navegação

## 🎯 DICAS IMPORTANTES:

### Para Modelos 3D:
- Importar Collections 1-4 e 5-8 primeiro (elementos principais)
- Usar esferas 360° para experiência imersiva
- Modelos individuais para customização específica

### Para Imagens:
- Priorizar boards principais da narrativa
- Usar letterings numerados como complemento
- Configurar como billboards para melhor visualização

### Para Áudios:
- Usar Guta_voiceover como narração principal
- ElevenLabs para diferentes vozes/idiomas
- Configurar como audio zones ou triggers

### Para Vídeos:
- Usar como YouTube embeds quando possível
- Configurar autoplay off para controle do usuário
- Posicionar em telas virtuais ou billboards

## ⚡ ATALHOS FIGMIN XR:
- **Spacebar**: Play/Pause
- **R**: Reset view
- **G**: Grab/Move objects
- **S**: Scale objects
- **Ctrl+Z**: Undo
- **Ctrl+C/V**: Copy/Paste URLs

## 🚀 RESULTADO ESPERADO:
Experiência XR completa com:
- Modelos 3D interativos
- Narrativa visual com boards
- Áudio imersivo
- Vídeos contextuais
- Esferas 360° para imersão total

---
**Atualizado em**: 4 de Julho de 2025
**Total de arquivos**: {urls_data['summary']['total_files']} arquivos multimídia
"""
    
    with open("figmin_checklist_complete.md", "w", encoding="utf-8") as f:
        f.write(checklist)

if __name__ == "__main__":
    print("🎯 Iniciando geração COMPLETA de URLs...")
    urls = generate_complete_urls()
    print(f"\n🎉 PROCESSO CONCLUÍDO COM SUCESSO!") 