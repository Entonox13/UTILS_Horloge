# Horloge plein écran

Application simple pour afficher une **grande horloge en plein écran**, avec en option les **horaires d'une épreuve** (début, fin, pauses, départ des élèves). Pensée pour les salles d'examen, les surveillances et les concours.

Aucune connexion Internet n'est requise une fois le programme installé.

---

## Sommaire

1. [Installation rapide (recommandée)](#installation-rapide-recommandée)
2. [Utilisation pas à pas](#utilisation-pas-à-pas)
3. [Écran de configuration](#écran-de-configuration)
4. [Mode plein écran](#mode-plein-écran)
5. [Presets DNB](#presets-dnb)
6. [Raccourcis clavier](#raccourcis-clavier)
7. [Installation pour développeurs](#installation-pour-développeurs)
8. [Compilation locale](#compilation-locale)
9. [Dépannage](#dépannage)

---

## Installation rapide (recommandée)

Des versions prêtes à l'emploi sont publiées automatiquement à chaque mise à jour du projet.

| Plateforme | Fichier | Lien |
|------------|---------|------|
| **Windows** | `horloge.exe` | [Télécharger](https://github.com/Entonox13/UTILS_Horloge/releases/latest/download/horloge.exe) |
| **Linux** | `Horloge-x86_64.AppImage` | [Télécharger](https://github.com/Entonox13/UTILS_Horloge/releases/latest/download/Horloge-x86_64.AppImage) |

Page des versions : [github.com/Entonox13/UTILS_Horloge/releases/latest](https://github.com/Entonox13/UTILS_Horloge/releases/latest)

### Windows

1. Téléchargez `horloge.exe`.
2. Double-cliquez pour lancer le programme.
3. Si Windows affiche un avertissement de sécurité, choisissez « Exécuter quand même » (le fichier n'est pas signé numériquement).

### Linux

1. Téléchargez `Horloge-x86_64.AppImage`.
2. Rendez-le exécutable, puis lancez-le :

```bash
chmod +x Horloge-x86_64.AppImage
./Horloge-x86_64.AppImage
```

---

## Utilisation pas à pas

Voici le déroulement typique, du premier lancement à la fermeture.

### 1. Lancer le programme

- **Windows** : double-clic sur `horloge.exe`.
- **Linux** : `./Horloge-x86_64.AppImage`
- **Développement** : `python main.py` (voir [Installation pour développeurs](#installation-pour-développeurs))

Une fenêtre de **configuration** s'ouvre.

### 2. Régler l'affichage (optionnel)

Choisissez les couleurs, la taille de l'horloge, la police, etc. (détails ci-dessous).

Si vous voulez seulement l'heure, sans horaires d'épreuve, décochez **« Afficher les horaires de l'épreuve »**.

### 3. Configurer l'épreuve (optionnel)

- Sélectionnez un **preset** (ex. « Français DNB ») ou composez votre propre enchaînement de parties et pauses.
- Indiquez l'**heure de début** de l'épreuve (heure à laquelle commence la première partie).

### 4. Afficher l'horloge

Cliquez sur **Lancer**. L'écran passe en **plein écran** avec l'heure actuelle.

### 5. Revenir aux réglages

Appuyez sur la touche **Échap** : vous retrouvez la fenêtre de configuration.

### 6. Quitter

Dans la fenêtre de configuration, cliquez sur **Quitter**.

---

## Écran de configuration

La fenêtre est organisée en sections. Faites défiler vers le bas si tout ne tient pas à l'écran.

### Couleurs

| Réglage | Rôle |
|---------|------|
| **Fond** | Couleur de l'arrière-plan en mode plein écran (noir par défaut). |
| **Texte horloge** | Couleur des chiffres de l'horloge (blanc par défaut). |
| **Label début / partie** | Couleur des textes « Début de l'épreuve » et « Fin partie… ». |
| **Label fin / départ** | Couleur des textes « Fin de l'épreuve » et « Départ autorisé ». |

Cliquez sur **Choisir** pour ouvrir le sélecteur de couleur de votre système.

### Typographie

| Réglage | Rôle |
|---------|------|
| **Police** | Police d'affichage de l'horloge (polices installées sur votre machine, liste filtrée). |
| **Taille texte** | Taille des chiffres de l'horloge (grande valeur par défaut pour la lisibilité à distance). |

### Options

| Case à cocher | Effet |
|---------------|-------|
| **Afficher les secondes** | Horloge au format `HH:MM:SS` au lieu de `HH:MM`. |
| **Afficher les horaires de l'épreuve** | Bandeau d'informations en bas de l'écran en mode plein écran. |

### Épreuve

| Réglage | Rôle |
|---------|------|
| **Preset** | Modèle prédéfini (matières du DNB, etc.). Choisir **Personnalisé** si vous modifiez la timeline à la main. |
| **Heure de début** | Heure de début de la première partie (format 24 h). |
| **Timeline** | Enchaînement des **parties** et **pauses**, avec leur durée en minutes. |

#### Timeline : boutons et actions

- **+ Partie** : ajoute une partie d'examen.
- **+ Pause** : ajoute une pause (le nom est fixé à « Pause »).
- **^ / v** : monter ou descendre une ligne.
- **x** : supprimer une ligne (il faut garder au moins une partie).

Les horaires affichés en bas de l'écran sont **calculés automatiquement** à partir de l'heure de début et des durées.

#### Informations affichées en plein écran

Quand l'option est activée, le bandeau du bas peut montrer :

- **Début de l'épreuve** — heure de la première partie ;
- **Fin de l'épreuve** — heure de fin de la dernière partie ;
- **Fin [nom de la partie]** — pendant une partie, l'heure de fin de la partie en cours (sauf la dernière) ;
- **Départ autorisé** — une heure après le début de la **dernière** partie.

---

## Mode plein écran

- L'horloge est **centrée en hauteur** (position fixe, vers le quart supérieur de l'écran) pour laisser la place aux horaires en bas.
- L'heure se met à jour en continu.
- **Échap** : retour à la configuration (le plein écran se ferme, vos réglages sont conservés tant que l'application tourne).

---

## Presets DNB

Presets fournis pour le Diplôme National du Brevet (durées indicatives, modifiables) :

| Preset | Contenu |
|--------|---------|
| **Français DNB** | Partie 1 (70 min) → Dictée (20 min) → Pause (15 min) → Partie 2 (90 min) |
| **HGEMC DNB** | Partie 1 (120 min) |
| **Sciences DNB** | Partie 1 (60 min) |
| **Maths DNB** | Partie 1 calculatrice interdite (20 min) → Partie 2 (100 min) |
| **Personnalisé** | Une partie de 60 min par défaut, entièrement modifiable |

La liste détaillée est aussi dans le fichier `DNB.txt` à la racine du projet.

---

## Raccourcis clavier

| Touche | Action |
|--------|--------|
| **Échap** | Quitter le mode plein écran et revenir à la configuration |

---

## Installation pour développeurs

Prérequis : [Conda](https://docs.conda.io/en/latest/miniconda.html) (ou Miniconda/Mamba).

```bash
git clone https://github.com/Entonox13/UTILS_Horloge.git
cd UTILS_Horloge
conda env create -f environment.yml
conda activate utils-horloge
python main.py
```

### Structure du code

```
src/
  app.py           # Application principale (orchestration)
  constants.py     # Constantes d'affichage
  models.py        # Modèles de configuration et d'épreuve
  schedule.py      # Calcul des horaires d'épreuve
  presets.py       # Presets DNB
  theme.py         # Apparence de l'interface (couleurs, polices)
  gui/
    config_view.py # Fenêtre de configuration
    clock_view.py  # Affichage plein écran
    timeline.py    # Éditeur de timeline
main.py            # Point d'entrée
```

---

## Compilation locale

### Linux (binaire unique)

```bash
chmod +x scripts/build_onefile.sh
./scripts/build_onefile.sh
```

### Linux (AppImage)

```bash
chmod +x scripts/build_appimage.sh
./scripts/build_appimage.sh
```

### Windows (.exe)

```powershell
./scripts/build_exe.ps1
```

Les builds automatiques sur GitHub Actions sont décrits dans [`.github/workflows/build.yml`](.github/workflows/build.yml).

---

## Dépannage

### Les textes sont pixellisés / illisibles

Cela arrive lorsque la bibliothèque graphique **Tk** est installée **sans support des polices vectorielles** (build `noxft`).

**Si vous utilisez Conda**, mettez à jour l'environnement :

```bash
conda activate utils-horloge
conda env update -f environment.yml --prune
```

Ou installez explicitement la variante avec fontconfig :

```bash
conda install -c conda-forge tk=8.6.13=xft_h891c84d_3
```

Puis relancez l'application.

### La fenêtre de configuration dépasse l'écran

Faites défiler avec la **molette** de la souris (ou les boutons de défilement à droite). La fenêtre est dimensionnée pour ne pas dépasser la taille de votre écran.

### L'horloge masque les horaires

Réduisez la **taille du texte** dans la configuration, ou décochez temporairement « Afficher les horaires de l'épreuve ».

### L'AppImage ne se lance pas (Linux)

Vérifiez qu'elle est exécutable : `chmod +x Horloge-x86_64.AppImage`

Sur certaines distributions, il faut installer `FUSE` pour les AppImages.

---

## Licence

Projet publié sur GitHub : [Entonox13/UTILS_Horloge](https://github.com/Entonox13/UTILS_Horloge).
