# Claude PC Control

Système d'automation GUI permettant à Claude de contrôler votre PC avec **précision absolue** via un système de grille intelligent.

> **v2.0** - Grid system + OmniParser integration + Nettoyage complet

## Installation

```bash
cd C:\Perso\Claude_ControlPc
py -3 setup.py
```

## Utilisation

### 1. Captures d'écran

```bash
# Capture complète
py -3 screenshot.py

# Capture avec nom personnalisé
py -3 screenshot.py output.png

# Capture d'une région spécifique (x, y, width, height)
py -3 screenshot.py region.png 100 100 800 600
```

Claude peut ensuite lire l'image avec son outil Read pour l'analyser visuellement.

### 2. Contrôle de la souris

```bash
# Obtenir la position actuelle
py -3 mouse_control.py position

# Déplacer à une position absolue
py -3 mouse_control.py move 500 300

# Déplacer avec durée personnalisée
py -3 mouse_control.py move 500 300 1.5

# Cliquer à une position
py -3 mouse_control.py click 400 200

# Clic droit
py -3 mouse_control.py click 400 200 right

# Double-clic
py -3 mouse_control.py doubleclick 400 200

# Cliquer à la position actuelle
py -3 mouse_control.py click

# Glisser-déposer
py -3 mouse_control.py drag 600 400

# Scroll (positif = haut, négatif = bas)
py -3 mouse_control.py scroll 3
py -3 mouse_control.py scroll -5 500 300
```

### 3. Contrôle du clavier

```bash
# Taper du texte
py -3 keyboard_control.py type "Hello World"

# Appuyer sur une touche
py -3 keyboard_control.py press enter
py -3 keyboard_control.py press tab 3

# Raccourcis clavier (hotkeys)
py -3 keyboard_control.py hotkey ctrl c
py -3 keyboard_control.py hotkey ctrl shift esc
py -3 keyboard_control.py hotkey win d

# Maintenir une touche
py -3 keyboard_control.py hold shift 2
```

**Touches disponibles:**
- Modificateurs: `ctrl`, `alt`, `shift`, `win`
- Navigation: `enter`, `tab`, `esc`, `space`, `backspace`, `delete`
- Flèches: `up`, `down`, `left`, `right`
- Fonction: `f1`-`f12`
- Alphanumériques: `a`-`z`, `0`-`9`

### 4. Informations d'écran

```bash
# Obtenir la taille de l'écran
py -3 screen_info.py size

# Trouver une image sur l'écran
py -3 screen_info.py find button.png
py -3 screen_info.py find icon.png 0.8

# Trouver toutes les instances
py -3 screen_info.py findall element.png

# Obtenir la couleur d'un pixel
py -3 screen_info.py pixel 500 300
```

## Démonstration

```bash
py -3 demo.py
```

Ce script démontre toutes les fonctionnalités:
1. Informations d'écran
2. Mouvement de la souris
3. Saisie clavier (ouvre Notepad)
4. Capture d'écran

## Sécurité

**Failsafe:** Déplacez rapidement la souris vers le coin supérieur gauche de l'écran pour interrompre n'importe quel script PyAutoGUI.

## Workflow avec Claude

1. **Claude prend une capture d'écran:**
   ```bash
   py -3 screenshot.py current.png
   ```

2. **Claude lit et analyse l'image:**
   ```
   (Utilise l'outil Read sur current.png)
   ```

3. **Claude détermine l'action:**
   - Trouve un bouton à cliquer
   - Identifie où taper du texte

4. **Claude exécute l'action:**
   ```bash
   py -3 mouse_control.py click 450 320
   py -3 keyboard_control.py type "text"
   ```

5. **Répétition:** Capture → Analyse → Action

## Exemples d'automatisations

### Ouvrir un programme
```bash
# Ouvrir le menu Démarrer
py -3 keyboard_control.py press win

# Taper le nom du programme
py -3 keyboard_control.py type "notepad"

# Valider
py -3 keyboard_control.py press enter
```

### Copier-coller
```bash
# Sélectionner tout
py -3 keyboard_control.py hotkey ctrl a

# Copier
py -3 keyboard_control.py hotkey ctrl c

# Coller ailleurs
py -3 mouse_control.py click 600 400
py -3 keyboard_control.py hotkey ctrl v
```

### Recherche visuelle
```bash
# Capturer l'écran
py -3 screenshot.py search_area.png

# (Claude analyse l'image avec Read)
# (Claude identifie l'élément à x=450, y=320)

# Cliquer sur l'élément trouvé
py -3 mouse_control.py click 450 320
```

## Notes importantes

- **Coordonnées absolues:** Les positions sont relatives au coin supérieur gauche de l'écran
- **Multi-écrans:** PyAutoGUI considère tous les écrans comme un seul grand écran virtuel
- **Délais:** Ajoutez des pauses entre les commandes si nécessaire (via `timeout` dans Bash)
- **Permissions:** Certains programmes (UAC, antivirus) peuvent bloquer les inputs simulés

## Dépannage

### PyAutoGUI ne s'installe pas
```bash
py -3 -m pip install --upgrade pip
py -3 -m pip install pyautogui pillow
```

### Les clics ne fonctionnent pas
- Vérifiez que le programme cible n'a pas besoin de privilèges admin
- Essayez d'exécuter le script en tant qu'administrateur

### Les captures d'écran sont noires
- Problème connu avec certains jeux en plein écran
- Utilisez le mode fenêtré ou des outils spécifiques (OBS, MSI Afterburner)

## Ressources

- [PyAutoGUI Documentation](https://pyautogui.readthedocs.io/)
- [Pillow Documentation](https://pillow.readthedocs.io/)
