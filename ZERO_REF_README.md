# Vision Automatique SANS Références

## Principe

**Aucune image de référence nécessaire!**

Le système utilise:
- **Détection de couleurs** (OpenCV)
- **Détection de formes** (rectangles, boutons)
- **Heuristiques** (positions connues pour Unity, etc.)
- **OCR** (optionnel - si Tesseract installé)

## Commandes

### 1. Trouver le bouton Play Unity (AUTOMATIQUE)

```bash
py -3 auto_vision.py unity
```

Retourne:
```json
{
  "found": true,
  "x": 240,
  "y": 30,
  "method": "unity_heuristic"
}
```

### 2. Trouver par couleur

```bash
# Boutons verts (Unity Play, etc.)
py -3 auto_vision.py color green

# Boutons bleus
py -3 auto_vision.py color blue

# Boutons rouges
py -3 auto_vision.py color red
```

### 3. Trouver par texte (OCR - nécessite Tesseract)

```bash
py -3 auto_vision.py text "Play"
py -3 auto_vision.py text "Start Game"
```

### 4. Trouver des rectangles (boutons, menus)

```bash
# Boutons standards (50-300px large, 30-100px haut)
py -3 auto_vision.py rectangles

# Personnalisé
py -3 auto_vision.py rectangles 100 50 400 150
```

### 5. Click intelligent (RECOMMANDÉ)

```bash
# Trouve automatiquement et clique
py -3 auto_vision.py click unity_play
py -3 auto_vision.py click "Start"
py -3 auto_vision.py click green color
```

## Workflow complet pour Unity

```bash
# 1. Cliquer sur Play
py -3 auto_vision.py click unity_play

# 2. Attendre 3 secondes
sleep 3

# 3. Appuyer sur Espace
py -3 keyboard_control.py press space

# 4. Trouver bouton dans le menu (par couleur)
py -3 auto_vision.py color blue

# 5. Bouger souris sur premier bouton trouvé
# (parsez le JSON, extrayez x,y du premier location)
py -3 mouse_control.py move X Y
```

## Exemples de résultats

### Unity Play button trouvé:
```json
{
  "found": true,
  "x": 240,
  "y": 30,
  "method": "unity_heuristic",
  "all_candidates": 1
}
```

### Boutons bleus trouvés:
```json
{
  "found": true,
  "count": 3,
  "locations": [
    {"x": 450, "y": 320, "width": 120, "height": 40, "area": 4800},
    {"x": 620, "y": 320, "width": 110, "height": 38, "area": 4180},
    {"x": 960, "y": 540, "width": 100, "height": 35, "area": 3500}
  ]
}
```

## Installation OCR (Optionnel)

Si vous voulez utiliser la recherche de texte:

1. Téléchargez Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
2. Installez (typiquement dans `C:\Program Files\Tesseract-OCR`)
3. Ajoutez au PATH ou configurez pytesseract

**Mais ce n'est PAS nécessaire** - détection couleur/forme fonctionne sans OCR!

## Avantages

✓ **Zéro configuration** - fonctionne immédiatement
✓ **Pas de références** - pas besoin de capturer quoi que ce soit
✓ **Rapide** - traitement en mémoire
✓ **Flexible** - plusieurs méthodes de détection
✓ **Unity-aware** - heuristiques spécifiques pour Unity

## Limitations

- Détection de couleur peut avoir des faux positifs
- Heuristiques Unity peuvent échouer si UI custom
- OCR nécessite Tesseract installé
- Marche mieux avec des UI contrastées

## Tips

- Pour Unity Play: utilisez `unity` command (le plus fiable)
- Pour boutons colorés: utilisez `color`
- Pour texte: utilisez `text` (nécessite OCR)
- Pour UI génériques: utilisez `rectangles`
- Pour click automatique: utilisez `click <target> auto`
