# Installation Guide - Claude PC Control

## Requirements

- **Python 3.14** (ou 3.12-3.13)
- **Windows 10/11**
- **~500MB** d'espace disque (PyTorch + dépendances)
- **Git** (pour cloner le repo)

## Installation Complète

### 1. Cloner le Repository

```bash
git clone https://github.com/ben-128/ClaudeControlPC.git
cd ClaudeControlPC
```

### 2. Dépendances de Base (Grid System)

**Minimum fonctionnel** pour le grid system:

```bash
pip install pyautogui pillow opencv-python numpy
```

**Packages installés:**
- `pyautogui==0.9.54` - Contrôle souris/clavier + screenshots
- `pillow==12.1.1` - Traitement d'images
- `opencv-python==4.13.0.92` - Vision par ordinateur
- `numpy==2.4.2` - Calculs numériques

### 3. Dépendances Complètes (OmniParser)

**Pour l'intégration OmniParser** (optionnel - en développement):

```bash
pip install torch torchvision transformers ultralytics supervision \
            typing_extensions pyyaml tqdm matplotlib seaborn pandas requests \
            sympy filelock fsspec networkx scipy psutil \
            huggingface-hub safetensors regex tokenizers einops timm accelerate
```

**Packages principaux:**

| Package | Version | Taille | Usage |
|---------|---------|--------|-------|
| `torch` | 2.10.0 | ~114MB | Deep learning framework |
| `torchvision` | 0.25.0 | ~4.3MB | Vision models |
| `transformers` | 5.1.0 | ~10MB | Hugging Face models |
| `ultralytics` | 8.4.14 | ~1.2MB | YOLOv8 |
| `supervision` | 0.27.0 | ~217KB | Vision utilities |

**Dépendances PyTorch:**
- `typing_extensions==4.15.0`
- `sympy==1.14.0`
- `filelock==3.21.2`
- `fsspec==2026.2.0`
- `networkx==3.6.1`

**Dépendances scientifiques:**
- `scipy==1.17.0` (~37MB)
- `matplotlib==3.10.8` (~8.3MB)
- `pandas==3.0.0` (~9.9MB)
- `seaborn==0.13.2`

**Dépendances Hugging Face:**
- `huggingface-hub==1.4.1`
- `safetensors==0.7.0`
- `tokenizers==0.22.2` (~2.7MB)
- `regex==2026.1.15`

**Utilities:**
- `tqdm==4.67.3` - Progress bars
- `pyyaml==6.0.3` - Config files
- `requests==2.32.5` - HTTP
- `psutil==7.2.2` - System info

**ML/AI:**
- `timm==1.0.24` - Vision models
- `einops==0.8.2` - Tensor operations
- `accelerate==1.12.0` - Training acceleration

### 4. Installation Automatique

```bash
# Version de base (grid system)
py -3 setup.py

# Version complète (avec OmniParser)
py -3 -m pip install -r OmniParser/requirements_py314.txt
py -3 -m pip install typing_extensions pyyaml tqdm matplotlib seaborn pandas requests \
                      sympy filelock fsspec networkx scipy psutil \
                      huggingface-hub safetensors regex tokenizers
```

## Structure d'Installation

```
Claude_ControlPc/
├── Python packages (site-packages)
│   ├── pyautogui/           6.8MB
│   ├── torch/             ~120MB
│   ├── torchvision/        ~15MB
│   ├── transformers/       ~35MB
│   ├── ultralytics/        ~10MB
│   ├── opencv/             ~45MB
│   ├── scipy/              ~40MB
│   ├── matplotlib/         ~25MB
│   ├── pandas/             ~35MB
│   └── (autres)            ~50MB
│
├── OmniParser/            (cloné localement)
│   └── weights/           (téléchargés au premier usage)
│       ├── yolov8n.pt      6.2MB
│       └── (futurs modèles UI fine-tuned)
│
└── Scripts locaux          ~20KB
```

**Total espace disque:** ~400-500MB

## Vérification de l'Installation

### Test de Base

```bash
# Test PyAutoGUI
py -3 -c "import pyautogui; print(f'Screen: {pyautogui.size()}')"

# Test OpenCV
py -3 -c "import cv2; print(f'OpenCV: {cv2.__version__}')"

# Test grid system
py -3 grid_click.py pos
```

### Test YOLO (OmniParser)

```bash
# Test import
py -3 -c "from ultralytics import YOLO; print('YOLO OK')"

# Test détection
py -3 omni_simple.py detect temp_screen.png
```

## Problèmes Courants

### Python 3.14 trop récent

**Symptôme:** Erreurs "no matching distribution found"

**Solution:** Certains packages (paddlepaddle, easyocr) ne supportent pas encore Python 3.14. Utilisez Python 3.11-3.12, ou utilisez uniquement le grid system (pas d'OmniParser complet).

### Erreur "No module named 'typing_extensions'"

**Solution:**
```bash
pip install typing_extensions
```

### PyTorch installation lente

**Normal.** PyTorch est ~114MB et peut prendre 2-5 minutes à télécharger/installer.

### YOLO détecte mal les UI

**Normal.** Le modèle générique (`yolov8n.pt`) est entraîné sur COCO dataset (objets du monde réel), pas sur les UI. Le modèle fine-tuned d'OmniParser pour UI n'est pas encore disponible pour Python 3.14.

**Solution actuelle:** Utiliser le **grid system** qui fonctionne parfaitement.

## Recommandations

### Installation Minimale (Recommandé)

Pour commencer rapidement avec le grid system:

```bash
pip install pyautogui pillow opencv-python numpy
```

**Avantages:**
- ✅ Installation rapide (~30MB)
- ✅ Fonctionne immédiatement
- ✅ Pas de modèles ML complexes
- ✅ Précision excellente avec grille 100x100px

### Installation Complète (Avancé)

Pour tester OmniParser et futures intégrations ML:

```bash
# Toutes les dépendances
pip install torch torchvision transformers ultralytics supervision \
            typing_extensions pyyaml tqdm matplotlib seaborn pandas \
            sympy filelock fsspec networkx scipy psutil \
            huggingface-hub safetensors regex tokenizers einops timm accelerate
```

**Avantages:**
- ✅ Prêt pour futurs modèles UI fine-tuned
- ✅ Support complet OmniParser
- ✅ Possibilités de ML/AI avancées

**Inconvénients:**
- ❌ ~400-500MB d'espace
- ❌ Installation ~10-15 minutes
- ❌ Modèles UI pas encore disponibles Python 3.14

## Mises à Jour

```bash
# Mise à jour pip
py -3 -m pip install --upgrade pip

# Mise à jour packages
pip install --upgrade pyautogui pillow opencv-python numpy

# Mise à jour PyTorch (si installé)
pip install --upgrade torch torchvision
```

## Désinstallation

```bash
# Supprimer packages ML lourds
pip uninstall torch torchvision transformers ultralytics

# Supprimer tout
pip uninstall pyautogui pillow opencv-python numpy scipy matplotlib pandas
```

## Notes de Version

- **v1.0** - PyAutoGUI + scripts basiques
- **v2.0** - Grid system + nettoyage
- **v2.1** - OmniParser integration (Python 3.14 compatible)
- **v3.0** (futur) - Modèles UI fine-tuned disponibles

## Support

- **Repo GitHub:** https://github.com/ben-128/ClaudeControlPC
- **Issues:** https://github.com/ben-128/ClaudeControlPC/issues
- **Wiki:** [INSTALLATION.md](./INSTALLATION.md)
