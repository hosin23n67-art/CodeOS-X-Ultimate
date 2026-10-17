#!/usr/bin/env python3
"""CodeOS Update: controlled APT updates and optional Timeshift recovery."""
import json
import os
import shutil
import subprocess
import threading
import urllib.error
import urllib.request
import tkinter as tk
from tkinter import messagebox, ttk

REPO = "hosin23n67-art/CodeOS-X-Ultimate"
API = f"https://api.github.com/repos/{REPO}/releases/latest"
VERSION_FILE = "/usr/share/codeos/version"
BG = "#101827"

def command(args, timeout=1800):
    return subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          text=True, timeout=timeout, check=False)

class Updater:
    def __init__(self, root):
        self.root = root
        root.title("CodeOS Update")
        root.geometry("720x540")
        root.minsize(560, 420)
        root.configure(bg=BG)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=BG)
        style.configure("TLabel", background=BG, foreground="#edf3ff")
        style.configure("Title.TLabel", font=("TkDefaultFont", 19, "bold"),
                        foreground="#8db2ff", background=BG)
        style.configure("TButton", padding=8)
        frame = ttk.Frame(root, padding=22)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="CodeOS Update", style="Title.TLabel").pack(anchor="w")
        self.version = self.read_version()
        ttk.Label(frame, text=f"نسخه نصب‌شده: {self.version}").pack(anchor="w", pady=(4, 12))
        ttk.Label(frame, text="به‌روزرسانی‌های سیستم، بررسی نسخه CodeOS و بازیابی",
                  wraplength=640).pack(anchor="w", pady=(0, 12))
        row = ttk.Frame(frame)
        row.pack(fill="x")
        ttk.Button(row, text="بررسی آپدیت‌ها", command=self.check_updates).pack(side="left", padx=(0, 8))
        ttk.Button(row, text="نصب آپدیت‌های سیستم", command=self.install_updates).pack(side="left", padx=8)
        ttk.Button(row, text="بازیابی سیستم", command=self.restore).pack(side="left", padx=8)
        self.status = tk.StringVar(value="برای شروع، بررسی آپدیت‌ها را انتخاب کن.")
        ttk.Label(frame, textvariable=self.status, wraplength=650).pack(anchor="w", pady=(16, 6))
        self.log = tk.Text(frame, height=14, wrap="word", bg="#0b1220", fg="#dbeafe",
                           insertbackground="white", relief="flat")
        self.log.pack(fill="both", expand=True)
        self.write("توجه: آپدیت‌های APT با مخازن رسمی تنظیم‌شده سیستم دریافت می‌شوند.\n"
                   "نسخه‌های اختصاصی CodeOS از بخش Releases مخزن بررسی می‌شوند؛ این ابزار به‌تنهایی ISO را جایگزین نمی‌کند.\n"
                   "بازیابی خودکار فقط در صورت نصب و پیکربندی Timeshift و وجود snapshot ممکن است.\n")

    def read_version(self):
        try:
            with open(VERSION_FILE, encoding="utf-8") as f:
                return f.read().strip() or "نامشخص"
        except OSError:
            return "نامشخص"

    def write(self, text):
        self.log.insert("end", text.rstrip() + "\n")
        self.log.see("end")

    def busy(self, label):
        self.status.set(label)

    def run_async(self, label, work):
        self.busy(label)
        def target():
            try:
                result = work()
                self.root.after(0, lambda: self.finish(result))
            except Exception as exc:
                self.root.after(0, lambda e=str(exc): self.finish("خطا: " + e))
        threading.Thread(target=target, daemon=True).start()

    def finish(self, result):
        self.busy("عملیات تمام شد.")
        self.write(str(result))

    def check_updates(self):
        def work():
            output = []
            output.append("=== بررسی نسخه CodeOS ===")
            req = urllib.request.Request(API, headers={"Accept": "application/vnd.github+json",
                                                       "User-Agent": "CodeOS-Updater"})
            try:
                with urllib.request.urlopen(req, timeout=12) as response:
                    release = json.load(response)
                output.append("آخرین انتشار: " + release.get("tag_name", "بدون برچسب"))
                output.append(release.get("html_url", ""))
                output.append("برای به‌روزرسانی اختصاصی، انتشار باید شامل دستورالعمل/بسته قابل نصب معتبر باشد؛ ISO به‌صورت خودکار جایگزین نمی‌شود.")
            except urllib.error.HTTPError as exc:
                output.append(f"انتشار CodeOS در دسترس نیست (HTTP {exc.code}). ممکن است هنوز Release منتشر نشده باشد.")
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                output.append(f"بررسی Release ناموفق بود: {exc}")
            output.append("\n=== بررسی بسته‌های سیستم ===")
            r = command(["pkexec", "apt-get", "update"], timeout=900)
            output.append(r.stdout[-12000:] or f"apt-get update exit={r.returncode}")
            if r.returncode == 0:
                p = command(["apt-get", "-s", "upgrade"], timeout=300)
                output.append("\n" + p.stdout[-12000:])
                if p.returncode:
                    output.append("شبیه‌سازی ارتقا ناموفق بود.")
            else:
                output.append("به دلیل خطای به‌روزرسانی فهرست بسته‌ها، تعداد آپدیت‌ها بررسی نشد.")
            return "\n".join(output)
        self.run_async("در حال بررسی آپدیت‌ها…", work)

    def install_updates(self):
        if not messagebox.askyesno("تأیید نصب", "نصب آپدیت‌های سیستم ممکن است بسته‌ها و هسته را تغییر دهد. قبل از ادامه از اطلاعات مهم پشتیبان بگیر. ادامه می‌دهی؟"):
            return
        def work():
            output = ["=== ایجاد snapshot در صورت آماده بودن Timeshift ==="]
            if shutil.which("timeshift"):
                snap = command(["pkexec", "timeshift", "--create", "--comments",
                                "Before CodeOS system update", "--tags", "D"], timeout=900)
                output.append(snap.stdout[-5000:] or f"Timeshift exit={snap.returncode}")
                if snap.returncode != 0:
                    output.append("ساخت snapshot تأیید نشد؛ نصب آپدیت لغو شد تا خطر کمتر شود.")
                    return "\n".join(output)
            else:
                output.append("Timeshift نصب نیست؛ برای جلوگیری از تغییر بدون نقطه بازیابی، نصب متوقف شد. ابتدا snapshot/پشتیبان را تنظیم کن.")
                return "\n".join(output)
            output.append("\n=== نصب آپدیت‌ها ===")
            r = command(["pkexec", "apt-get", "full-upgrade", "-y"], timeout=3600)
            output.append(r.stdout[-18000:] or f"apt-get full-upgrade exit={r.returncode}")
            output.append("نصب موفق بود." if r.returncode == 0 else "نصب با خطا پایان یافت؛ گزارش بالا را بررسی کن.")
            return "\n".join(output)
        self.run_async("در حال تهیه snapshot و نصب آپدیت‌ها…", work)

    def restore(self):
        if not shutil.which("timeshift"):
            messagebox.showwarning("بازیابی", "Timeshift نصب نیست؛ بازیابی از داخل CodeOS در دسترس نیست.")
            return
        if not messagebox.askyesno("بازیابی سیستم", "بازیابی snapshot می‌تواند فایل‌های سیستم را تغییر دهد. ادامه در ابزار Timeshift؟"):
            return
        terminal = shutil.which("x-terminal-emulator")
        if not terminal:
            messagebox.showerror("بازیابی", "ترمینال گرافیکی پیدا نشد.")
            return
        try:
            subprocess.Popen([terminal, "-e", "pkexec", "timeshift", "--restore"])
            self.status.set("ابزار بازیابی Timeshift باز شد؛ snapshot را با دقت انتخاب کن.")
        except OSError as exc:
            messagebox.showerror("بازیابی", str(exc))

def main():
    root = tk.Tk()
    Updater(root)
    root.mainloop()

if __name__ == "__main__":
    main()
