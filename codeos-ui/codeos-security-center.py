#!/usr/bin/env python3
"""CodeOS Security Center: real local status checks and user-confirmed scans."""
import os
import shutil
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

BG = "#101827"
FG = "#edf3ff"
ACCENT = "#8db2ff"

def command(args, timeout=20):
    try:
        return subprocess.run(args, capture_output=True, text=True, timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None

def main():
    root = tk.Tk()
    root.title("مرکز امنیت CodeOS X")
    root.geometry("760x620")
    root.minsize(600, 500)
    root.configure(bg=BG)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background=BG)
    style.configure("TLabel", background=BG, foreground=FG, font=("TkDefaultFont", 10))
    style.configure("Title.TLabel", background=BG, foreground=ACCENT, font=("TkDefaultFont", 20, "bold"))
    style.configure("TButton", padding=8)
    frame = ttk.Frame(root, padding=22)
    frame.pack(fill="both", expand=True)
    ttk.Label(frame, text="مرکز امنیت CodeOS X", style="Title.TLabel").pack(anchor="w")
    ttk.Label(frame, text="وضعیت واقعی ابزارهای محلی؛ هیچ اسکن یا تغییری بدون درخواست تو انجام نمی‌شود.", wraplength=700).pack(anchor="w", pady=(5, 15))
    status = tk.Text(frame, height=15, wrap="word", bg="#172338", fg=FG, insertbackground=FG, relief="flat", padx=12, pady=12)
    status.pack(fill="both", expand=True, pady=(0, 12))
    status.configure(state="disabled")

    def show(text):
        status.configure(state="normal")
        status.delete("1.0", "end")
        status.insert("end", text)
        status.configure(state="disabled")

    def refresh():
        lines = ["گزارش وضعیت سیستم", "=" * 28]
        if shutil.which("ufw"):
            r = command(["ufw", "status"])
            lines.append("\nفایروال UFW:\n" + ((r.stdout or r.stderr).strip() if r else "بررسی ناموفق"))
        else:
            lines.append("\nفایروال UFW: نصب نیست")
        if shutil.which("clamscan"):
            r = command(["clamscan", "--version"])
            lines.append("\nآنتی‌ویروس ClamAV:\n" + ((r.stdout or r.stderr).strip() if r else "بررسی ناموفق"))
        else:
            lines.append("\nClamAV: نصب نیست")
        if shutil.which("apt-get"):
            r = command(["apt-get", "-s", "upgrade"], timeout=60)
            if r and r.returncode == 0:
                lines.append("\nبررسی به‌روزرسانی‌ها:\n" + next((x.strip() for x in r.stdout.splitlines() if "upgraded," in x), "بررسی شبیه‌سازی‌شده انجام شد؛ جزئیات در خروجی apt موجود است."))
            else:
                lines.append("\nبررسی به‌روزرسانی‌ها: ناموفق؛ اتصال شبکه و مخازن را بررسی کن.")
        else:
            lines.append("\nمدیر بسته APT در دسترس نیست.")
        lines.append("\nتوجه: این ابزار جایگزین ممیزی حرفه‌ای یا تضمین امنیت کامل نیست.")
        show("\n".join(lines))

    def scan():
        if not shutil.which("clamscan"):
            messagebox.showwarning("ClamAV نصب نیست", "برای اسکن فایل‌ها ابتدا بسته clamav را از فروشگاه یا مخازن رسمی نصب کن.")
            return
        folder = filedialog.askdirectory(title="پوشه موردنظر برای اسکن را انتخاب کن")
        if not folder:
            return
        if not messagebox.askyesno("تأیید اسکن", "اسکن فایل‌های پوشه زیر شروع شود؟\n" + folder):
            return
        show("اسکن در حال اجراست؛ بسته به تعداد فایل‌ها ممکن است زمان ببرد...\n")
        root.update_idletasks()
        r = command(["clamscan", "-r", "--infected", "--no-summary", folder], timeout=3600)
        if r is None:
            show("اسکن متوقف یا ناموفق شد. زمان اجرا یا نصب ClamAV را بررسی کن.")
            return
        result = (r.stdout or "") + (r.stderr or "")
        show("گزارش اسکن ClamAV\n" + "=" * 28 + "\n" + (result[-12000:] or "ClamAV خروجی متنی نداد.") + "\n\nکد خروج: " + str(r.returncode) + "\nکد 0 معمولاً یعنی تهدیدی شناسایی نشد؛ کد 1 یعنی تهدید شناسایی شد؛ کد 2 خطا را نشان می‌دهد.")
    def firewall():
        if not shutil.which("ufw"):
            messagebox.showwarning("UFW نصب نیست", "ابتدا بسته ufw را نصب کن.")
            return
        if not messagebox.askyesno("تأیید فعال‌سازی فایروال", "فعال‌کردن UFW ممکن است بر اتصال‌های ورودی اثر بگذارد. ادامه می‌دهی؟"):
            return
        try:
            subprocess.Popen(["x-terminal-emulator", "-e", "sh", "-lc", "pkexec ufw enable; echo; read -r -p 'برای بستن Enter را بزن...' _"])
        except OSError as exc:
            messagebox.showerror("خطا", str(exc))
    buttons = ttk.Frame(frame)
    buttons.pack(fill="x")
    ttk.Button(buttons, text="به‌روزرسانی وضعیت", command=refresh).pack(side="left", padx=(0, 8))
    ttk.Button(buttons, text="اسکن پوشه با ClamAV", command=scan).pack(side="left", padx=8)
    ttk.Button(buttons, text="فعال‌کردن UFW…", command=firewall).pack(side="left", padx=8)
    refresh()
    root.mainloop()

if __name__ == "__main__":
    main()
