#!/usr/bin/env python3
"""Simple software center using a strict allowlist and PolicyKit prompt."""
import subprocess, tkinter as tk
from tkinter import ttk, messagebox
APPS=[("Firefox ESR","مرورگر وب","firefox-esr"),("VLC","پخش‌کننده رسانه","vlc"),("GIMP","ویرایش تصویر","gimp"),("LibreOffice","مجموعه اداری","libreoffice"),("Code - OSS","ویرایشگر کد آزاد","codium"),("Geany","ویرایشگر سبک کد","geany"),("Git","مدیریت نسخه","git"),("Python 3","زبان برنامه‌نویسی","python3"),("Nmap","تحلیل شبکه‌های مجاز","nmap"),("Wireshark","تحلیل بسته‌های شبکه","wireshark"),("GParted","مدیریت پارتیشن‌ها","gparted"),("ClamAV","پویش بدافزار","clamav")]
def installed(pkg):
    p=subprocess.run(["dpkg-query","-W","-f=${Status}",pkg],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True)
    return "install ok installed" in p.stdout
def install(pkg):
    if not messagebox.askyesno("تأیید نصب", f"نصب «{pkg}» با دسترسی مدیر انجام شود؟\\nبسته از مخازن تنظیم‌شده سیستم دریافت می‌شود."):
        return
    # Package names come only from the fixed APPS allowlist above.
    # Run the transaction in a visible terminal so APT errors are not hidden.
    command = (
        "pkexec apt-get install -y " + pkg +
        "; rc=$?; echo; "
        'if [ "$rc" -eq 0 ]; then echo "نصب با موفقیت پایان یافت."; '
        'else echo "نصب ناموفق بود؛ پیام خطا را بررسی کن."; fi; '
        'echo; read -r -p "برای بستن این پنجره Enter را بزن..." _'
    )
    try:
        subprocess.Popen(["x-terminal-emulator", "-e", "sh", "-lc", command])
    except OSError as e:
        messagebox.showerror(
            "خطا",
            f"اجرای ترمینال نصب ممکن نیست: {e}\\n"
            "می‌توانی بسته را از ترمینال با دستور apt install نصب کنی."
        )

def main():
    root=tk.Tk(); root.title("فروشگاه برنامه‌های CodeOS"); root.geometry("680x580"); root.minsize(520,420); root.configure(bg="#101827")
    style=ttk.Style(); style.theme_use("clam"); style.configure("TFrame",background="#101827"); style.configure("TLabel",background="#101827",foreground="#edf3ff"); style.configure("Title.TLabel",font=("TkDefaultFont",20,"bold"),foreground="#8db2ff")
    frame=ttk.Frame(root,padding=20); frame.pack(fill="both",expand=True)
    ttk.Label(frame,text="فروشگاه برنامه‌ها",style="Title.TLabel").pack(anchor="w")
    ttk.Label(frame,text="نصب برنامه‌های منتخب از مخازن سیستم؛ نصب هر برنامه نیازمند تأیید توست.").pack(anchor="w",pady=(5,14))
    search=tk.StringVar(); ttk.Entry(frame,textvariable=search).pack(fill="x",pady=(0,12))
    canvas=tk.Canvas(frame,bg="#101827",highlightthickness=0); scroll=ttk.Scrollbar(frame,orient="vertical",command=canvas.yview); inner=ttk.Frame(canvas)
    inner.bind("<Configure>",lambda e:canvas.configure(scrollregion=canvas.bbox("all"))); canvas.create_window((0,0),window=inner,anchor="nw"); canvas.configure(yscrollcommand=scroll.set)
    canvas.pack(side="left",fill="both",expand=True); scroll.pack(side="right",fill="y")
    def render(*_):
        for w in inner.winfo_children(): w.destroy()
        q=search.get().lower()
        for name,desc,pkg in APPS:
            if q not in (name+" "+desc+" "+pkg).lower(): continue
            row=ttk.Frame(inner,padding=10); row.pack(fill="x",pady=4); left=ttk.Frame(row); left.pack(side="left",fill="x",expand=True)
            ttk.Label(left,text=name,font=("TkDefaultFont",11,"bold")).pack(anchor="w"); ttk.Label(left,text=desc+" · "+pkg).pack(anchor="w")
            status="نصب‌شده" if installed(pkg) else "نصب"
            ttk.Button(row,text=status,state="disabled" if status=="نصب‌شده" else "normal",command=lambda p=pkg:install(p)).pack(side="right")
    search.trace_add("write",render); render()
    ttk.Label(frame,text="برای نصب به اینترنت، مخازن سالم و احراز هویت مدیر نیاز است.",wraplength=600).pack(anchor="w",pady=(10,0))
    root.mainloop()
if __name__=="__main__": main()
