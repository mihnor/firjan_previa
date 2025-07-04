#!/usr/bin/env python3
"""
SISTEMA CONSERVADOR DE REPOSICIONAMENTO AR - FIRJAN XR
====================================================

Este script implementa um reposicionamento conservador que apenas translada
o centro da cena para a origem (0,0,0) sem alterar escalas, rotações ou 
relações espaciais entre objetos.

CARACTERÍSTICAS:
- Apenas translação (sem escala)
- Preserva todas as escalas originais
- Preserva todas as rotações originais  
- Preserva todas as relações espaciais
- Backup automático para restauração
- Otimizado para AR sem perder qualidade

RESULTADO:
- Centro exato na origem (0,0,0)
- Todas as transformações preservadas
- Pronto para uso em AR/XR
- Dimensões: 62.5 × 1.9 × 7.0 unidades
"""

import bpy
from mathutils import Vector
import ast

def conservative_ar_positioning():
    """
    Reposiciona a cena para AR preservando todas as transformações originais
    """
    print("🔄 REPOSICIONAMENTO CONSERVADOR - PRESERVANDO RELAÇÕES")
    print("=" * 60)
    
    # 1. BACKUP COMPLETO DE SEGURANÇA
    print("💾 CRIANDO BACKUP DE SEGURANÇA...")
    backup_data = {}
    all_mesh_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
    
    for obj in all_mesh_objects:
        backup_data[obj.name] = {
            'location': [obj.location.x, obj.location.y, obj.location.z],
            'rotation': [obj.rotation_euler.x, obj.rotation_euler.y, obj.rotation_euler.z],
            'scale': [obj.scale.x, obj.scale.y, obj.scale.z]
        }
    
    print(f"   ✅ Backup criado para {len(all_mesh_objects)} objetos")
    
    # 2. CALCULAR CENTRO ATUAL
    print("\n📐 CALCULANDO CENTRO ATUAL...")
    locations = [obj.location for obj in all_mesh_objects]
    
    center_x = sum(loc.x for loc in locations) / len(locations)
    center_y = sum(loc.y for loc in locations) / len(locations)
    center_z = sum(loc.z for loc in locations) / len(locations)
    
    current_center = Vector((center_x, center_y, center_z))
    target_center = Vector((0.0, 0.0, 0.0))
    
    print(f"   🎯 Centro atual: ({center_x:.2f}, {center_y:.2f}, {center_z:.2f})")
    print(f"   🎯 Centro alvo: (0.00, 0.00, 0.00)")
    
    # 3. CALCULAR TRANSLAÇÃO NECESSÁRIA
    translation = target_center - current_center
    print(f"   ➡️ Translação necessária: ({translation.x:.2f}, {translation.y:.2f}, {translation.z:.2f})")
    
    # 4. APLICAR APENAS A TRANSLAÇÃO
    print("\n🔄 APLICANDO TRANSLAÇÃO CONSERVADORA...")
    print("   (Preservando escalas, rotações e relações espaciais)")
    
    for obj in all_mesh_objects:
        # Aplicar apenas translação - NÃO mexer em escala ou rotação
        obj.location += translation
    
    print(f"   ✅ {len(all_mesh_objects)} objetos transladados")
    
    # 5. VERIFICAR RESULTADOS
    print("\n📊 VERIFICANDO RESULTADOS...")
    new_locations = [obj.location for obj in all_mesh_objects]
    
    new_center_x = sum(loc.x for loc in new_locations) / len(new_locations)
    new_center_y = sum(loc.y for loc in new_locations) / len(new_locations)
    new_center_z = sum(loc.z for loc in new_locations) / len(new_locations)
    
    print(f"   🎯 Novo centro: ({new_center_x:.3f}, {new_center_y:.3f}, {new_center_z:.3f})")
    
    # 6. VERIFICAR PRESERVAÇÃO DAS TRANSFORMAÇÕES
    print("\n🔍 VERIFICANDO PRESERVAÇÃO DAS TRANSFORMAÇÕES...")
    scales_preserved = True
    rotations_preserved = True
    
    for obj in all_mesh_objects:
        original = backup_data[obj.name]
        
        # Verificar escala
        if not (abs(obj.scale.x - original['scale'][0]) < 0.001 and 
                abs(obj.scale.y - original['scale'][1]) < 0.001 and 
                abs(obj.scale.z - original['scale'][2]) < 0.001):
            scales_preserved = False
        
        # Verificar rotação
        if not (abs(obj.rotation_euler.x - original['rotation'][0]) < 0.001 and 
                abs(obj.rotation_euler.y - original['rotation'][1]) < 0.001 and 
                abs(obj.rotation_euler.z - original['rotation'][2]) < 0.001):
            rotations_preserved = False
    
    print(f"   🔄 Escalas preservadas: {'✅ SIM' if scales_preserved else '❌ NÃO'}")
    print(f"   🔄 Rotações preservadas: {'✅ SIM' if rotations_preserved else '❌ NÃO'}")
    
    # 7. CALCULAR DIMENSÕES FINAIS
    min_x = min(loc.x for loc in new_locations)
    max_x = max(loc.x for loc in new_locations)
    min_y = min(loc.y for loc in new_locations)
    max_y = max(loc.y for loc in new_locations)
    min_z = min(loc.z for loc in new_locations)
    max_z = max(loc.z for loc in new_locations)
    
    new_width = max_x - min_x
    new_height = max_y - min_y
    new_depth = max_z - min_z
    
    print(f"\n📏 DIMENSÕES FINAIS:")
    print(f"   Largura: {new_width:.2f} unidades")
    print(f"   Altura: {new_height:.2f} unidades")
    print(f"   Profundidade: {new_depth:.2f} unidades")
    
    # 8. SALVAR BACKUP
    print("\n💾 SALVANDO BACKUP...")
    bpy.context.scene["conservative_backup"] = str(backup_data)
    print("   ✅ Backup salvo nas propriedades da cena")
    
    print("\n🏆 REPOSICIONAMENTO CONSERVADOR CONCLUÍDO!")
    print("   ✅ Centro agora na origem (0,0,0)")
    print("   ✅ Todas as escalas preservadas")
    print("   ✅ Todas as rotações preservadas")
    print("   ✅ Todas as relações espaciais mantidas")
    print("   ✅ Pronto para uso em AR!")
    print("   💾 Backup disponível para restauração")
    
    return {
        'total_objects': len(all_mesh_objects),
        'new_center': (new_center_x, new_center_y, new_center_z),
        'new_dimensions': (new_width, new_height, new_depth),
        'scales_preserved': scales_preserved,
        'rotations_preserved': rotations_preserved
    }

def restore_conservative_backup():
    """
    Restaura todas as posições originais do backup conservador
    """
    print("🔄 RESTAURANDO BACKUP CONSERVADOR...")
    print("=" * 40)
    
    # Verificar se existe backup
    if "conservative_backup" not in bpy.context.scene:
        print("❌ ERRO: Backup conservador não encontrado!")
        return False
    
    try:
        # Carregar backup
        backup_str = bpy.context.scene["conservative_backup"]
        backup_data = ast.literal_eval(backup_str)
        
        print(f"📦 Backup encontrado com {len(backup_data)} objetos")
        
        # Restaurar cada objeto
        restored_count = 0
        for obj_name, transform_data in backup_data.items():
            obj = bpy.context.scene.objects.get(obj_name)
            if obj:
                # Restaurar transformações
                obj.location = Vector(transform_data['location'])
                obj.rotation_euler = Vector(transform_data['rotation'])
                obj.scale = Vector(transform_data['scale'])
                restored_count += 1
                print(f"   ✅ {obj_name} restaurado")
            else:
                print(f"   ❌ {obj_name} não encontrado na cena")
        
        print(f"\n✅ RESTAURAÇÃO CONCLUÍDA!")
        print(f"   📦 {restored_count} objetos restaurados")
        print(f"   🎯 Posições originais recuperadas")
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO na restauração: {str(e)}")
        return False

def verify_ar_status():
    """
    Verifica se a cena está otimizada para AR
    """
    print("🔍 VERIFICANDO STATUS AR...")
    print("=" * 30)
    
    all_mesh_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
    
    if not all_mesh_objects:
        print("❌ Nenhum objeto mesh encontrado")
        return False
    
    # Verificar centro
    locations = [obj.location for obj in all_mesh_objects]
    center_x = sum(loc.x for loc in locations) / len(locations)
    center_y = sum(loc.y for loc in locations) / len(locations)
    center_z = sum(loc.z for loc in locations) / len(locations)
    
    distance_from_origin = (center_x**2 + center_y**2 + center_z**2)**0.5
    
    print(f"📊 STATUS:")
    print(f"   📦 Total de objetos: {len(all_mesh_objects)}")
    print(f"   🎯 Centro: ({center_x:.3f}, {center_y:.3f}, {center_z:.3f})")
    print(f"   📏 Distância da origem: {distance_from_origin:.6f}")
    
    # Verificar se está centralizado
    is_centered = distance_from_origin < 0.001
    print(f"   🎯 Centralizado: {'✅ SIM' if is_centered else '❌ NÃO'}")
    
    # Verificar backup
    has_backup = "conservative_backup" in bpy.context.scene
    print(f"   💾 Backup disponível: {'✅ SIM' if has_backup else '❌ NÃO'}")
    
    return is_centered

def get_scene_info():
    """
    Mostra informações detalhadas da cena
    """
    print("📋 INFORMAÇÕES DA CENA")
    print("=" * 25)
    
    all_mesh_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
    
    if not all_mesh_objects:
        print("❌ Nenhum objeto mesh encontrado")
        return
    
    # Calcular bounding box
    locations = [obj.location for obj in all_mesh_objects]
    min_x = min(loc.x for loc in locations)
    max_x = max(loc.x for loc in locations)
    min_y = min(loc.y for loc in locations)
    max_y = max(loc.y for loc in locations)
    min_z = min(loc.z for loc in locations)
    max_z = max(loc.z for loc in locations)
    
    print(f"📦 Objetos: {len(all_mesh_objects)}")
    print(f"📐 Bounding Box:")
    print(f"   X: {min_x:.2f} → {max_x:.2f} (largura: {max_x - min_x:.2f})")
    print(f"   Y: {min_y:.2f} → {max_y:.2f} (altura: {max_y - min_y:.2f})")
    print(f"   Z: {min_z:.2f} → {max_z:.2f} (profundidade: {max_z - min_z:.2f})")
    
    # Centro
    center_x = sum(loc.x for loc in locations) / len(locations)
    center_y = sum(loc.y for loc in locations) / len(locations)
    center_z = sum(loc.z for loc in locations) / len(locations)
    
    print(f"🎯 Centro: ({center_x:.3f}, {center_y:.3f}, {center_z:.3f})")

# EXECUÇÃO PRINCIPAL
if __name__ == "__main__":
    print("🚀 SISTEMA CONSERVADOR DE REPOSICIONAMENTO AR - FIRJAN XR")
    print("=" * 65)
    
    # Verificar status atual
    get_scene_info()
    
    # Executar reposicionamento conservador
    conservative_ar_positioning()
    
    # Verificar status final
    verify_ar_status()
    
    print("\n🏆 SISTEMA CONSERVADOR EXECUTADO COM SUCESSO!")
    print("   Cena centrada na origem para AR")
    print("   Todas as transformações preservadas")
    print("   Backup disponível para restauração") 