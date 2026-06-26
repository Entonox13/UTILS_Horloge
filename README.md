# Horloge plein ecran (Tkinter)

Application Python/Tkinter qui affiche une horloge en plein ecran avec une fenetre de configuration au lancement.

## Telechargement

Binaires precompiles (mis a jour automatiquement a chaque push sur `main`) :

| Plateforme | Fichier | Lien |
|------------|---------|------|
| Windows | `horloge.exe` | [Telecharger](https://github.com/Entonox13/UTILS_Horloge/releases/latest/download/horloge.exe) |
| Linux | `Horloge-x86_64.AppImage` | [Telecharger](https://github.com/Entonox13/UTILS_Horloge/releases/latest/download/Horloge-x86_64.AppImage) |

Page des releases : [github.com/Entonox13/UTILS_Horloge/releases/latest](https://github.com/Entonox13/UTILS_Horloge/releases/latest)

### Utilisation des binaires

**Windows** : lancer `horloge.exe`.

**Linux** : rendre l'AppImage executable puis la lancer :

```bash
chmod +x Horloge-x86_64.AppImage
./Horloge-x86_64.AppImage
```

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

Le workflow [`.github/workflows/build.yml`](.github/workflows/build.yml) :

1. compile `horloge.exe` (Windows) et `Horloge-x86_64.AppImage` (Linux) ;
2. publie les deux fichiers dans la [release `latest`](https://github.com/Entonox13/UTILS_Horloge/releases/latest), accessibles depuis les liens ci-dessus.
