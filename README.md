# CodeOS X Ultimate

A custom **64-bit Kali Linux live ISO** project intended for the Lenovo ThinkPad T570.

## Planned package set
- Kali Linux rolling base and default desktop (XFCE)
- Python 3, GCC/G++, Clang/LLVM, Git, CMake, Ninja, NASM
- Firefox ESR and common terminal/network utilities
- Selected network analysis tools such as Nmap and Wireshark

## Build the ISO in GitHub Actions
1. Open the **Actions** tab in this repository.
2. Select **Build CodeOS X Ultimate ISO**.
3. Press **Run workflow**.
4. Wait for the run to complete successfully.
5. Open the run's **Artifacts** section and download `CodeOS-X-Ultimate-amd64-ISO`.

The build can take a long time and may fail if GitHub's runner runs out of disk space or Kali's package repositories are unavailable. The workflow runs source syntax checks before the expensive build, then checks the resulting ISO file and its El Torito boot catalog. These checks improve confidence but do not replace booting the ISO in a VM and testing it on real hardware.

## Important
This is a custom Kali-based live ISO project. A successful build and boot-catalog check do not prove that every desktop feature or the installer works; test it in a virtual machine and from a USB drive before installing. Test the ISO from a USB drive before installing. Installing an OS can erase data on the internal drive; back up important files first.

Kali Linux packages and trademarks remain subject to their respective licenses.

## CodeOS Update and recovery
The desktop image includes a CodeOS Update utility for checking APT upgrades and checking the repository's latest GitHub Release. A successful APT update is separate from updating the custom CodeOS ISO: the updater does not replace the running OS with a new ISO automatically.

System upgrades require Timeshift to be installed and configured with a working snapshot destination. The updater stops before upgrading if it cannot confirm that a snapshot was created. Restore opens Timeshift's interactive restore workflow; recovery is not guaranteed, so keep a separate backup of important files. Release-based CodeOS updates require a published GitHub Release and a future signed, installable update package; the current utility only reports release metadata and does not install arbitrary release assets.
