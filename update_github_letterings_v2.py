#!/usr/bin/env python3
"""
FIRJAN XR - GitHub Update & Video Generation Script v2
====================================================
VERSÃO CORRIGIDA com mapeamento real dos arquivos
"""

import os
import shutil
import subprocess
import json
from pathlib import Path
from datetime import datetime

class FirjanGitHubUpdater:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.letterings_source = self.project_root / "FIRJAN_XR_ASSETS" / "LETTERINGS NUMERADOS"
        self.audio_source = self.project_root / "FIRJAN_XR_ASSETS" / "AUDIO" / "VOICEOVER"
        self.boards_target = self.project_root / "FIRJAN_XR_ASSETS" / "BOARDS"
        
        # Mapeamento CORRETO baseado nos arquivos reais encontrados
        self.lettering_mapping = {
            "01_let_de_onde-_vem.png": "BOARD_01_PERGUNTA",
            "01_let_interrogacao.png": "BOARD_01_PERGUNTA",
            "01_let_interrogacoes.png": "BOARD_01_PERGUNTA", 
            "02_let_gutenberg.png": "BOARD_02_GUTENBERG",
            "02_gutenberg_comecou.png": "BOARD_02_GUTENBERG",
            "03_evolucao_da_producao_grafica.png": "BOARD_03_TIPOGRAFIA",
            "04_o_escritor.png": "BOARD_04_ESCRITORES",
            "05_parques_graficos.png": "BOARD_05_PARQUES",
            "06_cenografia_criativa.png": "BOARD_06_CENOGRAFIA",
            "06_experiencia_imersiva.png": "BOARD_06_CENOGRAFIA",
            "09_linha_do_tempo.png": "BOARD_09_EXPERIENCIA",
            "12_let_casa_firjan.png": "BOARD_12_CASA_FIRJAN"
        }
    
    def organize_letterings_for_github(self):
        """Organiza letterings nas pastas corretas dos boards"""
        print("🔄 Organizando letterings para GitHub...")
        
        organized_files = []
        
        for lettering_file, board_folder in self.lettering_mapping.items():
            source_path = self.letterings_source / lettering_file
            target_dir = self.boards_target / board_folder
            target_path = target_dir / f"LETTERING_{lettering_file}"
            
            if source_path.exists():
                # Criar diretório se não existir
                target_dir.mkdir(parents=True, exist_ok=True)
                
                # Copiar arquivo
                shutil.copy2(source_path, target_path)
                organized_files.append({
                    "original": str(source_path),
                    "target": str(target_path),
                    "board": board_folder,
                    "size_mb": round(source_path.stat().st_size / (1024*1024), 2)
                })
                print(f"  ✅ {lettering_file} → {board_folder} ({round(source_path.stat().st_size / (1024*1024), 1)}MB)")
            else:
                print(f"  ❌ Arquivo não encontrado: {lettering_file}")
        
        return organized_files
    
    def prepare_video_structure(self):
        """Prepara estrutura para geração de vídeos"""
        print("\n🎬 Preparando estrutura para vídeos...")
        
        video_configs = []
        
        for board_folder in set(self.lettering_mapping.values()):
            board_path = self.boards_target / board_folder
            video_config = {
                "board": board_folder,
                "letterings": [],
                "audio": None,
                "output": f"{board_folder}_VIDEO.mp4"
            }
            
            # Buscar letterings do board
            if board_path.exists():
                letterings = list(board_path.glob("LETTERING_*.png"))
                video_config["letterings"] = [str(l) for l in sorted(letterings)]
                print(f"  📁 {board_folder}: {len(letterings)} letterings")
            
            # Buscar áudio correspondente
            main_audio = self.project_root / "Casa Firjan - tour virtual locução - Tratamento.wav"
            if main_audio.exists():
                video_config["audio"] = str(main_audio)
                print(f"    🎵 Áudio: {main_audio.name}")
            
            video_configs.append(video_config)
        
        return video_configs
    
    def generate_ffmpeg_commands(self, video_configs):
        """Gera comandos FFmpeg para criar vídeos"""
        print("\n🎥 Gerando comandos FFmpeg...")
        
        commands = []
        
        for config in video_configs:
            if not config["letterings"]:
                continue
                
            board_name = config["board"]
            output_path = self.boards_target / board_name / config["output"]
            
            # Para múltiplas imagens (slideshow)
            if len(config["letterings"]) >= 1:
                # Criar lista de arquivos para FFmpeg
                filelist_path = self.boards_target / board_name / "filelist.txt"
                with open(filelist_path, 'w') as f:
                    for img in config["letterings"]:
                        f.write(f"file '{img}'\n")
                        f.write("duration 3\n")  # 3 segundos por imagem
                
                # Comando FFmpeg
                cmd = [
                    "ffmpeg", "-y",
                    "-f", "concat",
                    "-safe", "0",
                    "-i", str(filelist_path),
                    "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1",
                    "-pix_fmt", "yuv420p",
                    "-r", "30"
                ]
                
                # Adicionar áudio se existir
                if config["audio"]:
                    cmd.extend([
                        "-i", config["audio"],
                        "-c:a", "aac",
                        "-b:a", "128k",
                        "-shortest"
                    ])
                
                cmd.append(str(output_path))
                
                commands.append({
                    "board": board_name,
                    "command": cmd,
                    "description": f"Slideshow HD: {len(config['letterings'])} letterings"
                })
                
                print(f"  🎬 {board_name}: {len(config['letterings'])} imagens → vídeo")
        
        return commands
    
    def create_video_generation_script(self, ffmpeg_commands):
        """Cria script bash para gerar todos os vídeos"""
        video_script = self.project_root / "generate_videos.sh"
        
        with open(video_script, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("# FIRJAN XR - Video Generation Script\n")
            f.write(f"# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("echo '🎬 Gerando vídeos para FIRJAN XR...'\n")
            f.write("echo '================================'\n\n")
            
            for i, cmd_info in enumerate(ffmpeg_commands, 1):
                board = cmd_info["board"]
                description = cmd_info["description"]
                cmd = " ".join([f'"{arg}"' if " " in str(arg) else str(arg) for arg in cmd_info["command"]])
                
                f.write(f"echo '[{i}/{len(ffmpeg_commands)}] {board}: {description}'\n")
                f.write(f"{cmd}\n")
                f.write("if [ $? -eq 0 ]; then\n")
                f.write(f"    echo '✅ {board} concluído!'\n")
                f.write("else\n")
                f.write(f"    echo '❌ Erro ao gerar {board}'\n")
                f.write("fi\n")
                f.write("echo ''\n\n")
            
            f.write("echo '✅ Todos os vídeos foram processados!'\n")
        
        # Make executable
        os.chmod(video_script, 0o755)
        print(f"🎬 Script de vídeos criado: {video_script}")
        
        return video_script
    
    def create_github_commit_script(self, organized_files):
        """Cria script para commit no GitHub"""
        commit_script = self.project_root / "commit_letterings.sh"
        
        with open(commit_script, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("# FIRJAN XR - Letterings Update Script\n")
            f.write(f"# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("echo '🔄 Updating FIRJAN XR Letterings...'\n\n")
            
            # Add files
            f.write("# Add new letterings\n")
            for file_info in organized_files:
                relative_path = Path(file_info["target"]).relative_to(self.project_root)
                f.write(f"git add '{relative_path}'\n")
            
            f.write("\n# Commit changes\n")
            f.write(f"git commit -m 'Add letterings numerados - {len(organized_files)} files ({sum(f['size_mb'] for f in organized_files):.1f}MB)'\n\n")
            
            f.write("# Push to GitHub\n")
            f.write("git push origin main\n\n")
            
            f.write("echo '✅ Letterings updated on GitHub!'\n")
        
        # Make executable
        os.chmod(commit_script, 0o755)
        print(f"📝 Script de commit criado: {commit_script}")
        
        return commit_script
    
    def generate_summary_report(self, organized_files, video_configs, ffmpeg_commands):
        """Gera relatório final"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "letterings_organized": len(organized_files),
            "boards_updated": len(set(f["board"] for f in organized_files)),
            "videos_to_generate": len(ffmpeg_commands),
            "total_size_mb": round(sum(f["size_mb"] for f in organized_files), 2),
            "organized_files": organized_files,
            "video_configs": video_configs,
            "ffmpeg_commands": [{"board": cmd["board"], "description": cmd["description"]} for cmd in ffmpeg_commands]
        }
        
        report_path = self.project_root / "FIRJAN_XR_ASSETS" / "update_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 Relatório salvo em: {report_path}")
        return report
    
    def run_update(self):
        """Executa todo o processo de atualização"""
        print("🚀 FIRJAN XR - Iniciando atualização v2...")
        print("=" * 50)
        
        # 1. Organizar letterings
        organized_files = self.organize_letterings_for_github()
        
        # 2. Preparar estrutura de vídeos
        video_configs = self.prepare_video_structure()
        
        # 3. Gerar comandos FFmpeg
        ffmpeg_commands = self.generate_ffmpeg_commands(video_configs)
        
        # 4. Criar script de geração de vídeos
        video_script = self.create_video_generation_script(ffmpeg_commands)
        
        # 5. Criar script de commit
        commit_script = self.create_github_commit_script(organized_files)
        
        # 6. Gerar relatório
        report = self.generate_summary_report(organized_files, video_configs, ffmpeg_commands)
        
        print("\n" + "=" * 50)
        print("✅ ATUALIZAÇÃO COMPLETA!")
        print(f"📁 Letterings organizados: {len(organized_files)}")
        print(f"🎬 Vídeos para gerar: {len(ffmpeg_commands)}")
        print(f"📊 Tamanho total: {report['total_size_mb']:.1f} MB")
        print(f"🎯 Boards atualizados: {report['boards_updated']}")
        
        print("\n🔧 PRÓXIMOS PASSOS:")
        print(f"1. 📤 GitHub: {commit_script}")
        print(f"2. 🎬 Vídeos: {video_script}")
        print("3. 📊 Verificar relatório gerado")
        
        return report

if __name__ == "__main__":
    # Caminho para o projeto
    project_root = "/Users/cleliodepaula/Documents/_%20_%20_%20_%20_%20_%20_%20_%20_%20_refs/_%20agentes/wesense/____%20__%20_%20__%20_%20____AgentesWeSense/Neg%C3%B3cios/Firjan/BOARDS"
    
    updater = FirjanGitHubUpdater(project_root)
    report = updater.run_update() 