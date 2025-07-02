# 🎨 GUIA PROTOTIPAGEM: Figmin XR para FIRJAN
**Desenvolvimento Rápido do Teaser "De Onde Vem o Livro que Você Lê?"**

## 🎯 VISÃO GERAL

### **O que é Figmin XR?**
Figmin XR é uma ferramenta de prototipagem imersiva que permite criar experiências holográficas de forma intuitiva, sem necessidade de programação. Perfeita para validação rápida de conceitos XR.

### **Vantagens para o Projeto FIRJAN:**
- ⚡ **Prototipagem em 1 semana** vs. 4-5 semanas Unity
- 💰 **Baixo custo inicial** para validação
- 🔄 **Iterações rápidas** baseadas em feedback
- 🎮 **Nativo Meta Quest** 2/3/Pro
- 👥 **Multiplayer até 2 usuários** simultâneos

---

## 🛠️ SETUP INICIAL

### **1. Instalação & Configuração**

```bash
# Via Meta Quest Store
1. Abrir Quest Store no headset
2. Buscar "Figmin XR"
3. Download & Install (gratuito)
4. Launch app

# Via SideQuest (alternativo)
1. Baixar APK do Figmin XR
2. Instalar via SideQuest
3. Configurar permissões
```

### **2. Preparação dos Assets**

```bash
# Organização de Arquivos (Desktop)
FIRJAN_Assets/
├── Images/
│   ├── Board_01_Pergunta.png (otimizada 1024x1024)
│   ├── Board_02_Gutenberg.png
│   ├── Board_03_Tipografia.png
│   └── ... (todos os 12 boards)
├── 3D_Models/
│   ├── Gutenberg_Bust.obj
│   ├── Typography_3D.fbx
│   └── Book_Stack.glb
├── Audio/
│   ├── Guta_Welcome.mp3
│   ├── Board_Narrations/
│   └── SFX/
└── References/
    ├── Roteiro_Guta.txt
    └── Board_Sequence.pdf
```

### **3. Otimização de Assets**

```bash
# Imagens (usar Photoshop/GIMP)
- Resolução: 1024x1024 pixels máximo
- Formato: PNG com transparência
- Compressão: 80% qualidade
- Background: Transparente quando necessário

# Modelos 3D
- Polígonos: <5000 faces por modelo
- Formato: GLB/GLTF (preferencial)
- Texturas: 512x512 max
- Animações: Simples, <30 frames

# Áudio
- Formato: MP3, 44.1kHz
- Bitrate: 128kbps
- Duração: <60s por clipe
- Normalization: -12dB peak
```

---

## 🏗️ CONSTRUÇÃO DA EXPERIÊNCIA

### **FASE 1: Setup do Ambiente (1 dia)**

#### **Configuração Espacial**
```
1. Abrir Figmin XR no Quest
2. Create New Scene: "FIRJAN_Teaser"
3. Set Environment: "Studio Space" (fundo neutro)
4. Configure Lighting: "Soft Natural" 
5. Set Scale: "Room Scale" (3x3m working area)
```

#### **Import Base Assets**
```
1. Menu → Import → Images
   - Upload todos os 12 boards
   - Configurar como "UI Panels"
   - Tamanho: 1.5m width cada

2. Menu → Import → 3D Models
   - Gutenberg bust
   - Typography elements
   - Book models

3. Menu → Import → Audio
   - Guta voiceover files
   - Background ambience
   - UI sound effects
```

### **FASE 2: Layout Espacial (1 dia)**

#### **Posicionamento dos Boards**
```javascript
// Configuração espacial dos boards
Board Layout (Vista Superior):

    👤 User Start Position
         ↓
    [1] → [2] → [3] → [4]
                        ↓
    [8] ← [7] ← [6] ← [5]
     ↓
    [9] → [10] → [11] → [12]

// Coordenadas aproximadas (em metros)
Board_01: Position(0, 1.5, 2)     // Altura olho, 2m frente
Board_02: Position(2, 1.5, 2)     // 2m direita
Board_03: Position(4, 1.5, 2)     // 4m direita
// ... continuar sequência
```

#### **Setup da Jornada Guiada**
```
1. Create Path System:
   - Start Point: User spawn
   - Waypoints: Em frente a cada board
   - End Point: Final experience

2. Add Navigation Hints:
   - Floating arrows 3D
   - Glow effects nos próximos boards
   - Audio spatial cues

3. Configure Interaction Zones:
   - Trigger areas: 1.5m radius cada board
   - Activation: Gaze + Hand gesture
   - Feedback: Scale animation + audio
```

### **FASE 3: Interatividade Core (2 dias)**

#### **Sistema de Boards Interativos**

```javascript
// Para cada Board (1-12):

Board Settings:
├── Trigger Type: "Gaze + Gesture"
├── Activation Distance: 1.5m
├── Visual Feedback: Scale(1.0 → 1.1) + Glow
├── Audio: Board-specific narration
├── Duration: Auto-advance after 30s
└── Next Board: Auto-show + navigation hint

Interaction Flow:
1. User approaches board (proximity trigger)
2. Board highlights + scale animation
3. Gaze for 2s OR hand gesture activates
4. Audio narration plays (Guta voice)
5. Visual content displays (images/3D)
6. Auto-advance to next after completion
```

#### **Avatar Guta (Simplified)**

```javascript
// Guta Character (usando assets Figmin)
Guta Setup:
├── Base Model: Female avatar from library
├── Position: Floating 1.5m height, left side
├── Animation: Idle float + gesture pointing
├── Voice: Pre-recorded MP3 files
├── Behavior: Follow user at 2m distance
└── Interaction: Point to active board

// Guta Voice Triggers
Welcome: "Olá! Eu sou a Guta..."
Board_Intro: "Tá vendo esse cara aí do lado?"
Transition: "Vamos passar pela evolução..."
Closing: "Gostou? Essa foi uma provinha..."
```

### **FASE 4: Sequência Narrativa (1 dia)**

#### **Roteiro Interativo Implementado**

```
CENA 1: BOAS-VINDAS (30s)
├── Fade-in from black
├── Guta aparece com welcome message
├── Board 1 se materializa: "VOCÊ SABE DE ONDE VEM O LIVRO?"
├── Aguarda interação usuário
└── Transition: Guta gesture → Board 2

CENA 2: JORNADA GUTENBERG (60s)
├── Board 2: Retrato Gutenberg + narração Guta
├── 3D Element: Tipo móvel interativo aparece
├── Mini-interaction: User pode "tocar" tipo móvel
├── Audio: "Ele inventou o tipo móvel..."
└── Auto-advance para Board 3

CENA 3: EVOLUÇÃO TIPOGRÁFICA (45s)
├── Board 3: Galeria de fontes modernas
├── Efeito: Letras flutuam ao redor do user
├── Spotlight: Escritores brasileiros
├── Connection: Indústria gráfica nacional
└── Transition para Board 4

[... continuar para todos os 12 boards]

CENA FINAL: CONVITE EVENTO (30s)
├── Boards 6-11: Preview Casa Firjan
├── 3D Logo: Casa Firjan materializa
├── Date/Time: "17 de setembro"
├── Guta: "A gente se vê lá!"
└── Fade-out + restart option
```

---

## 🎮 INTERAÇÕES E MECÂNICAS

### **Sistema de Navegação**

```javascript
Navigation Types:
├── Gaze-based: 2s olhar fixo ativa
├── Hand Gesture: Point + pinch
├── Voice: "Próximo" / "Avançar"
├── Auto-advance: 30s timeout
└── Manual: Hand controller button

Progress Indicators:
├── Floating UI: "3/12" boards
├── Minimap: Dots showing progression
├── Guta: Verbal confirmations
└── Visual: Completed boards fade slightly
```

### **Feedback Systems**

```javascript
Visual Feedback:
├── Hover: Board scale +10% + blue glow
├── Active: Pulsing animation + audio
├── Completed: Green checkmark + fade
└── Next: Yellow highlight + arrow

Audio Feedback:
├── Hover: Subtle "ping" sound
├── Activation: "Click" + board narration
├── Completion: Success chime
└── Guta: Contextual voice responses

Haptic Feedback:
├── Quest Controllers: Vibration on interaction
├── Hand Tracking: Visual hand glow
└── Spatial: Controller rumble proximity
```

---

## 📊 TESTING & ITERATION

### **Testing Protocol (2 dias)**

```bash
Day 1: Internal Testing
├── Solo Experience: Complete walkthrough
├── Performance Check: Frame rate stability
├── Audio Sync: Voice + visual alignment
├── Navigation Flow: Intuitive progression
└── Bug Documentation: Issues tracking

Day 2: Stakeholder Testing
├── FIRJAN Team: Content accuracy
├── Target Audience: 3-5 industry professionals
├── Feedback Collection: Structured questionnaire
├── Iteration Planning: Priority fixes
└── Final Polish: Based on feedback
```

### **Key Metrics to Track**

```javascript
Technical Metrics:
├── Frame Rate: Consistent 72fps (Quest 2)
├── Load Times: <3s between boards
├── Audio Latency: <100ms trigger to sound
└── Interaction Response: <200ms visual feedback

Experience Metrics:
├── Completion Rate: Target >90%
├── Session Duration: 4-5 minutes optimal
├── Interaction Success: >95% first-try
├── User Satisfaction: 4.5/5 rating
└── Content Comprehension: Post-test quiz
```

---

## 🔧 OPTIMIZAÇÃO & EXPORT

### **Performance Optimization**

```javascript
Figmin Optimization Settings:
├── Render Quality: "High" (Quest 3) / "Medium" (Quest 2)
├── LOD System: Auto-enabled for 3D models
├── Audio Compression: Automatic optimization
├── Texture Streaming: Enable for large images
└── Memory Management: Auto-cleanup unused assets

Best Practices:
├── Keep scene under 100MB total
├── Limit concurrent audio to 3 sources
├── Use particle effects sparingly
├── Optimize lighting for mobile GPU
└── Test on oldest target device (Quest 2)
```

### **Export & Sharing**

```bash
# Export Options Figmin XR
1. Share Link: Generate public URL
   - Duration: 30 days
   - Access: Link-based
   - Analytics: Basic view tracking

2. Export APK: Standalone app
   - Custom branding
   - Offline playback
   - No Figmin dependency

3. Cloud Save: Version control
   - Multiple iterations
   - Collaborative editing
   - Backup security
```

---

## 📋 TIMELINE DETALHADO

### **Semana 1: Desenvolvimento Completo**

```bash
DIA 1: Setup & Import (8h)
├── 09:00-11:00: Configuração ambiente
├── 11:00-13:00: Preparação assets
├── 14:00-16:00: Import para Figmin XR
├── 16:00-18:00: Layout espacial básico
└── Output: Assets importados, ambiente configurado

DIA 2: Layout & Navegação (8h)
├── 09:00-12:00: Posicionamento boards
├── 13:00-15:00: Sistema navegação
├── 15:00-17:00: Triggers e zonas interação
├── 17:00-18:00: Teste navegação básica
└── Output: Layout espacial completo

DIA 3: Interatividade (8h)
├── 09:00-12:00: Board interactions
├── 13:00-15:00: Audio integration
├── 15:00-17:00: Guta avatar setup
├── 17:00-18:00: Feedback systems
└── Output: Interações funcionais

DIA 4: Conteúdo & Narrativa (8h)
├── 09:00-12:00: Sequência narrativa
├── 13:00-15:00: Roteiro Guta completo
├── 15:00-17:00: Polish visual/audio
├── 17:00-18:00: Integration testing
└── Output: Experiência completa

DIA 5: Testing & Polish (8h)
├── 09:00-11:00: Internal testing
├── 11:00-13:00: Bug fixes
├── 14:00-16:00: Stakeholder demo
├── 16:00-18:00: Final adjustments
└── Output: Versão pronta para apresentação
```

---

## 💡 DICAS AVANÇADAS

### **Otimização Específica Quest**

```javascript
Quest 2 Optimizations:
├── Resolution: 1832×1920 per eye
├── Refresh Rate: 72Hz (90Hz opcional)
├── Memory: 6GB RAM (Android app limit: 2-3GB)
├── Storage: Microsd support
└── Processor: Snapdragon XR2 Gen 1

Quest 3 Enhancements:
├── Resolution: 2064×2208 per eye (+30%)
├── Mixed Reality: Color passthrough
├── Hand Tracking: Improved accuracy
├── Memory: 8GB RAM
└── Processor: Snapdragon XR2 Gen 2 (+2.5x GPU)
```

### **Troubleshooting Comum**

```bash
Issues & Solutions:

1. Audio Desync:
   - Solution: Use uncompressed WAV files
   - Check: Audio format compatibility

2. Frame Drops:
   - Solution: Reduce concurrent 3D models
   - Check: Scene complexity under limits

3. Hand Tracking Inconsistent:
   - Solution: Improve lighting conditions
   - Check: Quest firmware updated

4. Board Loading Slow:
   - Solution: Pre-load next board
   - Check: Image resolution optimization

5. Guta Avatar Stutter:
   - Solution: Simplify animation complexity
   - Check: Rigging compatibility
```

---

## 🎯 DELIVERABLES FINAIS

### **Pacote de Entrega**

```bash
FIRJAN_Figmin_Package/
├── Experience/
│   ├── FIRJAN_Teaser.figminxr (arquivo principal)
│   ├── Share_Link.txt (URL público)
│   └── Installation_Guide.pdf
├── Assets/
│   ├── All_Boards_Optimized/
│   ├── 3D_Models_Used/
│   ├── Audio_Files/
│   └── Source_Files/
├── Documentation/
│   ├── User_Manual.pdf
│   ├── Technical_Specs.md
│   ├── Testing_Results.json
│   └── Feedback_Summary.md
└── Next_Steps/
    ├── Unity_Migration_Plan.md
    ├── Feature_Enhancements.md
    └── Cost_Analysis.xlsx
```

---

**🚀 Esta abordagem Figmin XR permite validar rapidamente o conceito FIRJAN com investimento mínimo, estabelecendo a base sólida para desenvolvimento posterior em Unity se aprovado pelos stakeholders.** 

---

## 🔧 ALTERNATIVA ROBUSTA: BLENDER → GLB → UNITY/WEBXR

### **Quando Usar Esta Abordagem:**
- ✅ Projeto aprovado para produção profissional
- ✅ Orçamento para desenvolvimento completo (R$ 45.000+)
- ✅ Necessidade de performance otimizada
- ✅ Deploy em múltiplas plataformas (Quest, Web, Vision Pro)

### **Vantagens Blender + GLB:**
- 🎯 **Controle total** sobre assets e qualidade
- 📦 **GLB = padrão indústria** para XR/WebXR
- ⚡ **Performance otimizada** para dispositivos mobile
- 🔄 **Compatibilidade universal** (Unity, Three.js, A-Frame, etc.)
- 💎 **Qualidade profissional** para cliente final

---

## 🎨 WORKFLOW BLENDER PARA FIRJAN

### **FASE 1: Preparação Assets Blender (2 dias)**

#### **Setup Projeto Blender**
```bash
# Configuração Projeto FIRJAN
Blender 4.0+ LTS
- Units: Metric (metros)
- Frame Rate: 60 fps
- Render Engine: Eevee (para preview rápido)
- Color Management: sRGB
```

#### **Organização Cena**
```
FIRJAN_Scene.blend
├── Collections/
│   ├── Boards/ (12 painéis interativos)
│   ├── Environment/ (espaço 3D)
│   ├── Props/ (elementos 3D)
│   ├── Lighting/ (iluminação otimizada)
│   └── Avatar_Guta/ (personagem guia)
├── Materials/
│   ├── Board_Materials/
│   ├── Environment_PBR/
│   └── Character_Materials/
└── Animations/
    ├── Board_Interactions/
    ├── Guta_Gestures/
    └── Transition_Effects/
```

#### **Criação dos 12 Boards**
```python
# Script Python para criar boards automaticamente
import bpy
import bmesh

def create_firjan_board(board_num, title, image_path):
    # Criar geometria do board
    bpy.ops.mesh.primitive_plane_add(size=2, location=(board_num*3, 0, 1.5))
    board = bpy.context.active_object
    board.name = f"Board_{board_num:02d}_{title}"
    
    # Material PBR otimizado
    mat = bpy.data.materials.new(f"Mat_Board_{board_num:02d}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    
    # Shader setup para XR
    bsdf = nodes["Principled BSDF"]
    bsdf.inputs[0].default_value = (1, 1, 1, 1)  # Base Color
    bsdf.inputs[7].default_value = 0.1  # Roughness para XR
    bsdf.inputs[12].default_value = 1.0  # Specular
    
    # Texture do board
    tex_image = nodes.new('ShaderNodeTexImage')
    tex_image.image = bpy.data.images.load(image_path)
    
    # Conectar texture ao material
    mat.node_tree.links.new(tex_image.outputs[0], bsdf.inputs[0])
    
    # Aplicar material
    board.data.materials.append(mat)
    
    return board

# Criar todos os 12 boards
boards_data = [
    (1, "Pergunta", "BOARD_01_pergunta_de_onde_vem.png"),
    (2, "Gutenberg", "BOARD_02_gutenberg_lettering.png"),
    (3, "Tipografia", "BOARD_03_tipografia_industria_grafica.png"),
    # ... continuar para todos os 12
]

for num, title, image in boards_data:
    create_firjan_board(num, title, f"/Assets/Boards/{image}")
```

### **FASE 2: Avatar Guta (1 dia)**

#### **Criação Personagem Simplificado**
```python
# Script para criar avatar Guta otimizado
def create_guta_avatar():
    # Base character (low-poly feminina)
    bpy.ops.mesh.primitive_uv_sphere_add(location=(0, -2, 0))
    head = bpy.context.active_object
    head.name = "Guta_Head"
    head.scale = (0.8, 0.8, 1.0)
    
    # Corpo simplificado
    bpy.ops.mesh.primitive_cylinder_add(location=(0, -2, -1.5))
    body = bpy.context.active_object
    body.name = "Guta_Body"
    body.scale = (0.6, 0.6, 1.5)
    
    # Material character
    char_mat = bpy.data.materials.new("Guta_Material")
    char_mat.use_nodes = True
    char_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.8, 0.6, 0.4, 1.0)
    
    # Aplicar material
    for obj in [head, body]:
        obj.data.materials.append(char_mat)
    
    # Animações básicas (gestos)
    create_guta_animations()

def create_guta_animations():
    # Gesture animations para Guta
    actions = ["Point_Board", "Welcome_Wave", "Explain_Gesture", "Goodbye_Wave"]
    
    for action_name in actions:
        action = bpy.data.actions.new(f"Guta_{action_name}")
        # Keyframes simples para gestos
        # ... (implementar animações básicas)
```

### **FASE 3: Otimização XR (1 dia)**

#### **LOD System (Level of Detail)**
```python
def create_lod_system():
    # LOD para performance em dispositivos mobile
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH' and "Board" in obj.name:
            # LOD 0: High quality (perto)
            lod0 = obj.copy()
            lod0.data = obj.data.copy()
            lod0.name = f"{obj.name}_LOD0"
            
            # LOD 1: Medium quality (médio)
            lod1 = obj.copy()
            lod1.data = obj.data.copy()
            lod1.name = f"{obj.name}_LOD1"
            
            # Aplicar decimation modifier
            decimate = lod1.modifiers.new("Decimate", "DECIMATE")
            decimate.ratio = 0.5  # 50% dos polígonos
            
            # LOD 2: Low quality (longe)
            lod2 = obj.copy()
            lod2.data = obj.data.copy()
            lod2.name = f"{obj.name}_LOD2"
            
            decimate2 = lod2.modifiers.new("Decimate", "DECIMATE")
            decimate2.ratio = 0.25  # 25% dos polígonos
```

#### **Texture Optimization**
```python
def optimize_textures():
    for image in bpy.data.images:
        if image.source == 'FILE':
            # Resize para XR (máximo 1024x1024)
            if image.size[0] > 1024 or image.size[1] > 1024:
                image.scale(1024, 1024)
            
            # Compressão para GLB
            image.file_format = 'PNG'
            image.compression = 15  # Compressão moderada
```

### **FASE 4: Export GLB Otimizado**

#### **Export Settings Perfeitos**
```python
# Script export GLB otimizado para XR
import bpy

def export_firjan_glb():
    # Configurações export para XR
    bpy.ops.export_scene.gltf(
        filepath="/Export/FIRJAN_XR_Experience.glb",
        
        # Format
        export_format='GLB',
        
        # Include
        use_selection=False,  # Exportar tudo
        use_visible=True,     # Apenas objetos visíveis
        use_renderable=True,  # Apenas renderizáveis
        use_active_collection=False,
        
        # Transform
        export_yup=True,      # Y-up para padrão glTF
        
        # Geometry  
        export_apply=True,         # Aplicar modifiers
        export_texcoords=True,     # UV coordinates
        export_normals=True,       # Normais para shading
        export_draco_mesh_compression_enable=True,  # Compressão Draco
        export_draco_mesh_compression_level=6,      # Nível médio
        
        # Materials
        export_materials='EXPORT',    # Exportar materiais
        export_image_format='AUTO',   # PNG/JPEG automático
        
        # Animation
        export_frame_range=True,      # Range de animação
        export_frame_step=1,          # Todos os frames
        export_force_sampling=True,   # Sampling forçado
        export_nla_strips=False,      # Sem NLA tracks
        
        # Compression & Optimization
        export_texture_dir="",        # Texturas embedded
        export_jpeg_quality=80,       # Qualidade JPEG
        
        # XR Specific
        export_cameras=False,         # Sem câmeras (headset usa própria)
        export_lights=True,           # Manter iluminação
    )
    
    print("✅ GLB exportado com otimizações XR!")

# Executar export
export_firjan_glb()
```

### **FASE 5: Deploy Unity/WebXR (2 dias)**

#### **Unity Import & Setup**
```csharp
// Unity script para carregar GLB FIRJAN
using UnityEngine;
using Siccity.GLTFUtility;

public class FIRJANExperienceLoader : MonoBehaviour 
{
    public string glbPath = "FIRJAN_XR_Experience.glb";
    
    void Start() 
    {
        StartCoroutine(LoadFIRJANExperience());
    }
    
    IEnumerator LoadFIRJANExperience() 
    {
        // Carregar GLB principal
        GameObject firjanScene = Importer.LoadFromFile(glbPath);
        
        // Setup específico FIRJAN
        SetupInteractiveBoards(firjanScene);
        SetupGutaAvatar(firjanScene);
        SetupXRInteractions(firjanScene);
        
        yield return null;
    }
    
    void SetupInteractiveBoards(GameObject scene) 
    {
        // Encontrar todos os boards
        foreach(Transform child in scene.transform) 
        {
            if(child.name.Contains("Board_")) 
            {
                // Adicionar interatividade
                var collider = child.gameObject.AddComponent<BoxCollider>();
                var interaction = child.gameObject.AddComponent<XRGrabInteractable>();
                
                // Audio clip para cada board
                var audioSource = child.gameObject.AddComponent<AudioSource>();
                audioSource.clip = GetBoardAudio(child.name);
            }
        }
    }
}
```

#### **WebXR Deploy (A-Frame)**
```html
<!-- WebXR version para browser -->
<!DOCTYPE html>
<html>
<head>
    <script src="https://aframe.io/releases/1.4.0/aframe.min.js"></script>
    <script src="https://cdn.jsdelivr.net/gh/donmccurdy/aframe-extras@v6.1.1/dist/aframe-extras.min.js"></script>
    <script src="https://unpkg.com/aframe-environment-component/dist/aframe-environment-component.min.js"></script>
</head>
<body>
    <a-scene background="color: #000000" embedded arjs="debugUIEnabled: false;">
        <!-- Carregar GLB FIRJAN -->
        <a-asset-item id="firjan-glb" src="./assets/FIRJAN_XR_Experience.glb"></a-asset-item>
        
        <!-- Cena principal -->
        <a-entity gltf-model="#firjan-glb" 
                  position="0 0 -5" 
                  scale="1 1 1"
                  animation-mixer="clip: *">
        </a-entity>
        
        <!-- Controles XR -->
        <a-entity id="rig" 
                  movement-controls="fly: false" 
                  position="0 1.6 3">
            <a-entity camera 
                      look-controls="pointerLockEnabled: true">
            </a-entity>
            
            <!-- Hand controls -->
            <a-entity laser-controls="hand: right" 
                      raycaster="objects: .interactive"></a-entity>
        </a-entity>
        
        <!-- Iluminação otimizada -->
        <a-light type="ambient" color="#404040" intensity="0.4"></a-light>
        <a-light type="directional" position="1 4 2" color="#ffffff" intensity="0.8"></a-light>
    </a-scene>
</body>
</html>
```

---

## 📊 COMPARAÇÃO: FIGMIN vs BLENDER+GLB

| Aspecto | Figmin XR | Blender → GLB → Unity |
|---------|-----------|----------------------|
| **Tempo** | 1 semana | 3-4 semanas |
| **Custo** | R$ 15.000 | R$ 45.000 |
| **Qualidade** | Protótipo | Produção profissional |
| **Controle** | Limitado | Total |
| **Compatibilidade** | Quest/Vision Pro | Universal |
| **Performance** | Boa | Otimizada |
| **Manutenção** | Dependente da plataforma | Código próprio |

---

## 🎯 RECOMENDAÇÃO FINAL

### **Para FIRJAN especificamente:**

**FASE 1:** Figmin XR (1 semana, R$ 15.000)
- Validação rápida com stakeholders
- Teste conceito narrativo
- Feedback para iterações

**FASE 2:** Blender → GLB → Unity (3 semanas, R$ 45.000)  
- Produção profissional
- Deploy multiplataforma
- Performance otimizada para evento

**Total: R$ 60.000 | 4 semanas**

✅ **Melhor dos dois mundos: validação rápida + qualidade profissional** 