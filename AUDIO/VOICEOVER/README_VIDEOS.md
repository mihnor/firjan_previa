# FIRJAN XR - Vídeos de Voiceover

## Vídeos Gerados

Os seguintes vídeos foram gerados a partir dos arquivos de áudio para uso no Figmin XR:

### 📹 Arquivos de Vídeo (.mp4)
1. **ElevenLabs_2025-07-04T10_50_20__s50_v3.mp4** - 3.4MB
2. **ElevenLabs_2025-07-04T10_53_15_James - Husky & Engaging_pvc_sp100_s50_sb50_se10_b_e2.mp4** - 3.8MB
3. **FIRJAN_tour_virtual_guta_voiceover.mp4** - 4.3MB

### 🎵 Arquivos de Áudio Originais (.mp3)
1. **ElevenLabs_2025-07-04T10_50_20__s50_v3.mp3** - 2.1MB
2. **ElevenLabs_2025-07-04T10_53_15_James - Husky & Engaging_pvc_sp100_s50_sb50_se10_b_e2.mp3** - 2.5MB
3. **FIRJAN_tour_virtual_guta_voiceover.mp3** - 3.8MB

## 📝 Especificações dos Vídeos

- **Resolução**: 1920x1080 (Full HD)
- **Formato**: MP4 (H.264)
- **Áudio**: AAC, 192kbps
- **Fundo**: Preto sólido (logo do Firjan não encontrado)
- **Duração**: Mesmo tempo que os arquivos de áudio originais
- **Compatibilidade**: YouTube, Figmin XR, navegadores web

## 🚀 Próximos Passos

### 1. Upload para YouTube
1. Acesse o [YouTube Studio](https://studio.youtube.com/)
2. Clique em "CREATE" > "Upload videos"
3. Faça upload dos 3 vídeos .mp4 da pasta `videos/`
4. Configure as seguintes opções:
   - **Visibilidade**: Não listado (ou público se preferir)
   - **Título**: Use nomes descritivos (ex: "FIRJAN XR - Voiceover Guta")
   - **Descrição**: Adicione informações sobre o projeto Firjan XR
   - **Categoria**: Educação ou Ciência e Tecnologia

### 2. Copiar URLs dos Vídeos
Após o upload, copie os URLs dos vídeos do YouTube no formato:
```
https://www.youtube.com/watch?v=VIDEO_ID
```

### 3. Atualizar figmin_urls.json
No arquivo `FIRJAN_XR_ASSETS/figmin_urls.json`, atualize as URLs dos vídeos:

```json
{
  "voiceover_videos": {
    "elevenlabs_v3": "https://www.youtube.com/watch?v=YOUR_VIDEO_ID_1",
    "elevenlabs_james": "https://www.youtube.com/watch?v=YOUR_VIDEO_ID_2",
    "guta_voiceover": "https://www.youtube.com/watch?v=YOUR_VIDEO_ID_3"
  }
}
```

### 4. Testar no Figmin XR
1. Acesse o Figmin XR com as novas URLs
2. Teste a reprodução dos vídeos
3. Verifique se o áudio está sincronizado
4. Confirme se os vídeos carregam corretamente

## 🛠️ Regenerar Vídeos

Para regenerar os vídeos (caso necessário):

```bash
cd FIRJAN_XR_ASSETS/AUDIO/VOICEOVER
./generate_videos.sh
```

## 📋 Estrutura de Arquivos

```
VOICEOVER/
├── videos/                                     # Vídeos gerados
│   ├── ElevenLabs_2025-07-04T10_50_20__s50_v3.mp4
│   ├── ElevenLabs_2025-07-04T10_53_15_James...mp4
│   └── FIRJAN_tour_virtual_guta_voiceover.mp4
├── ElevenLabs_2025-07-04T10_50_20__s50_v3.mp3     # Áudio original
├── ElevenLabs_2025-07-04T10_53_15_James...mp3     # Áudio original
├── FIRJAN_tour_virtual_guta_voiceover.mp3          # Áudio original
├── generate_videos.sh                          # Script de geração
└── README_VIDEOS.md                           # Este arquivo
```

## 🔧 Requisitos Técnicos

- **ffmpeg**: Para conversão de áudio para vídeo
- **Sistema**: macOS, Linux ou Windows
- **Conexão**: Internet para upload no YouTube

## 📞 Suporte

Se houver problemas com os vídeos ou o upload:

1. Verifique se os arquivos .mp4 estão reproduzindo corretamente
2. Confirme se as URLs do YouTube estão corretas
3. Teste a integração no Figmin XR
4. Verifique a configuração do figmin_urls.json

---

**Status**: ✅ Vídeos gerados com sucesso
**Data**: 04/07/2025
**Formato**: MP4 (H.264) - 1920x1080
**Pronto para**: YouTube upload e Figmin XR 