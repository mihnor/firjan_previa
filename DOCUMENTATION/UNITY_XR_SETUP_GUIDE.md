# 🎮 GUIA TÉCNICO: Unity XR Setup para Meta Quest 3
**Projeto FIRJAN - Experiência "De Onde Vem o Livro que Você Lê?"**

## 🛠️ PRÉ-REQUISITOS

### Software Necessário
```bash
Unity Hub 3.8+
Unity 2022.3.45f1 LTS (ou superior)
Visual Studio 2022 / VS Code
Android SDK API Level 29+
Meta Quest Developer Hub
Git LFS (para assets grandes)
```

### Hardware Mínimo
```
PC Windows 11 / macOS 12+
RAM: 16GB+ (32GB recomendado)
GPU: RTX 3060+ / AMD 6600 XT+
USB 3.0+ para debug Meta Quest
Meta Quest 2/3/Pro
```

---

## 🚀 SETUP INICIAL DO PROJETO

### 1. Criação do Projeto Unity

```bash
# Via Unity Hub
1. New Project → 3D (URP)
2. Project Name: "FIRJAN_XR_Teaser"
3. Location: C:/Projects/FIRJAN_XR/
4. Unity Version: 2022.3.45f1 LTS
```

### 2. Configuração Build Settings

```csharp
// File → Build Settings
Platform: Android
Architecture: ARM64
API Level: 29 (Android 10.0)
Scripting Backend: IL2CPP
Target Device Family: Quest
```

### 3. Player Settings Essenciais

```csharp
// Edit → Project Settings → Player
Company Name: "MEMOrIA XR"
Product Name: "FIRJAN Teaser - De Onde Vem o Livro"
Package Name: com.memoriaxr.firjan.teaser
Minimum API Level: Android 10.0 (API level 29)
Target API Level: Automatic (highest installed)

// XR Settings
Virtual Reality Supported: ✓
Stereo Rendering Mode: Single Pass Instanced
```

---

## 📦 PACOTES XR ESSENCIAIS

### 1. Instalação via Package Manager

```json
{
  "dependencies": {
    "com.unity.xr.interaction.toolkit": "2.5.4",
    "com.unity.xr.openxr": "1.9.1",
    "com.unity.xr.management": "4.4.0",
    "com.unity.xr.hands": "1.3.0",
    "com.unity.inputsystem": "1.7.0",
    "com.unity.render-pipelines.universal": "14.0.10"
  }
}
```

### 2. Meta XR SDK Integration

```bash
# Via Unity Asset Store ou GitHub
Meta XR All-in-One SDK v66+
├── Meta XR Core SDK
├── Meta XR Platform SDK  
├── Meta XR Interaction SDK
└── Meta XR Audio SDK
```

### 3. OpenXR Feature Groups

```csharp
// Edit → Project Settings → XR Plug-in Management → OpenXR
Feature Groups:
├── ✓ Meta Quest Support
├── ✓ Hand Tracking Subsystem
├── ✓ OpenXR Runtime Debugger
└── ✓ Oculus Android Provider

Interaction Profiles:
├── ✓ Oculus Touch Controller Profile
├── ✓ Hand Interaction Profile
└── ✓ Eye Gaze Interaction Profile
```

---

## 🏗️ ESTRUTURA DO PROJETO

### Hierarquia de Pastas

```
Assets/
├── _FIRJAN/
│   ├── Scenes/
│   │   ├── MainExperience.unity
│   │   └── TestingScene.unity
│   ├── Scripts/
│   │   ├── Core/
│   │   ├── UI/
│   │   ├── Audio/
│   │   └── Analytics/
│   ├── Prefabs/
│   │   ├── XR_Rig/
│   │   ├── Boards/
│   │   ├── UI/
│   │   └── Audio/
│   ├── Materials/
│   ├── Textures/
│   │   ├── Boards/ (1-12 folders)
│   │   └── UI/
│   ├── Audio/
│   │   ├── Voiceover/
│   │   ├── SFX/
│   │   └── Music/
│   └── Models/
│       ├── Gutenberg/
│       ├── Typography/
│       └── Books/
└── Plugins/
    └── Meta/
```

---

## 🎮 SETUP XR RIG BÁSICO

### 1. XR Origin Configuration

```csharp
// Hierarchy Setup
XR Origin (XR Rig)
├── Camera Offset
│   ├── Main Camera (XR Camera)
│   ├── LeftHand Controller
│   ├── RightHand Controller
│   └── XR Hands (Hand Tracking)
├── Locomotion System
└── XR Interaction Manager
```

### 2. Script: XR Manager Core

```csharp
using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;
using Unity.XR.CoreUtils;

public class FIRJANXRManager : MonoBehaviour
{
    [Header("XR Components")]
    public XROrigin xrOrigin;
    public XRInteractionManager interactionManager;
    
    [Header("Experience Settings")]
    public float experienceDuration = 300f; // 5 minutes
    public bool enableHandTracking = true;
    public bool enableEyeTracking = false;
    
    void Start()
    {
        InitializeXRExperience();
        SetupPerformanceSettings();
    }
    
    void InitializeXRExperience()
    {
        // Configure XR settings for optimal Quest performance
        XRSettings.eyeTextureResolutionScale = 1.0f;
        Application.targetFrameRate = 72; // Quest 2 native
        
        if (enableHandTracking)
            EnableHandTracking();
    }
    
    void SetupPerformanceSettings()
    {
        // Optimize for Quest 2/3 performance
        QualitySettings.vSyncCount = 0;
        QualitySettings.renderPipeline = Resources.Load("URP-Performant");
    }
    
    void EnableHandTracking()
    {
        var handTrackingManager = FindObjectOfType<XRHandTrackingManager>();
        if (handTrackingManager != null)
            handTrackingManager.enabled = true;
    }
}
```

---

## 🎨 SISTEMA DE BOARDS INTERATIVOS

### 1. Board Controller Script

```csharp
using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;

public class InteractiveBoard : XRGrabInteractable
{
    [Header("Board Settings")]
    public int boardNumber;
    public string boardTitle;
    public Texture2D boardTexture;
    public AudioClip boardNarration;
    
    [Header("Animation")]
    public float hoverScale = 1.1f;
    public float animationDuration = 0.3f;
    
    private Vector3 originalScale;
    private AudioSource audioSource;
    private MeshRenderer meshRenderer;
    
    protected override void Awake()
    {
        base.Awake();
        originalScale = transform.localScale;
        audioSource = GetComponent<AudioSource>();
        meshRenderer = GetComponent<MeshRenderer>();
        
        // Setup board texture
        if (boardTexture != null)
            meshRenderer.material.mainTexture = boardTexture;
    }
    
    protected override void OnHoverEntered(HoverEnterEventArgs args)
    {
        base.OnHoverEntered(args);
        AnimateScale(originalScale * hoverScale);
        PlayHoverSound();
    }
    
    protected override void OnHoverExited(HoverExitEventArgs args)
    {
        base.OnHoverExited(args);
        AnimateScale(originalScale);
    }
    
    protected override void OnSelectEntered(SelectEnterEventArgs args)
    {
        base.OnSelectEntered(args);
        PlayBoardNarration();
        FIRJANAnalytics.TrackBoardInteraction(boardNumber);
    }
    
    void AnimateScale(Vector3 targetScale)
    {
        LeanTween.scale(gameObject, targetScale, animationDuration)
                 .setEaseOutBack();
    }
    
    void PlayBoardNarration()
    {
        if (boardNarration != null && audioSource != null)
        {
            audioSource.clip = boardNarration;
            audioSource.Play();
        }
    }
    
    void PlayHoverSound()
    {
        // Play subtle hover sound
        FIRJANAudioManager.Instance.PlayHoverSFX();
    }
}
```

### 2. Board Sequence Manager

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BoardSequenceManager : MonoBehaviour
{
    [Header("Board Sequence")]
    public List<InteractiveBoard> boards = new List<InteractiveBoard>();
    public float boardSpacing = 2.0f;
    public Vector3 startPosition = Vector3.zero;
    
    [Header("Guta Avatar")]
    public GutaAvatarController gutaController;
    
    private int currentBoardIndex = 0;
    private bool experienceStarted = false;
    
    void Start()
    {
        SetupBoardPositions();
        ShowWelcomeBoard();
    }
    
    void SetupBoardPositions()
    {
        for (int i = 0; i < boards.Count; i++)
        {
            Vector3 position = startPosition + (Vector3.right * boardSpacing * i);
            boards[i].transform.position = position;
            
            // Hide all boards except first
            if (i > 0)
                boards[i].gameObject.SetActive(false);
        }
    }
    
    void ShowWelcomeBoard()
    {
        if (boards.Count > 0)
        {
            boards[0].gameObject.SetActive(true);
            gutaController.PlayWelcomeSequence();
        }
    }
    
    public void AdvanceToNextBoard()
    {
        if (currentBoardIndex < boards.Count - 1)
        {
            // Hide current board
            boards[currentBoardIndex].gameObject.SetActive(false);
            
            // Show next board
            currentBoardIndex++;
            boards[currentBoardIndex].gameObject.SetActive(true);
            
            // Update Guta narrative
            gutaController.PlayBoardNarrative(currentBoardIndex);
        }
        else
        {
            // Experience completed
            CompleteExperience();
        }
    }
    
    void CompleteExperience()
    {
        gutaController.PlayClosingSequence();
        FIRJANAnalytics.TrackExperienceCompletion();
    }
}
```

---

## 🎤 SISTEMA DE ÁUDIO ESPACIALIZADO

### 1. Audio Manager

```csharp
using UnityEngine;
using UnityEngine.Audio;

public class FIRJANAudioManager : MonoBehaviour
{
    public static FIRJANAudioManager Instance;
    
    [Header("Audio Mixers")]
    public AudioMixerGroup voiceoverMixer;
    public AudioMixerGroup sfxMixer;
    public AudioMixerGroup musicMixer;
    
    [Header("3D Audio Settings")]
    public AnimationCurve spatialBlend = AnimationCurve.Linear(0, 0, 1, 1);
    public float maxDistance = 20f;
    
    void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject);
        }
        else
            Destroy(gameObject);
    }
    
    public AudioSource Create3DAudioSource(Transform parent, AudioClip clip)
    {
        GameObject audioObj = new GameObject("3D Audio Source");
        audioObj.transform.SetParent(parent);
        audioObj.transform.localPosition = Vector3.zero;
        
        AudioSource source = audioObj.AddComponent<AudioSource>();
        source.clip = clip;
        source.spatialBlend = 1.0f; // Full 3D
        source.rolloffMode = AudioRolloffMode.Logarithmic;
        source.maxDistance = maxDistance;
        source.outputAudioMixerGroup = voiceoverMixer;
        
        return source;
    }
    
    public void PlayHoverSFX()
    {
        // Play UI hover sound
    }
}
```

---

## 📊 SISTEMA DE ANALYTICS

### 1. Analytics Tracker

```csharp
using UnityEngine;
using System.Collections.Generic;

public class FIRJANAnalytics : MonoBehaviour
{
    private static Dictionary<string, object> sessionData = new Dictionary<string, object>();
    private static float sessionStartTime;
    
    void Start()
    {
        sessionStartTime = Time.time;
        TrackSessionStart();
    }
    
    public static void TrackSessionStart()
    {
        sessionData["session_start"] = System.DateTime.Now.ToString();
        sessionData["device_model"] = SystemInfo.deviceModel;
        sessionData["unity_version"] = Application.unityVersion;
    }
    
    public static void TrackBoardInteraction(int boardNumber)
    {
        string key = $"board_{boardNumber}_interactions";
        if (sessionData.ContainsKey(key))
            sessionData[key] = (int)sessionData[key] + 1;
        else
            sessionData[key] = 1;
            
        Debug.Log($"Board {boardNumber} interaction tracked");
    }
    
    public static void TrackExperienceCompletion()
    {
        float sessionDuration = Time.time - sessionStartTime;
        sessionData["session_duration"] = sessionDuration;
        sessionData["experience_completed"] = true;
        
        // Send data to analytics service
        SendAnalyticsData();
    }
    
    static void SendAnalyticsData()
    {
        // Implementation for sending to analytics service
        string jsonData = JsonUtility.ToJson(sessionData);
        Debug.Log($"Analytics Data: {jsonData}");
    }
}
```

---

## ⚡ OTIMIZAÇÃO DE PERFORMANCE

### 1. LOD System Setup

```csharp
public class FIRJANLODManager : MonoBehaviour
{
    [Header("LOD Settings")]
    public float[] lodDistances = { 5f, 10f, 20f };
    public float cullDistance = 30f;
    
    void Start()
    {
        SetupLODGroups();
        ConfigureOcclusionCulling();
    }
    
    void SetupLODGroups()
    {
        // Setup LOD for all 3D models
        GameObject[] models = GameObject.FindGameObjectsWithTag("3DModel");
        
        foreach (GameObject model in models)
        {
            LODGroup lodGroup = model.GetComponent<LODGroup>();
            if (lodGroup == null)
                lodGroup = model.AddComponent<LODGroup>();
                
            // Configure LOD levels
            LOD[] lods = new LOD[3];
            // Implementation for different LOD levels
        }
    }
    
    void ConfigureOcclusionCulling()
    {
        // Enable occlusion culling for performance
        Camera.main.useOcclusionCulling = true;
    }
}
```

### 2. URP Performance Settings

```csharp
// Create URP Asset for Quest optimization
public class QuestURPSettings : ScriptableObject
{
    public static void ApplyQuestOptimizations()
    {
        var urpAsset = GraphicsSettings.renderPipelineAsset as UniversalRenderPipelineAsset;
        
        if (urpAsset != null)
        {
            // Optimize for Quest 2/3
            urpAsset.shadowDistance = 15f;
            urpAsset.shadowCascadeCount = 2;
            urpAsset.msaaSampleCount = 4;
            urpAsset.renderScale = 1.0f;
        }
    }
}
```

---

## 🔧 BUILD & DEPLOYMENT

### 1. Build Configuration

```csharp
// Build script for automation
public class FIRJANBuildPipeline
{
    [MenuItem("FIRJAN/Build for Quest")]
    static void BuildForQuest()
    {
        // Set build settings
        EditorUserBuildSettings.buildAppBundle = false;
        EditorUserBuildSettings.androidBuildSystem = AndroidBuildSystem.Gradle;
        
        BuildPlayerOptions buildPlayerOptions = new BuildPlayerOptions();
        buildPlayerOptions.scenes = new[] { "Assets/_FIRJAN/Scenes/MainExperience.unity" };
        buildPlayerOptions.locationPathName = "Builds/FIRJAN_Teaser.apk";
        buildPlayerOptions.target = BuildTarget.Android;
        buildPlayerOptions.options = BuildOptions.None;
        
        BuildPipeline.BuildPlayer(buildPlayerOptions);
    }
}
```

### 2. Deploy to Quest

```bash
# Via ADB (Android Debug Bridge)
adb devices
adb install -r "Builds/FIRJAN_Teaser.apk"

# Via Meta Quest Developer Hub
# 1. Connect Quest via USB
# 2. Enable Developer Mode
# 3. Use MQDH Build & Deploy
```

---

## 📋 CHECKLIST FINAL

### ✅ **Pré-Produção**
- [ ] Projeto Unity criado e configurado
- [ ] Pacotes XR instalados e testados
- [ ] Assets visuais organizados e otimizados
- [ ] Sistema de áudio implementado

### ✅ **Desenvolvimento**
- [ ] XR Rig configurado para Quest 2/3
- [ ] Sistema de boards interativos
- [ ] Navegação por gestos/gaze
- [ ] Analytics implementado

### ✅ **Testing**
- [ ] Testes em Quest 2 (performance baseline)
- [ ] Testes em Quest 3 (features avançadas)
- [ ] Validação UX com stakeholders
- [ ] Otimização performance final

### ✅ **Deploy**
- [ ] Build APK otimizado
- [ ] Instalação e teste em dispositivos
- [ ] Documentação técnica
- [ ] Handoff para cliente

---

**🎯 Este guia garante uma implementação técnica robusta e otimizada para a experiência XR da FIRJAN, maximizando performance e engajamento no Meta Quest 3.** 