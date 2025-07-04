#!/usr/bin/env python3
"""
🎯 SISTEMA DE REPOSICIONAMENTO PARA AR/XR - FIRJAN
==================================================

Script completo para reposicionar cenas 3D para uso em Realidade Aumentada
mantendo todas as relações espaciais entre objetos.

Autor: AI Assistant via MCP Blender
Data: Julho 2025
Projeto: Casa Firjan - Exposição XR
"""

import bpy
from mathutils import Vector
import json

def save_position_backup(backup_name="ar_backup"):
    """
    Salva backup completo das posições, rotações e escalas
    """
    backup_data = {}
    
    for obj in bpy.context.scene.objects:
        if obj.type in ['MESH', 'LIGHT', 'CAMERA', 'EMPTY']:
            backup_data[obj.name] = {
                'location': [obj.location.x, obj.location.y, obj.location.z],
                'rotation': [obj.rotation_euler.x, obj.rotation_euler.y, obj.rotation_euler.z],
                'scale': [obj.scale.x, obj.scale.y, obj.scale.z],
                'type': obj.type
            }
    
    # Salvar no custom properties da cena
    bpy.context.scene[backup_name] = json.dumps(backup_data)
    
    print(f"💾 BACKUP SALVO: '{backup_name}'")
    print(f"   {len(backup_data)} objetos salvos")
    
    return backup_data

def restore_position_backup(backup_name="ar_backup"):
    """
    Restaura backup de posições
    """
    if backup_name not in bpy.context.scene:
        print(f"❌ Backup '{backup_name}' não encontrado!")
        return False
    
    try:
        backup_data = json.loads(bpy.context.scene[backup_name])
        
        restored = 0
        for obj_name, data in backup_data.items():
            obj = bpy.data.objects.get(obj_name)
            if obj:
                obj.location = Vector(data['location'])
                obj.rotation_euler = Vector(data['rotation'])
                obj.scale = Vector(data['scale'])
                restored += 1
        
        print(f"🔄 BACKUP RESTAURADO: '{backup_name}'")
        print(f"   {restored} objetos restaurados")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao restaurar backup: {e}")
        return False

def reposition_for_ar(target_center=Vector((0, 0, 0)), move_lights=True):
    """
    Reposiciona todos os objetos para AR mantendo posições relativas
    """
    # Coletar objetos relevantes
    relevant_objects = []
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH' and (obj.name.startswith('BOARD_') or 'let_' in obj.name):
            relevant_objects.append(obj)
    
    if not relevant_objects:
        print("❌ Nenhum objeto relevante encontrado!")
        return False
    
    # Calcular centro atual
    positions = [obj.location for obj in relevant_objects]
    current_center = Vector([
        sum(pos.x for pos in positions) / len(positions),
        sum(pos.y for pos in positions) / len(positions),
        sum(pos.z for pos in positions) / len(positions)
    ])
    
    # Calcular offset
    offset = target_center - current_center
    
    print(f"🎯 REPOSICIONAMENTO PARA AR:")
    print(f"   Centro atual: ({current_center.x:6.2f}, {current_center.y:6.2f}, {current_center.z:6.2f})")
    print(f"   Centro alvo: ({target_center.x:6.2f}, {target_center.y:6.2f}, {target_center.z:6.2f})")
    print(f"   Offset: ({offset.x:6.2f}, {offset.y:6.2f}, {offset.z:6.2f})")
    
    # Mover objetos principais
    for obj in relevant_objects:
        obj.location += offset
    
    # Mover luzes se solicitado
    if move_lights:
        for obj in bpy.context.scene.objects:
            if obj.type in ['LIGHT', 'CAMERA', 'EMPTY']:
                if not (obj.name == 'INIT' and obj.location.length < 0.1):
                    obj.location += offset
    
    print(f"   ✅ {len(relevant_objects)} objetos reposicionados")
    return True

def scale_scene_for_ar(target_width=8.0):
    """
    Escala toda a cena para largura ideal para AR
    """
    # Coletar objetos relevantes
    relevant_objects = []
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH' and (obj.name.startswith('BOARD_') or 'let_' in obj.name):
            relevant_objects.append(obj)
    
    if not relevant_objects:
        return False
    
    # Calcular largura atual
    positions = [obj.location for obj in relevant_objects]
    current_width = max(pos.x for pos in positions) - min(pos.x for pos in positions)
    scale_factor = target_width / current_width
    
    print(f"📏 ESCALA PARA AR:")
    print(f"   Largura atual: {current_width:6.2f}")
    print(f"   Largura alvo: {target_width:6.2f}")
    print(f"   Fator de escala: {scale_factor:6.4f}")
    
    # Aplicar escala a posições e objetos
    for obj in relevant_objects:
        obj.location *= scale_factor
        obj.scale *= scale_factor
    
    # Escalar luzes
    for obj in bpy.context.scene.objects:
        if obj.type == 'LIGHT':
            obj.location *= scale_factor
    
    print(f"   ✅ Escala aplicada a {len(relevant_objects)} objetos")
    return True

def optimize_heights_for_ar():
    """
    Otimiza alturas (Z) para AR
    """
    relevant_objects = []
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH' and (obj.name.startswith('BOARD_') or 'let_' in obj.name):
            relevant_objects.append(obj)
    
    if not relevant_objects:
        return False
    
    # Calcular Z médio e aplicar offset para Z≈0
    avg_z = sum(obj.location.z for obj in relevant_objects) / len(relevant_objects)
    z_offset = -avg_z
    
    for obj in relevant_objects:
        obj.location.z += z_offset
    
    print(f"📏 ALTURA OTIMIZADA:")
    print(f"   Z médio era: {avg_z:6.2f}")
    print(f"   Offset aplicado: {z_offset:+6.2f}")
    print(f"   ✅ Objetos agora próximos de Z=0")
    
    return True

def complete_ar_setup(target_width=8.0):
    """
    Setup completo para AR: backup + reposicionamento + escala + otimização
    """
    print("🚀 SETUP COMPLETO PARA AR/XR")
    print("=" * 40)
    
    # 1. Salvar backup
    print("1. Salvando backup...")
    save_position_backup("before_ar_setup")
    
    # 2. Reposicionar para origem
    print("\n2. Reposicionando para origem...")
    reposition_for_ar()
    
    # 3. Escalar para AR
    print(f"\n3. Escalando para {target_width} units...")
    scale_scene_for_ar(target_width)
    
    # 4. Otimizar alturas
    print("\n4. Otimizando alturas...")
    optimize_heights_for_ar()
    
    # 5. Salvar resultado
    print("\n5. Salvando resultado...")
    save_position_backup("ar_optimized")
    
    print(f"\n🎉 SETUP AR COMPLETO!")
    print(f"✅ Centro na origem (0,0,0)")
    print(f"✅ Largura de {target_width} units")
    print(f"✅ Altura otimizada (Z≈0)")
    print(f"✅ Backups salvos")
    print(f"🎯 PRONTO PARA AR/XR!")
    
    return True

def get_scene_stats():
    """
    Obtém estatísticas da cena atual
    """
    relevant_objects = []
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH' and (obj.name.startswith('BOARD_') or 'let_' in obj.name):
            relevant_objects.append(obj)
    
    if not relevant_objects:
        return None
    
    positions = [obj.location for obj in relevant_objects]
    
    # Centro
    center = Vector([
        sum(pos.x for pos in positions) / len(positions),
        sum(pos.y for pos in positions) / len(positions),
        sum(pos.z for pos in positions) / len(positions)
    ])
    
    # Dimensões
    min_x = min(pos.x for pos in positions)
    max_x = max(pos.x for pos in positions)
    min_y = min(pos.y for pos in positions)
    max_y = max(pos.y for pos in positions)
    min_z = min(pos.z for pos in positions)
    max_z = max(pos.z for pos in positions)
    
    stats = {
        'object_count': len(relevant_objects),
        'center': center,
        'width': max_x - min_x,
        'height': max_y - min_y,
        'depth': max_z - min_z,
        'bounds': {
            'x': [min_x, max_x],
            'y': [min_y, max_y],
            'z': [min_z, max_z]
        }
    }
    
    return stats

# INSTRUÇÕES DE USO:
"""
Para usar este sistema no Blender:

1. Execute o arquivo inteiro no Text Editor do Blender

2. Funções principais:
   - complete_ar_setup(8.0) - Setup completo para AR (RECOMENDADO)
   - save_position_backup("nome") - Salvar backup
   - restore_position_backup("nome") - Restaurar backup
   - get_scene_stats() - Ver estatísticas

3. Exemplo de uso completo:
   >>> complete_ar_setup(8.0)  # Setup para 8 units de largura
   >>> get_scene_stats()       # Ver resultado

4. Para reverter:
   >>> restore_position_backup("before_ar_setup")

CONFIGURAÇÕES RECOMENDADAS:
- AR Mobile: complete_ar_setup(2.0)
- AR Ambiente: complete_ar_setup(8.0)  ← PADRÃO
- AR Mundo: complete_ar_setup(15.0)
- AR Exposição: complete_ar_setup(25.0)
"""

if __name__ == "__main__":
    # Executar setup padrão se o script for executado diretamente
    print("Executando setup padrão para AR...")
    complete_ar_setup(8.0) 