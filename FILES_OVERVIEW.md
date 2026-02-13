# Claude PC Control - Files Overview

## Core Scripts (ACTIFS)

### Vision & Detection
- **`claude_vision.py`** ⭐ - Screenshot + Read workflow (fichier temp unique)
- **`auto_vision.py`** - Détection automatique (couleur, OCR, heuristiques)
- **`smart_vision.py`** - Vision avec références d'images
- **`omni_simple.py`** 🆕 - Wrapper OmniParser simplifié (YOLO)

### Input Control
- **`mouse_control.py`** - Contrôle souris (move, click, drag, scroll)
- **`keyboard_control.py`** - Contrôle clavier (type, press, hotkey)

### Grid System
- **`grid_overlay.py`** - Affiche grille numérotée sur l'écran
- **`grid_click.py`** ⭐ - Click par coordonnées de grille (résout problème spatial!)

### Utilities
- **`screen_info.py`** - Infos écran (size, pixel color, find image)
- **`screenshot.py`** - Capture d'écran basique
- **`capture_reference.py`** - Capture références pour smart_vision
- **`setup.py`** - Installation dépendances

### Demo
- **`demo.py`** - Démonstration des fonctionnalités

## Documentation

- **`README.md`** - Documentation principale
- **`AUTO_README.md`** - Doc vision avec références
- **`ZERO_REF_README.md`** - Doc vision sans références
- **`OMNIPARSER_INTEGRATION.md`** 🆕 - Plan intégration OmniParser
- **`FILES_OVERVIEW.md`** - Ce fichier

## OmniParser

- **`OmniParser/`** - Repo GitHub Microsoft (version simplifiée)
- **`OmniParser/requirements_py314.txt`** 🆕 - Requirements compatibles Python 3.14

## Fichiers temporaires

- **`temp_screen.png`** - Screenshot temporaire unique (réutilisé)
- **`.gitignore`** - Exclut screenshots et cache

## Obsolète/Supprimé ❌

- ~~`test_screenshot.png`~~ (supprimé)
- ~~`unity_initial.png`~~ (supprimé)
- ~~`unity_check.png`~~ (supprimé)
- ~~`after_play.png`~~ (supprimé)
- ~~`menu_screen.png`~~ (supprimé)
- ~~`demo_screenshot.png`~~ (supprimé)

## Workflow Recommandé

### Option 1: Grid System (MEILLEUR pour Claude)
```bash
# 1. Capture
py claude_vision.py capture

# 2. Claude analyse et identifie cellule grille (ex: 4,2)
# 3. Click précis
py grid_click.py click 4 2
```

### Option 2: OmniParser (FUTUR - quand modèle UI fine-tuné disponible)
```bash
# 1. Detect UI elements
py omni_simple.py detect temp_screen.png

# 2. Annotate avec numéros
py omni_simple.py annotate temp_screen.png

# 3. Claude lit image annotée et dit "click #5"
# 4. Click précis
py omni_simple.py click temp_screen.png 5
```

### Option 3: Auto Vision (Sans références)
```bash
# Unity Play button
py auto_vision.py click unity_play

# Boutons par couleur
py auto_vision.py color blue
```

## Historique des améliorations

1. **v1**: Screenshots multiples sur disque ❌ (lent, pollution)
2. **v2**: `temp_screen.png` unique ✓ (plus rapide)
3. **v3**: Auto-détection (OpenCV, OCR) ⚠️ (imprécis)
4. **v4**: Grid system ✅ (résout problème spatial de Claude)
5. **v5**: OmniParser integration 🚧 (en cours - Python 3.14 compatibility)

## Problèmes résolus

✅ **Pollution disque** - Un seul fichier temp réutilisé
✅ **Mauvaise estimation spatiale** - Grid system + feedback utilisateur
✅ **Lenteur** - Pas de Read systématique, JSON parsing direct
⏳ **Précision absolue** - En cours avec OmniParser

## État actuel

- **Fonctionnel**: Grid system fonctionne bien!
- **En test**: OmniParser wrapper simplifié
- **Limitation**: Modèle YOLO générique, pas fine-tuned pour UI (à venir)
