#!/usr/bin/env python3
# update_all_figmin_urls.py - Atualiza URLs completas para todos os arquivos multimídia

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

def update_all_figmin_urls():
    """Atualiza todas as URLs para todos os arquivos multimídia"""
    
    print("🚀 FIRJAN XR → ATUALIZANDO URLS COMPLETAS DO FIGMIN")
    print("=" * 70)
    
    # Escanear arquivos
    files_found = scan_multimedia_files()
    
    # Estrutura de dados completa
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
        file_size = 0
        if os.path.exists(file_info['path']):
            file_size = round(os.path.getsize(file_info['path']) / (1024*1024), 1)
        
        urls_data["models_3d"].append({
            "name": file_info['name'],
            "folder": file_info['folder'],
            "url": generate_github_url(file_info['relative_path']),
            "figmin_name": generate_figmin_name(file_info),
            "file_path": file_info['relative_path'],
            "size_mb": file_size
        })
        print(f"   ✓ {file_info['name']} → {file_info['folder']} ({file_size}MB)")
    
    # Processar ÁUDIOS
    print(f"\n🎵 PROCESSANDO ÁUDIOS ({len(files_found['audio'])} arquivos):")
    for file_info in files_found['audio']:
        file_size = 0
        if os.path.exists(file_info['path']):
            file_size = round(os.path.getsize(file_info['path']) / (1024*1024), 1)
        
        urls_data["audio_files"].append({
            "name": file_info['name'],
            "folder": file_info['folder'],
            "url": generate_github_url(file_info['relative_path']),
            "figmin_name": generate_figmin_name(file_info),
            "file_path": file_info['relative_path'],
            "size_mb": file_size
        })
        print(f"   ✓ {file_info['name']} → {file_info['folder']} ({file_size}MB)")
    
    # Processar VÍDEOS
    print(f"\n🎬 PROCESSANDO VÍDEOS ({len(files_found['video'])} arquivos):")
    for file_info in files_found['video']:
        file_size = 0
        if os.path.exists(file_info['path']):
            file_size = round(os.path.getsize(file_info['path']) / (1024*1024), 1)
        
        urls_data["video_files"].append({
            "name": file_info['name'],
            "folder": file_info['folder'],
            "url": generate_github_url(file_info['relative_path']),
            "figmin_name": generate_figmin_name(file_info),
            "file_path": file_info['relative_path'],
            "size_mb": file_size
        })
        print(f"   ✓ {file_info['name']} → {file_info['folder']} ({file_size}MB)")
    
    # Atualizar summary
    urls_data["summary"]["total_files"] = len(files_found['images']) + len(files_found['models']) + len(files_found['audio']) + len(files_found['video'])
    urls_data["summary"]["total_images"] = len(files_found['images'])
    urls_data["summary"]["total_models"] = len(files_found['models'])
    urls_data["summary"]["total_audio"] = len(files_found['audio'])
    urls_data["summary"]["total_video"] = len(files_found['video'])
    
    # Salvar JSON atualizado
    with open("figmin_urls_complete.json", "w", encoding="utf-8") as f:
        json.dump(urls_data, f, indent=2, ensure_ascii=False)
    
    # Atualizar arquivo original também
    with open("figmin_urls.json", "w", encoding="utf-8") as f:
        json.dump(urls_data, f, indent=2, ensure_ascii=False)
    
    # Gerar arquivo de texto organizado
    generate_organized_text_file(urls_data)
    
    print("\n" + "=" * 70)
    print("📊 RESUMO FINAL:")
    print("=" * 70)
    print(f"📷 Imagens: {urls_data['summary']['total_images']}")
    print(f"🎲 Modelos 3D: {urls_data['summary']['total_models']}")
    print(f"🎵 Áudios: {urls_data['summary']['total_audio']}")
    print(f"🎬 Vídeos: {urls_data['summary']['total_video']}")
    print(f"🌐 Esferas 360°: {len(urls_data['spheres_360'])}")
    print(f"📁 Total: {urls_data['summary']['total_files']} arquivos")
    
    print(f"\n✅ ARQUIVOS ATUALIZADOS:")
    print(f"   📄 figmin_urls.json (atualizado)")
    print(f"   📄 figmin_urls_complete.json (novo)")
    print(f"   📝 figmin_urls_organized.txt (atualizado)")
    
    return urls_data

def generate_organized_text_file(urls_data):
    """Gera arquivo de texto organizado para copy-paste"""
    
    with open("figmin_urls_organized.txt", "w", encoding="utf-8") as f:
        f.write("FIRJAN XR - URLs COMPLETAS PARA FIGMIN\n")
        f.write("=" * 60 + "\n")
        f.write(f"Gerado em: 4 de Julho de 2025\n")
        f.write(f"Total de arquivos: {urls_data['summary']['total_files']}\n\n")
        
        # MODELOS 3D (mais importantes primeiro)
        f.write("🎲 MODELOS 3D GLB\n")
        f.write("-" * 30 + "\n")
        for i, model in enumerate(urls_data["models_3d"], 1):
            f.write(f"{i:02d}. NOME: {model['figmin_name']}\n")
            f.write(f"    URL:  {model['url']}\n")
            f.write(f"    TAMANHO: {model['size_mb']} MB\n\n")
        
        # ESFERAS 360° (experiência imersiva)
        f.write("🌐 ESFERAS 360°\n")
        f.write("-" * 30 + "\n")
        for i, sphere in enumerate(urls_data["spheres_360"], 1):
            f.write(f"{i:02d}. NOME: {sphere['figmin_name']}\n")
            f.write(f"    URL:  {sphere['url']}\n\n")
        
        # IMAGENS (boards e outros)
        f.write("📷 IMAGENS\n")
        f.write("-" * 30 + "\n")
        for i, img in enumerate(urls_data["images"], 1):
            f.write(f"{i:02d}. NOME: {img['figmin_name']}\n")
            f.write(f"    URL:  {img['url']}\n")
            f.write(f"    PASTA: {img['folder']}\n\n")
        
        # ÁUDIOS
        f.write("🎵 ÁUDIOS\n")
        f.write("-" * 30 + "\n")
        for i, audio in enumerate(urls_data["audio_files"], 1):
            f.write(f"{i:02d}. NOME: {audio['figmin_name']}\n")
            f.write(f"    URL:  {audio['url']}\n")
            f.write(f"    TAMANHO: {audio['size_mb']} MB\n\n")
        
        # VÍDEOS
        f.write("🎬 VÍDEOS\n")
        f.write("-" * 30 + "\n")
        for i, video in enumerate(urls_data["video_files"], 1):
            f.write(f"{i:02d}. NOME: {video['figmin_name']}\n")
            f.write(f"    URL:  {video['url']}\n")
            f.write(f"    TAMANHO: {video['size_mb']} MB\n\n")
    
    # Atualizar arquivo simple também
    with open("figmin_urls_simple.txt", "w", encoding="utf-8") as f:
        f.write("FIRJAN XR - URLs para Figmin XR (Copy & Paste)\n")
        f.write("=" * 50 + "\n\n")
        
        # Todos os arquivos em ordem de importância
        all_items = []
        
        # Modelos 3D primeiro
        for model in urls_data["models_3d"]:
            all_items.append(f"NOME: {model['figmin_name']}\nURL:  {model['url']}\n")
        
        # Esferas 360°
        for sphere in urls_data["spheres_360"]:
            all_items.append(f"NOME: {sphere['figmin_name']}\nURL:  {sphere['url']}\n")
        
        # Imagens principais
        for img in urls_data["images"]:
            all_items.append(f"NOME: {img['figmin_name']}\nURL:  {img['url']}\n")
        
        # Áudios
        for audio in urls_data["audio_files"]:
            all_items.append(f"NOME: {audio['figmin_name']}\nURL:  {audio['url']}\n")
        
        # Vídeos
        for video in urls_data["video_files"]:
            all_items.append(f"NOME: {video['figmin_name']}\nURL:  {video['url']}\n")
        
        f.write("\n".join(all_items))

if __name__ == "__main__":
    print("🎯 Iniciando atualização COMPLETA das URLs do Figmin...")
    urls = update_all_figmin_urls()
    print(f"\n🎉 ATUALIZAÇÃO CONCLUÍDA COM SUCESSO!")
    print(f"🔗 Todas as URLs foram atualizadas para {urls['summary']['total_files']} arquivos multimídia!") 