#!/usr/bin/env python3
"""CodeOS Repair: diagnose package-manager and package-file problems safely."""
import shutil
import subprocess
import threading
import tkinter as tk
from tkinter import messagebox, ttk

BG = "#101827"

def run(args, timeout=1800):
    return subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          text=True, timeout=timeout, check=False)

class RepairApp:
    def __init__(self, root):
        self.root = root
        root.title("CodeOS Repair")
        root.geometry("760x580")
        root.minsize(580, 450)
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
        ttk.Label(frame, text="CodeOS Repair", style="Title.TLabel").pack(anchor="w")
        ttk.Label(frame, text="بررسی خرابی بسته‌ها و کمک به تعمیر فایل‌های سیستمی",
                  wraplength=690).pack(anchor="w", pady=(5, 12))
        ttk.Button(frame, text="۱. بررسی سلامت سیستم", command=self.scan).pack(anchor="w", pady=3)
        ttk.Label(frame, text="۲. تعمیر فایل‌های یک بسته مشخص (نام بسته را وارد کن):").pack(anchor="w", pady=(12, 4))
        row = ttk.Frame(frame)
        row.pack(fill="x")
        self.package = tk.StringVar()
        ttk.Entry(row, textvariable=self.package).pack(side="left", fill="x", expand=True, padx=(0, 8))
        ttk.Button(row, text="نصب دوباره بسته", command=self.reinstall).pack(side="left")
        ttk.Button(frame, text="۳. ترمیم وابستگی‌ها و نصب‌های نیمه‌تمام", command=self.repair_packages).pack(anchor="w", pady=(10, 3))
        ttk.Button(frame, text="بازکردن بازیابی Timeshift", command=self.restore).pack(anchor="w", pady=3)
        ttk.Label(frame, text="این ابزار فایل‌های شخصی را تعمیر نمی‌کند. پیش از تغییرات مهم، پشتیبان بگیر.",
                  wraplength=690).pack(anchor="w", pady=(10, 6))
        self.status = tk.StringVar(value="ابتدا بررسی سلامت را اجرا کن.")
        ttk.Label(frame, textvariable=self.status, wraplength=690).pack(anchor="w", pady=4)
        self.log = tk.Text(frame, height=13, wrap="word", bg="#0b1220", fg="#dbeafe",
                           insertbackground="white", relief="flat")
        self.log.pack(fill="both", expand=True)

    def write(self, text):
        self.log.insert("end", str(text).rstrip() + "\n")
        self.log.see("end")

    def async_work(self, label, work):
        self.status.set(label)
        def target():
            try:
                result = work()
            except Exception as exc:
                result = "خطا: " + str(exc)
            self.root.after(0, lambda r=result: self.finish(r))
        threading.Thread(target=target, daemon=True).start()

    def finish(self, result):
        self.status.set("عملیات تمام شد؛ گزارش را بررسی کن.")
        self.write(result)

    def scan(self):
        def work():
            out = ["=== بررسی بسته‌های نیمه‌نصب‌شده (dpkg --audit) ==="]
            for args in (["dpkg", "--audit"], ["apt-get", "check"], ["dpkg", "--verify"]):
                r = run(args, timeout=900)
                out.append("$ " + " ".join(args) + "\n" + (r.stdout.strip() or "(خروجی ندارد)"))
                out.append("کد خروج: " + str(r.returncode))
            out.append("\nتفسیر: خروجی dpkg --verify می‌تواند فایل‌های بسته را که با نسخه نصب‌شده تفاوت دارند نشان دهد؛ همه تفاوت‌ها الزاماً خرابی نیستند.")
            out.append("اگر فایل مشکوک است، نام بسته مالک آن را پیدا کن و با گزینه نصب دوباره، همان بسته را تعمیر کن.")
            return "\n\n".join(out)
        self.async_work("در حال بررسی سلامت بسته‌ها…", work)

    def reinstall(self):
        package = self.package.get().strip()
        if not package or any(ch.isspace() for ch in package) or package.startswith("-"):
            messagebox.showwarning("نام بسته", "نام یک بسته معتبر را وارد کن؛ مثلاً xfce4-panel.")
            return
        if not messagebox.askyesno("تأیید تعمیر", f"بسته «{package}» از مخازن APT دوباره نصب می‌شود. ادامه می‌دهی؟"):
            return
        def work():
            out = ["=== بررسی مخازن بسته ==="]
            update = run(["pkexec", "apt-get", "update"], timeout=900)
            out.append(update.stdout[-8000:] or f"apt-get update exit={update.returncode}")
            if update.returncode != 0:
                out.append("به دلیل خطای مخازن/شبکه، نصب دوباره متوقف شد.")
                return "\n".join(out)
            out.append("\n=== نصب دوباره بسته ===")
            result = run(["pkexec", "apt-get", "install", "--reinstall", "-y", "--", package], timeout=1800)
            out.append(result.stdout[-14000:] or f"reinstall exit={result.returncode}")
            out.append("تعمیر بسته موفق بود." if result.returncode == 0 else "تعمیر ناموفق بود؛ گزارش خطا را بررسی کن.")
            return "\n".join(out)
        self.async_work("در حال نصب دوباره بسته…", work)

    def repair_packages(self):
        if not messagebox.askyesno("تأیید ترمیم", "این کار ممکن است بسته‌های سیستم را تغییر دهد. از فایل‌های مهم پشتیبان داری و می‌خواهی ادامه بدهی؟"):
            return
        def work():
            out = ["=== تکمیل پیکربندی بسته‌های نیمه‌نصب‌شده ==="]
            for args in (["pkexec", "dpkg", "--configure", "-a"],
                         ["pkexec", "apt-get", "-f", "install", "-y"]):
                result = run(args, timeout=1800)
                out.append("$ " + " ".join(args) + "\n" + (result.stdout[-10000:] or f"exit={result.returncode}"))
                if result.returncode != 0:
                    out.append("فرایند متوقف شد تا خطا بررسی شود.")
                    break
            return "\n\n".join(out)
        self.async_work("در حال ترمیم وضعیت بسته‌ها…", work)

    def restore(self):
        if not shutil.which("timeshift"):
            messagebox.showwarning("بازیابی", "Timeshift نصب نیست.")
            return
        if not messagebox.askyesno("بازیابی", "بازیابی snapshot ممکن است فایل‌های سیستم را برگرداند و تغییرات جدید را حذف کند. ادامه می‌دهی؟"):
            return
        terminal = shutil.which("x-terminal-emulator")
        if not terminal:
            messagebox.showerror("بازیابی", "ترمینال گرافیکی پیدا نشد.")
            return
        try:
            subprocess.Popen([terminal, "-e", "pkexec", "timeshift", "--restore"])
            self.status.set("ابزار Timeshift باز شد؛ snapshot را با دقت انتخاب کن.")
        except OSError as exc:
            messagebox.showerror("بازیابی", str(exc))

def main():
    root = tk.Tk()
    RepairApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
