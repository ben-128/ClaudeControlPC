# Système de Vision Automatique

## Concept

**Tout se passe en mémoire** - pas de fichiers screenshots créés sur le disque.
Le script retourne du JSON que Claude peut interpréter directement.

## Workflow

### 1. Capturer des références (une seule fois par élément)

```bash
# Méthode interactive (précise)
py -3 capture_reference.py unity_play_button

# Méthode rapide (carré autour de la souris)
py -3 capture_reference.py menu_button quick 80
```

Ceci crée `references/unity_play_button.png` - une petite image de l'élément.

### 2. Utiliser la vision automatique

```bash
# Trouver et cliquer automatiquement
py -3 smart_vision.py find references/unity_play_button.png

# Trouver sans cliquer (juste localiser)
py -3 smart_vision.py find references/button.png 0.8 no

# Trouver toutes les instances
py -3 smart_vision.py findall references/icon.png

# Attendre qu'un élément apparaisse (max 10s)
py -3 smart_vision.py wait references/menu.png 10

# Obtenir infos écran (mouse position, screen size)
py -3 smart_vision.py info

# Analyser une région spécifique
py -3 smart_vision.py region 100 100 200 150
```

## Résultats JSON

### Find (succès)
```json
{
  "found": true,
  "x": 450,
  "y": 320,
  "region": {
    "left": 430,
    "top": 305,
    "width": 40,
    "height": 30
  },
  "clicked": true
}
```

### Find (échec)
```json
{
  "found": false,
  "error": "Element not found on screen"
}
```

### Info
```json
{
  "screen": {"width": 1920, "height": 1080},
  "mouse": {"x": 840, "y": 500},
  "pixel_at_mouse": [45, 45, 48]
}
```

## Exemple d'utilisation par Claude

### Scénario: Cliquer sur Play dans Unity

```bash
# 1. Capturer le bouton Play (une seule fois)
py -3 capture_reference.py unity_play

# 2. Utiliser automatiquement
py -3 smart_vision.py find references/unity_play.png
# Retourne: {"found": true, "x": 240, "y": 30, "clicked": true}

# 3. Attendre que le jeu charge et chercher le menu
py -3 smart_vision.py wait references/game_menu.png 5
# Retourne: {"found": true, "x": 960, "y": 540, "wait_time": 2.3}

# 4. Trouver un bouton spécifique dans le menu
py -3 smart_vision.py find references/start_button.png
```

## Avantages

✓ **Rapide** - Pas de fichiers créés/supprimés
✓ **Précis** - Reconnaissance d'image automatique
✓ **Autonome** - Claude reçoit juste du JSON, pas besoin de Read
✓ **Flexible** - Confidence ajustable, wait timeout, find vs findall
✓ **Propre** - Aucune pollution du disque

## Cas d'usage

### Gaming/Unity
```bash
py -3 smart_vision.py find references/play_button.png
py -3 smart_vision.py wait references/level_complete.png 30
py -3 smart_vision.py findall references/enemy.png
```

### Automation UI
```bash
py -3 smart_vision.py find references/submit_button.png
py -3 smart_vision.py wait references/success_message.png 5
```

### Testing
```bash
py -3 smart_vision.py findall references/error_icon.png
# Si count > 0 → il y a des erreurs
```

## Notes

- Les images de référence sont petites (quelques KB chacune)
- Confidence par défaut: 0.8 (80% match)
- Plus la confidence est haute = plus strict le match
- Baissez la confidence si l'élément n'est pas trouvé (essayez 0.7 ou 0.6)
