# CodeOS X desktop components

This directory adds the first native desktop integration layer for the CodeOS X Ultimate Kali-based live image.

- **CodeOS Settings**: XFCE light/dark theme selection, accent preference, and wallpaper picker.
- **CodeOS Software Center**: curated package list; asks before using PolicyKit to install from the system's configured APT repositories.
- **CodeOS Security Center**: opens the existing Persian security dashboard.
- **Default wallpaper**: CodeOS X SVG artwork.

Security Center simulated scan results remain explicitly labeled as demo data. Software installation depends on network access, working APT repositories, and a PolicyKit authentication agent. This is not a replacement for a full installer or a verified ISO.

- **CodeOS Control Center**: one window for appearance, software, files, network, display, audio, power, processes and security.
- **Persian/English keyboard**: US + Persian XKB layouts, Alt+Shift switching, and an XFCE panel layout indicator (FA/EN).
- Additional desktop utilities: power manager, notifications, Bluetooth, audio control and archive integration.
- The ISO workflow collects the ISO from Kali live-build's actual output path, checks the El Torito boot catalog, and runs Python, shell, XML, and SVG source validation before the expensive build. These checks do not replace real boot testing.
