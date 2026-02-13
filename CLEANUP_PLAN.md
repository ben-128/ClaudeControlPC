# Cleanup Analysis - Claude PC Control

## Fichiers à SUPPRIMER (obsolètes/redondants)

### Scripts Python obsolètes:
- ❌ **`auto_vision.py`** (9.7K) - Détection couleur/OCR, remplacé par grid system + OmniParser
- ❌ **`smart_vision.py`** (5.7K) - Nécessite références manuelles, complexe et peu utilisé
- ❌ **`capture_reference.py`** (3.0K) - Pour smart_vision, inutile si smart_vision supprimé
- ❌ **`screen_info.py`** (2.7K) - Fonctionnalités déjà dans claude_vision + grid
- ❌ **`screenshot.py`** (1.3K) - Basique, remplacé par claude_vision.py
- ⚠️ **`demo.py`** (3.8K) - Utile pour tests, mais peut être supprimé si pas utilisé

### Documentation redondante:
- ❌ **`AUTO_README.md`** (3.3K) - Décrit smart_vision (à supprimer)
- ❌ **`ZERO_REF_README.md`** (3.4K) - Décrit auto_vision (à supprimer)
- ✅ **`README.md`** (5.0K) - À GARDER et mettre à jour
- ✅ **`FILES_OVERVIEW.md`** (3.5K) - À GARDER (nouveau, utile)
- ✅ **`OMNIPARSER_INTEGRATION.md`** (4.3K) - À GARDER (plan futur)

## Fichiers à GARDER (essentiels)

### Core workflow:
- ✅ **`claude_vision.py`** (2.1K) - Screenshot + workflow principal
- ✅ **`grid_click.py`** (2.8K) - Solution qui fonctionne!
- ✅ **`grid_overlay.py`** (4.2K) - Affichage grille
- ✅ **`omni_simple.py`** (4.6K) - Future solution OmniParser

### Input control (essentiels):
- ✅ **`mouse_control.py`** (3.2K)
- ✅ **`keyboard_control.py`** (2.1K)

### Setup:
- ✅ **`setup.py`** (1.1K)

## Économie de nettoyage

**À supprimer:** ~33.7K de code obsolète
**À garder:** ~20.1K de code actif

## Actions recommandées

1. **Supprimer** scripts obsolètes (auto_vision, smart_vision, etc.)
2. **Supprimer** documentation obsolète (AUTO_README, ZERO_REF_README)
3. **Mettre à jour** README.md principal avec workflow grid system
4. **Créer** CHANGELOG.md pour tracer l'évolution
5. **Supprimer** demo.py (optionnel - garder si utile pour tests)

## Commande de nettoyage

```bash
cd "C:\Perso\Claude_ControlPc"

# Supprimer scripts obsolètes
rm auto_vision.py smart_vision.py capture_reference.py screen_info.py screenshot.py demo.py

# Supprimer doc obsolète
rm AUTO_README.md ZERO_REF_README.md

# Total: 9 fichiers supprimés (~34K)
```
