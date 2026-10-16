#!/bin/bash
set -euo pipefail
DESTDIR="${DESTDIR:-}"
install -d "$DESTDIR/usr/share/codeos" "$DESTDIR/usr/local/bin" "$DESTDIR/usr/share/applications" "$DESTDIR/etc/skel/.config/codeos" "$DESTDIR/etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml"
install -m 0644 /project/codeos-ui/codeos-wallpaper.svg "$DESTDIR/usr/share/codeos/codeos-wallpaper.svg"
install -m 0644 /project/codeos-ui/xfce4-panel.xml "$DESTDIR/etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml"
install -m 0644 /project/codeos-ui/xfce4-desktop.xml "$DESTDIR/etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml"
install -m 0755 /project/codeos-ui/codeos-settings.py "$DESTDIR/usr/local/bin/codeos-settings"
install -m 0755 /project/codeos-ui/codeos-store.py "$DESTDIR/usr/local/bin/codeos-store"
install -m 0755 /project/codeos-ui/codeos-control-center.py "$DESTDIR/usr/local/bin/codeos-control-center"
install -m 0755 /project/codeos-ui/codeos-keyboard-setup.sh "$DESTDIR/usr/local/bin/codeos-keyboard-setup"
install -m 0644 /project/security-center/index.html "$DESTDIR/usr/share/codeos/security-center.html"
cat > "$DESTDIR/usr/share/applications/codeos-settings.desktop" <<'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=CodeOS Settings
Name[fa]=تنظیمات CodeOS
Comment=Customize CodeOS appearance
Exec=codeos-settings
Icon=preferences-desktop-theme
Terminal=false
Categories=Settings;DesktopSettings;
EOF
cat > "$DESTDIR/usr/share/applications/codeos-store.desktop" <<'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=CodeOS Software Center
Name[fa]=فروشگاه برنامه‌های CodeOS
Comment=Install selected applications
Exec=codeos-store
Icon=system-software-install
Terminal=false
Categories=System;PackageManager;
EOF
cat > "$DESTDIR/usr/share/applications/codeos-security.desktop" <<'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=CodeOS Security Center
Name[fa]=مرکز امنیت CodeOS
Comment=Security tools dashboard preview
Exec=firefox-esr --new-window file:///usr/share/codeos/security-center.html
Icon=security-high
Terminal=false
Categories=System;Security;
EOF
cat > "$DESTDIR/etc/skel/.config/codeos/README.txt" <<'EOF'
CodeOS X user settings are stored in ~/.config/codeos.
The desktop wallpaper is installed at /usr/share/codeos/codeos-wallpaper.svg.
EOF
cat > "$DESTDIR/usr/share/applications/codeos-installer.desktop" <<'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Install CodeOS X
Name[fa]=نصب CodeOS X
Comment=Install this live system to the computer
Exec=pkexec calamares
Icon=drive-harddisk
Terminal=false
Categories=System;
EOF

cat > "$DESTDIR/usr/share/applications/codeos-control-center.desktop" <<'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=CodeOS Control Center
Name[fa]=مرکز کنترل CodeOS
Comment=System settings and tools
Comment[fa]=تنظیمات و ابزارهای سیستم
Exec=codeos-control-center
Icon=preferences-system
Terminal=false
Categories=Settings;System;
EOF
install -d "$DESTDIR/etc/skel/.config/autostart"
cat > "$DESTDIR/etc/skel/.config/autostart/codeos-keyboard.desktop" <<'EOF'
[Desktop Entry]
Type=Application
Name=CodeOS Persian/English Keyboard
Name[fa]=کیبورد فارسی و انگلیسی CodeOS
Exec=codeos-keyboard-setup
Terminal=false
X-GNOME-Autostart-enabled=true
EOF
