#!/bin/sh
set -eu
# Configure US + Persian layouts and Alt+Shift switching for the current X11 session.
if ! command -v setxkbmap >/dev/null 2>&1; then
    if command -v notify-send >/dev/null 2>&1; then
        notify-send "CodeOS" "ابزار تنظیم کیبورد (setxkbmap) پیدا نشد."
    fi
    exit 1
fi
setxkbmap -layout "us,ir" -option "grp:alt_shift_toggle"
if command -v notify-send >/dev/null 2>&1; then
    notify-send "CodeOS" "کیبورد فارسی و انگلیسی فعال شد؛ با Alt+Shift زبان را عوض کن."
fi
