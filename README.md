# Horloge plein ecran (Tkinter)

Application Python/Tkinter qui affiche une horloge en plein ecran avec une fenetre de configuration au lancement.

## Fonctionnalites

- Fenetre de configuration au demarrage
- Parametres:
  - couleur de fond (defaut: noir)
  - couleur du texte (defaut: blanc)
  - police texte (simple, systeme uniquement)
  - taille du texte
- Bouton `Lancer` pour passer en mode plein ecran
- Touche `Echap` pour revenir a la configuration
- Bouton `Quitter` pour fermer l'application

## Environnement conda (Python 3.11)

```bash
conda env create -f environment.yml
conda activate utils-horloge
```

## Lancer en developpement

```bash
python main.py
```

## Build local

### Linux one-file

```bash
chmod +x scripts/build_onefile.sh
./scripts/build_onefile.sh
```

### Linux AppImage

```bash
chmod +x scripts/build_appimage.sh
./scripts/build_appimage.sh
```

### Windows .exe

```powershell
./scripts/build_exe.ps1
```

## GitHub Actions

Le workflow `.github/workflows/build.yml` produit automatiquement:

- `horloge.exe` (artefact `horloge-exe`)
- `Horloge-x86_64.AppImage` (artefact `horloge-appimage`)
