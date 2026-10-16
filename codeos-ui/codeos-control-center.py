#!/usr/bin/env python3
"""Unified CodeOS X graphical control center."""
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

ACTIONS = [
    ("ظاهر، تم و تصویر زمینه", "codeos-settings", "تنظیمات ظاهری CodeOS"),
    ("فروشگاه برنامه‌ها", "codeos-store", "نصب و مدیریت برنامه‌ها"),
    ("مدیریت فایل‌ها", "thunar", "باز کردن مدیر فایل"),
    ("شبکه و وای‌فای", "nm-connection-editor", "مدیریت اتصال‌های شبکه"),
    ("نمایشگر", "xfce4-display-settings", "وضوح و چیدمان نمایشگر"),
    ("صدا", "pavucontrol", "خروجی صدا و میکروفون"),
    ("باتری و انرژی", "xfce4-power-manager-settings", "تنظیمات مصرف انرژی"),
    ("مدیریت فرایندها", "xfce4-taskmanager", "نمایش CPU و حافظه"),
    ("مرکز امنیت", "codeos-security", "باز کردن داشبورد امنیتی"),
]

def launch(command):
    try:
        subprocess.Popen(command.split())
    except OSError as exc:
        messagebox.showerror("CodeOS", f"اجرای برنامه ممکن نیست. شاید بسته نصب نشده باشد.\n{exc}")

def main():
    root = tk.Tk()
    root.title("مرکز کنترل CodeOS X")
    root.geometry("620x570")
    root.minsize(500, 450)
    root.configure(bg="#101827")
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#101827")
    style.configure("TLabel", background="#101827", foreground="#edf3ff")
    style.configure("Title.TLabel", font=("TkDefaultFont", 21, "bold"), foreground="#8db2ff")
    style.configure("TButton", padding=10)
    frame = ttk.Frame(root, padding=22)
    frame.pack(fill="both", expand=True)
    ttk.Label(frame, text="CodeOS X", style="Title.TLabel").pack(anchor="w")
    ttk.Label(frame, text="مرکز کنترل سیستم — انتخاب کنید چه چیزی را تنظیم کنید").pack(anchor="w", pady=(4, 18))
    for title, command, description in ACTIONS:
        row = ttk.Frame(frame, padding=(0, 4))
        row.pack(fill="x")
        ttk.Label(row, text=title, font=("TkDefaultFont", 11, "bold"), width=24).pack(side="left", anchor="w")
        ttk.Label(row, text=description).pack(side="left", fill="x", expand=True, padx=8)
        ttk.Button(row, text="باز کردن", command=lambda c=command: launch(c)).pack(side="right")
    ttk.Separator(frame).pack(fill="x", pady=12)
    ttk.Button(frame, text="اعمال کیبورد فارسی / انگلیسی (Alt+Shift)", command=lambda: launch("codeos-keyboard-setup")).pack(anchor="w")
    ttk.Label(frame, text="برای تغییر زبان، از Alt+Shift استفاده کنید؛ نشانگر FA/EN در نوار وظیفه قرار دارد.", wraplength=560).pack(anchor="w", pady=(8, 0))
    root.mainloop()

if __name__ == "__main__":
    main()
