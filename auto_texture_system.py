#!/usr/bin/env python3
"""
🤖 SISTEMA AUTOMÁTICO DE TEXTURAS E MOLDURAS - FIRJAN XR
========================================================

Este arquivo contém a função automática para aplicar texturas e molduras
nos objetos do projeto Firjan XR no Blender.

Autor: AI Assistant via MCP Blender
Data: Julho 2025
Projeto: Casa Firjan - Exposição XR
Versão: 2.0 - Inclui suporte automático à transparência
"""

import bpy

def auto_texture_system_with_transparency():
    """
    Sistema automático MELHORADO com suporte a transparência
    Versão 2.0 - Inclui detecção automática de canal alpha
    
    FUNCIONALIDADES:
    - Detecta automaticamente imagens baseado no nome dos objetos
    - Aplica texturas correspondentes sem intervenção manual
    - Diferencia entre textos (let_) e imagens (BOARD_)
    - Aplica molduras elegantes apenas nas imagens
    - DETECTA TRANSPARÊNCIA AUTOMATICAMENTE (canal alpha)
    - Cria materiais inteligentes (transparentes ou opacos)
    
    RETORNA:
    tuple: (sucessos, materiais_transparentes, materiais_opacos)
    """
    
    print("🤖 SISTEMA AUTOMÁTICO V2.0 - COM TRANSPARÊNCIA")
    print("=" * 55)
    
    def find_matching_image(obj_name):
        """Encontra imagem correspondente ao objeto"""
        clean_name = obj_name.replace("BOARD_", "").replace("board_", "")
        
        possible_names = [
            obj_name,
            f"{obj_name}.png",
            f"{obj_name}.jpg", 
            clean_name,
            f"{clean_name}.png",
            f"{clean_name}.jpg"
        ]
        
        for img in bpy.data.images:
            for possible_name in possible_names:
                if possible_name.lower() in img.name.lower():
                    return img
        return None
    
    def create_smart_material(obj, image):
        """Cria material inteligente com transparência se necessário"""
        
        # Detectar se precisa de transparência
        needs_transparency = image.channels == 4  # RGBA
        
        # Criar material
        mat_name = f"{obj.name}_Smart"
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        
        # Configurar transparência se necessário
        if needs_transparency:
            mat.blend_method = 'BLEND'
            mat.show_transparent_back = False
        else:
            mat.blend_method = 'OPAQUE'
        
        # Limpar nodes
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        # Criar nodes
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (400, 0)
        
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        principled.location = (200, 0)
        
        image_node = nodes.new(type='ShaderNodeTexImage')
        image_node.location = (0, 0)
        image_node.image = image
        
        # Conectar nodes
        links.new(image_node.outputs['Color'], principled.inputs['Base Color'])
        links.new(principled.outputs['BSDF'], output_node.inputs['Surface'])
        
        # Conectar alpha apenas se necessário
        if needs_transparency:
            links.new(image_node.outputs['Alpha'], principled.inputs['Alpha'])
            principled.inputs['Alpha'].default_value = 1.0
        
        return mat, needs_transparency
    
    def apply_frame_to_image(obj):
        """Aplica molduras elegantes apenas às imagens"""
        if not obj.name.startswith('BOARD_'):
            return False
            
        # Verificar se já tem molduras
        has_solidify = any(mod.type == 'SOLIDIFY' for mod in obj.modifiers)
        has_bevel = any(mod.type == 'BEVEL' for mod in obj.modifiers)
        
        if not has_solidify:
            solidify = obj.modifiers.new(name="Frame_Depth", type='SOLIDIFY')
            solidify.thickness = 0.02
            solidify.offset = -1.0
        
        if not has_bevel:
            bevel = obj.modifiers.new(name="Frame_Bevel", type='BEVEL')
            bevel.width = 0.02
            bevel.segments = 3
            bevel.profile = 0.7
        
        return True
    
    # Processar todos os objetos relevantes
    processed = 0
    transparent_materials = 0
    opaque_materials = 0
    frames_applied = 0
    
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH' and (obj.name.startswith('BOARD_') or 'let_' in obj.name):
            
            # Encontrar imagem correspondente
            matching_image = find_matching_image(obj.name)
            
            if matching_image:
                # Criar material inteligente
                smart_mat, has_transparency = create_smart_material(obj, matching_image)
                
                # Aplicar material
                obj.data.materials.clear()
                obj.data.materials.append(smart_mat)
                
                processed += 1
                if has_transparency:
                    transparent_materials += 1
                    transparency_status = "🔮 TRANSPARENTE"
                else:
                    opaque_materials += 1
                    transparency_status = "⚫ OPACO"
                
                print(f"   ✅ {obj.name} → {matching_image.name} ({transparency_status})")
                
                # Aplicar moldura apenas às imagens
                if obj.name.startswith('BOARD_'):
                    if apply_frame_to_image(obj):
                        frames_applied += 1
    
    print(f"\n📊 RESULTADO V2.0:")
    print(f"   ✅ Objetos processados: {processed}")
    print(f"   🔮 Materiais transparentes: {transparent_materials}")
    print(f"   ⚫ Materiais opacos: {opaque_materials}")
    print(f"   🖼️ Molduras aplicadas: {frames_applied}")
    print("🤖 Sistema automático V2.0 finalizado!")
    
    return processed, transparent_materials, opaque_materials

def auto_texture_system():
    """
    Sistema automático de aplicação de texturas - função reutilizável
    
    FUNCIONALIDADES:
    - Detecta automaticamente imagens baseado no nome dos objetos
    - Aplica texturas correspondentes sem intervenção manual
    - Diferencia entre textos (let_) e imagens (BOARD_)
    - Aplica molduras elegantes apenas nas imagens
    
    RETORNA:
    tuple: (sucessos, falhas)
    """
    
    print("🤖 SISTEMA AUTOMÁTICO DE TEXTURAS - EXECUTANDO")
    print("=" * 55)
    
    def find_matching_image(obj_name):
        """Encontra imagem correspondente ao objeto"""
        clean_name = obj_name.replace("BOARD_", "").replace("board_", "")
        
        possible_names = [
            obj_name,  # Nome exato
            f"{obj_name}.png",
            f"{obj_name}.jpg", 
            clean_name,
            f"{clean_name}.png",
            f"{clean_name}.jpg"
        ]
        
        for img in bpy.data.images:
            for possible_name in possible_names:
                if possible_name.lower() in img.name.lower():
                    return img
        return None
    
    def apply_texture_to_object(obj, image):
        """Aplica textura ao objeto"""
        # Criar/atualizar material
        if len(obj.data.materials) == 0:
            mat = bpy.data.materials.new(name=f"{obj.name}_Auto")
            obj.data.materials.append(mat)
        else:
            mat = obj.data.materials[0]
        
        # Configurar nodes
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        
        # Encontrar ou criar Image Texture node
        image_node = None
        for node in nodes:
            if node.type == 'TEX_IMAGE':
                image_node = node
                break
        
        if not image_node:
            nodes.clear()
            output_node = nodes.new(type='ShaderNodeOutputMaterial')
            output_node.location = (400, 0)
            
            principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            principled.location = (200, 0)
            
            image_node = nodes.new(type='ShaderNodeTexImage')
            image_node.location = (0, 0)
            
            links.new(image_node.outputs['Color'], principled.inputs['Base Color'])
            links.new(principled.outputs['BSDF'], output_node.inputs['Surface'])
        
        image_node.image = image
        return True
    
    def apply_frame_to_image(obj):
        """Aplica molduras elegantes apenas às imagens"""
        if not obj.name.startswith('BOARD_'):
            return False
            
        # Verificar se já tem molduras
        has_solidify = any(mod.type == 'SOLIDIFY' for mod in obj.modifiers)
        has_bevel = any(mod.type == 'BEVEL' for mod in obj.modifiers)
        
        if not has_solidify:
            solidify = obj.modifiers.new(name="Frame_Depth", type='SOLIDIFY')
            solidify.thickness = 0.02
            solidify.offset = -1.0
        
        if not has_bevel:
            bevel = obj.modifiers.new(name="Frame_Bevel", type='BEVEL')
            bevel.width = 0.02
            bevel.segments = 3
            bevel.profile = 0.7
        
        return True
    
    # Processar todos os objetos relevantes
    processed = 0
    failed = 0
    frames_applied = 0
    
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH' and (obj.name.startswith('BOARD_') or 'let_' in obj.name):
            # Aplicar textura
            matching_image = find_matching_image(obj.name)
            
            if matching_image:
                if apply_texture_to_object(obj, matching_image):
                    processed += 1
                    print(f"   ✅ {obj.name} → {matching_image.name}")
                else:
                    failed += 1
                    print(f"   ❌ Falha ao aplicar textura em {obj.name}")
            else:
                failed += 1
                print(f"   ⚠️ Sem imagem para {obj.name}")
            
            # Aplicar moldura apenas às imagens
            if obj.name.startswith('BOARD_'):
                if apply_frame_to_image(obj):
                    frames_applied += 1
    
    print(f"\n📊 RESULTADO:")
    print(f"   ✅ Texturas aplicadas: {processed}")
    print(f"   🖼️ Molduras aplicadas: {frames_applied}")
    print(f"   ⚠️ Falhas: {failed}")
    print("🤖 Sistema automático finalizado!")
    
    return processed, failed

def quick_texture_check():
    """Verificação rápida do status das texturas"""
    print("🔍 VERIFICAÇÃO RÁPIDA DE TEXTURAS")
    print("=" * 40)
    
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH' and (obj.name.startswith('BOARD_') or 'let_' in obj.name):
            has_texture = False
            has_frame = any(mod.type in ['SOLIDIFY', 'BEVEL'] for mod in obj.modifiers)
            has_transparency = False
            
            if len(obj.data.materials) > 0:
                mat = obj.data.materials[0]
                if mat and mat.use_nodes:
                    for node in mat.node_tree.nodes:
                        if node.type == 'TEX_IMAGE' and node.image:
                            has_texture = True
                            break
                    
                    # Verificar transparência
                    if mat.blend_method == 'BLEND':
                        has_transparency = True
            
            obj_type = "📝" if 'let_' in obj.name else "🖼️"
            texture_status = "✅" if has_texture else "❌"
            frame_status = "🖼️" if has_frame else "📝"
            transparency_status = "🔮" if has_transparency else "⚫"
            
            print(f"   {obj_type} {texture_status} {frame_status} {transparency_status} {obj.name}")

# INSTRUÇÕES DE USO:
"""
Para usar este sistema no Blender:

1. Execute o arquivo inteiro no Text Editor do Blender
2. Use as funções:
   - auto_texture_system_with_transparency() - V2.0 COM TRANSPARÊNCIA AUTOMÁTICA (RECOMENDADO)
   - auto_texture_system() - Versão básica
   - quick_texture_check() - Verifica status atual

EXEMPLO:
>>> auto_texture_system_with_transparency()  # RECOMENDADO
>>> quick_texture_check()

REGRAS:
- Objetos com 'let_' no nome = TEXTOS (sem molduras)
- Objetos 'BOARD_' = IMAGENS (com molduras)
- Texturas são aplicadas por correspondência de nomes
- Transparência é detectada automaticamente (canal alpha)

VERSÃO 2.0 NOVIDADES:
- ✅ Detecção automática de transparência
- ✅ Materiais inteligentes
- ✅ Blend Mode correto (BLEND/OPAQUE)
- ✅ Conexão automática do canal alpha
""" 