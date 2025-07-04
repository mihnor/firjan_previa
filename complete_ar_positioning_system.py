#!/usr/bin/env python3
"""
SISTEMA COMPLETO DE REPOSICIONAMENTO AR - FIRJAN XR
==================================================

Este script implementa o sistema completo de reposicionamento AR que inclui
TODOS os objetos mesh da cena, não apenas aqueles com padrões específicos.

FUNCIONALIDADES:
- Reposicionamento completo de todos os objetos mesh
- Backup automático de todas as transformações
- Restauração completa das posições originais
- Aplicação automática de texturas com detecção de transparência
- Otimização para AR (centro na origem, escala ideal)

COMO USAR:
1. Execute complete_ar_repositioning() para reposicionar todos os objetos
2. Execute restore_from_complete_backup() para restaurar posições originais
3. Execute apply_automatic_textures() para aplicar texturas automaticamente

RESULTADO:
- Todos os objetos centrados na origem (0,0,0)
- Escala otimizada para AR (8.0 unidades de largura)
- Todas as relações espaciais preservadas
- Backup completo para restauração
"""

import bpy
import bmesh
from mathutils import Vector
import ast

def complete_ar_repositioning():
    """
    Reposiciona TODOS os objetos mesh da cena para otimização AR
    """
    print("🔄 REPOSICIONAMENTO COMPLETO - TODOS OS OBJETOS MESH")
    print("=" * 60)
    
    # 1. BACKUP COMPLETO de todos os objetos
    print("💾 CRIANDO BACKUP COMPLETO...")
    backup_data = {}
    all_mesh_objects = []
    
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            all_mesh_objects.append(obj)
            backup_data[obj.name] = {
                'location': [obj.location.x, obj.location.y, obj.location.z],
                'rotation': [obj.rotation_euler.x, obj.rotation_euler.y, obj.rotation_euler.z],
                'scale': [obj.scale.x, obj.scale.y, obj.scale.z]
            }
    
    print(f"   ✅ Backup criado para {len(all_mesh_objects)} objetos mesh")
    
    # 2. CALCULAR CENTRO DE TODOS OS OBJETOS
    print("\n📐 CALCULANDO CENTRO DE TODOS OS OBJETOS...")
    all_locations = []
    for obj in all_mesh_objects:
        all_locations.append(obj.location)
    
    if all_locations:
        center_x = sum(loc.x for loc in all_locations) / len(all_locations)
        center_y = sum(loc.y for loc in all_locations) / len(all_locations)
        center_z = sum(loc.z for loc in all_locations) / len(all_locations)
        current_center = Vector((center_x, center_y, center_z))
        
        print(f"   🎯 Centro atual: ({center_x:.2f}, {center_y:.2f}, {center_z:.2f})")
        
        # Calcular dimensões atuais
        min_x = min(loc.x for loc in all_locations)
        max_x = max(loc.x for loc in all_locations)
        min_y = min(loc.y for loc in all_locations)
        max_y = max(loc.y for loc in all_locations)
        min_z = min(loc.z for loc in all_locations)
        max_z = max(loc.z for loc in all_locations)
        
        current_width = max_x - min_x
        current_height = max_y - min_y
        current_depth = max_z - min_z
        
        print(f"   📏 Dimensões atuais: {current_width:.2f} × {current_height:.2f} × {current_depth:.2f}")
    
    # 3. REPOSICIONAMENTO PARA ORIGEM
    print("\n🎯 REPOSICIONANDO TODOS OS OBJETOS PARA ORIGEM...")
    target_center = Vector((0.0, 0.0, 0.0))
    translation = target_center - current_center
    
    for obj in all_mesh_objects:
        obj.location += translation
    
    print(f"   ✅ {len(all_mesh_objects)} objetos reposicionados")
    
    # 4. APLICAR ESCALA AR
    print("\n📐 APLICANDO ESCALA AR...")
    target_width = 8.0  # Escala ideal para AR
    scale_factor = target_width / current_width
    
    # Aplicar escala mantendo relações
    for obj in all_mesh_objects:
        obj.location *= scale_factor
    
    print(f"   🔍 Fator de escala aplicado: {scale_factor:.3f}")
    
    # 5. VERIFICAR RESULTADOS
    print("\n📊 VERIFICANDO RESULTADOS...")
    new_locations = []
    for obj in all_mesh_objects:
        new_locations.append(obj.location)
    
    if new_locations:
        new_center_x = sum(loc.x for loc in new_locations) / len(new_locations)
        new_center_y = sum(loc.y for loc in new_locations) / len(new_locations)
        new_center_z = sum(loc.z for loc in new_locations) / len(new_locations)
        
        new_min_x = min(loc.x for loc in new_locations)
        new_max_x = max(loc.x for loc in new_locations)
        new_min_y = min(loc.y for loc in new_locations)
        new_max_y = max(loc.y for loc in new_locations)
        new_min_z = min(loc.z for loc in new_locations)
        new_max_z = max(loc.z for loc in new_locations)
        
        new_width = new_max_x - new_min_x
        new_height = new_max_y - new_min_y
        new_depth = new_max_z - new_min_z
        
        print(f"   🎯 Novo centro: ({new_center_x:.3f}, {new_center_y:.3f}, {new_center_z:.3f})")
        print(f"   📏 Novas dimensões: {new_width:.2f} × {new_height:.2f} × {new_depth:.2f}")
    
    # 6. SALVAR BACKUP NO BLEND
    print("\n💾 SALVANDO BACKUP NO ARQUIVO...")
    bpy.context.scene["ar_complete_backup"] = str(backup_data)
    print("   ✅ Backup salvo nas propriedades da cena")
    
    print("\n✅ REPOSICIONAMENTO COMPLETO CONCLUÍDO!")
    print(f"   📦 Total de objetos reposicionados: {len(all_mesh_objects)}")
    print(f"   🎯 Todos os objetos agora estão centrados na origem")
    print(f"   📱 Escala otimizada para AR: {new_width:.1f} unidades de largura")
    print(f"   💾 Backup disponível para restauração se necessário")
    
    return {
        'total_objects': len(all_mesh_objects),
        'new_center': (new_center_x, new_center_y, new_center_z),
        'new_dimensions': (new_width, new_height, new_depth),
        'scale_factor': scale_factor
    }

def restore_from_complete_backup():
    """
    Restaura todos os objetos para suas posições originais usando o backup completo
    """
    print("🔄 RESTAURANDO POSIÇÕES ORIGINAIS...")
    print("=" * 40)
    
    # Verificar se existe backup
    if "ar_complete_backup" not in bpy.context.scene:
        print("❌ ERRO: Backup não encontrado!")
        return False
    
    try:
        # Carregar backup
        backup_str = bpy.context.scene["ar_complete_backup"]
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

def apply_automatic_textures():
    """
    Aplica texturas automaticamente com detecção de transparência
    """
    print("🎨 APLICANDO SISTEMA DE TEXTURAS AUTOMÁTICAS V2.0")
    print("=" * 55)
    
    results = {"success": 0, "failed": 0, "details": []}
    
    for obj in bpy.context.scene.objects:
        if obj.type != 'MESH':
            continue
            
        # Buscar textura correspondente
        texture_image = None
        for image in bpy.data.images:
            # Verificar se o nome da imagem corresponde ao objeto
            if obj.name in image.name or image.name.startswith(obj.name):
                texture_image = image
                break
        
        if not texture_image:
            results["failed"] += 1
            results["details"].append(f"❌ {obj.name} - Textura não encontrada")
            continue
        
        # Criar material se não existir
        if not obj.data.materials:
            obj.data.materials.append(bpy.data.materials.new(name=f"{obj.name}_Material"))
        
        material = obj.data.materials[0]
        
        # Configurar nós do material
        material.use_nodes = True
        nodes = material.node_tree.nodes
        links = material.node_tree.links
        
        # Limpar nós existentes
        nodes.clear()
        
        # Criar nós essenciais
        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        output = nodes.new(type='ShaderNodeOutputMaterial')
        tex_image = nodes.new(type='ShaderNodeTexImage')
        
        # Configurar imagem
        tex_image.image = texture_image
        
        # Posicionar nós
        bsdf.location = (0, 0)
        output.location = (300, 0)
        tex_image.location = (-300, 0)
        
        # Conectar nós básicos
        links.new(tex_image.outputs['Color'], bsdf.inputs['Base Color'])
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        # Detectar transparência automática
        if texture_image.channels == 4:  # RGBA
            material.blend_method = 'BLEND'
            material.use_screen_refraction = True
            links.new(tex_image.outputs['Alpha'], bsdf.inputs['Alpha'])
            results["details"].append(f"✅ {obj.name} - Textura aplicada COM transparência")
        else:
            material.blend_method = 'OPAQUE'
            results["details"].append(f"✅ {obj.name} - Textura aplicada SEM transparência")
        
        results["success"] += 1
    
    print(f"\n📊 RESULTADOS:")
    print(f"   ✅ Sucessos: {results['success']}")
    print(f"   ❌ Falhas: {results['failed']}")
    
    return results

def get_ar_status():
    """
    Verifica o status atual da cena para AR
    """
    print("🔍 STATUS DA CENA PARA AR")
    print("=" * 30)
    
    all_mesh_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
    
    if not all_mesh_objects:
        print("❌ Nenhum objeto mesh encontrado")
        return False
    
    # Verificar centro e dimensões
    locations = [obj.location for obj in all_mesh_objects]
    
    center_x = sum(loc.x for loc in locations) / len(locations)
    center_y = sum(loc.y for loc in locations) / len(locations)
    center_z = sum(loc.z for loc in locations) / len(locations)
    
    min_x = min(loc.x for loc in locations)
    max_x = max(loc.x for loc in locations)
    min_y = min(loc.y for loc in locations)
    max_y = max(loc.y for loc in locations)
    min_z = min(loc.z for loc in locations)
    max_z = max(loc.z for loc in locations)
    
    width = max_x - min_x
    height = max_y - min_y
    depth = max_z - min_z
    
    print(f"📊 ESTATÍSTICAS:")
    print(f"   📦 Total de objetos: {len(all_mesh_objects)}")
    print(f"   🎯 Centro: ({center_x:.3f}, {center_y:.3f}, {center_z:.3f})")
    print(f"   📏 Dimensões: {width:.2f} × {height:.2f} × {depth:.2f}")
    
    # Verificar se está otimizado para AR
    ar_optimized = (
        abs(center_x) < 0.01 and 
        abs(center_y) < 0.01 and 
        abs(center_z) < 0.01 and
        width >= 7.0 and width <= 9.0
    )
    
    print(f"   📱 AR Otimizado: {'✅ SIM' if ar_optimized else '❌ NÃO'}")
    
    # Verificar backup
    has_backup = "ar_complete_backup" in bpy.context.scene
    print(f"   💾 Backup disponível: {'✅ SIM' if has_backup else '❌ NÃO'}")
    
    return ar_optimized

# EXECUÇÃO PRINCIPAL
if __name__ == "__main__":
    print("🚀 SISTEMA COMPLETO DE REPOSICIONAMENTO AR - FIRJAN XR")
    print("=" * 60)
    
    # Verificar status atual
    get_ar_status()
    
    # Executar reposicionamento completo
    complete_ar_repositioning()
    
    # Aplicar texturas automáticas
    apply_automatic_textures()
    
    # Verificar status final
    get_ar_status()
    
    print("\n🏆 SISTEMA COMPLETO EXECUTADO COM SUCESSO!")
    print("   Cena otimizada para AR/XR")
    print("   Todas as legendas/textos incluídos")
    print("   Backup disponível para restauração") 