#!/usr/bin/env python3
"""CodeOS X settings: lightweight XFCE appearance controls."""
import os, subprocess, tkinter as tk
from tkinter import ttk, filedialog, messagebox
ACCENTS = {"آبی CodeOS":"#3978f6","بنفش":"#8b5cf6","فیروزه‌ای":"#14b8a6","نارنجی":"#f97316","صورتی":"#ec4899"}
def run(args):
    try: return subprocess.run(args, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except OSError as e: messagebox.showerror("CodeOS", str(e)); return None
def xfconf(channel, prop, value):
    r=run(["xfconf-query","-c",channel,"-p",prop,"-s",value])
    if r and r.returncode: run(["xfconf-query","-c",channel,"-p",prop,"--create","-t","string","-s",value])
def main():
    root=tk.Tk(); root.title("تنظیمات CodeOS X"); root.geometry("620x500"); root.minsize(500,420); root.configure(bg="#101827")
    style=ttk.Style(); style.theme_use("clam")
    style.configure("TFrame",background="#101827"); style.configure("TLabel",background="#101827",foreground="#edf3ff",font=("TkDefaultFont",11))
    style.configure("TButton",padding=8); style.configure("Title.TLabel",font=("TkDefaultFont",20,"bold"),foreground="#8db2ff"); style.configure("TCombobox",padding=6)
    frame=ttk.Frame(root,padding=24); frame.pack(fill="both",expand=True)
    ttk.Label(frame,text="CodeOS X",style="Title.TLabel").pack(anchor="w")
    ttk.Label(frame,text="ظاهر، رنگ و تصویر زمینه دسکتاپ").pack(anchor="w",pady=(3,20))
    ttk.Label(frame,text="حالت ظاهری").pack(anchor="w")
    theme=tk.StringVar(value="تاریک"); ttk.Combobox(frame,textvariable=theme,values=["تاریک","روشن"],state="readonly").pack(fill="x",pady=(5,15))
    def apply_theme(*_):
        xfconf("xsettings","/Net/ThemeName","Adwaita-dark" if theme.get()=="تاریک" else "Adwaita")
        xfconf("xsettings","/Net/IconThemeName","Papirus")
        messagebox.showinfo("CodeOS","تم دسکتاپ اعمال شد. اگر بخشی تغییر نکرد، یک‌بار از نشست خارج و دوباره وارد شو.")
    ttk.Button(frame,text="اعمال تم",command=apply_theme).pack(anchor="w",pady=(0,18))
    ttk.Label(frame,text="رنگ رابط CodeOS").pack(anchor="w")
    accent=tk.StringVar(value="آبی CodeOS"); ttk.Combobox(frame,textvariable=accent,values=list(ACCENTS),state="readonly").pack(fill="x",pady=(5,8))
    ttk.Label(frame,text="رنگ انتخابی در تنظیمات کاربر ذخیره می‌شود؛ هنوز روی همه اجزای دسکتاپ اعمال نمی‌شود.").pack(anchor="w")
    def save_accent():
        path=os.path.expanduser("~/.config/codeos"); os.makedirs(path,exist_ok=True)
        with open(os.path.join(path,"accent"),"w",encoding="utf-8") as f: f.write(ACCENTS[accent.get()])
        messagebox.showinfo("CodeOS","رنگ ذخیره شد.")
    ttk.Button(frame,text="ذخیره رنگ",command=save_accent).pack(anchor="w",pady=(8,18))
    ttk.Label(frame,text="تصویر زمینه").pack(anchor="w")
    def wallpaper():
        path=filedialog.askopenfilename(title="انتخاب تصویر زمینه",filetypes=[("تصاویر","*.png *.jpg *.jpeg *.webp"),("همه فایل‌ها","*")])
        if not path:return
        r=run(["xfconf-query","-c","xfce4-desktop","-l"]); targets=[p for p in (r.stdout.splitlines() if r else []) if p.endswith("/last-image")]
        if not targets:
            messagebox.showwarning("CodeOS","ویژگی تصویر زمینه در XFCE پیدا نشد. روی دسکتاپ راست‌کلیک کن و Desktop Settings را باز کن."); return
        for prop in targets: xfconf("xfce4-desktop",prop,path)
        messagebox.showinfo("CodeOS","درخواست تغییر تصویر زمینه ارسال شد.")
    ttk.Button(frame,text="انتخاب تصویر…",command=wallpaper).pack(anchor="w",pady=(6,18))
    ttk.Label(frame,text="تغییرات واقعی فقط در نشست XFCE فعلی اعمال می‌شوند.",wraplength=540).pack(anchor="w",pady=(8,0))
    root.mainloop()
if __name__=="__main__": main()
