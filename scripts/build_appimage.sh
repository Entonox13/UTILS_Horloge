#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

"$ROOT_DIR/scripts/build_onefile.sh"

APPDIR="$ROOT_DIR/dist/AppDir"
APPIMAGE_NAME="Horloge-x86_64.AppImage"

rm -rf "$APPDIR"
mkdir -p "$APPDIR/usr/bin"

cp "$ROOT_DIR/dist/horloge" "$APPDIR/usr/bin/horloge"

cat > "$APPDIR/AppRun" <<'EOF'
#!/usr/bin/env bash
HERE="$(dirname "$(readlink -f "${0}")")"
exec "${HERE}/usr/bin/horloge" "$@"
EOF
chmod +x "$APPDIR/AppRun"

cat > "$APPDIR/horloge.desktop" <<'EOF'
[Desktop Entry]
Type=Application
Name=Horloge
Exec=horloge
Icon=horloge
Categories=Utility;
Terminal=false
EOF

cat > "$APPDIR/horloge.svg" <<'EOF'
<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256">
  <rect x="0" y="0" width="256" height="256" rx="28" fill="#111111"/>
  <circle cx="128" cy="128" r="88" fill="#111111" stroke="#ffffff" stroke-width="12"/>
  <line x1="128" y1="128" x2="128" y2="72" stroke="#ffffff" stroke-width="10" stroke-linecap="round"/>
  <line x1="128" y1="128" x2="168" y2="144" stroke="#ffffff" stroke-width="10" stroke-linecap="round"/>
  <circle cx="128" cy="128" r="8" fill="#ffffff"/>
</svg>
EOF

ln -s horloge.svg "$APPDIR/.DirIcon"

APPIMAGETOOL="$ROOT_DIR/dist/appimagetool-x86_64.AppImage"
if [ ! -f "$APPIMAGETOOL" ]; then
  curl -L \
    "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage" \
    -o "$APPIMAGETOOL"
  chmod +x "$APPIMAGETOOL"
fi

APPIMAGE_EXTRACT_AND_RUN=1 ARCH=x86_64 "$APPIMAGETOOL" "$APPDIR" "$ROOT_DIR/dist/$APPIMAGE_NAME"

echo "AppImage generated in dist/$APPIMAGE_NAME"
