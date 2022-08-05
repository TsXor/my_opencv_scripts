@echo off
cd %~dp0
"E:\Adobe\Adobe Photoshop CS6 (64 Bit)\Photoshop.exe" %1
extract_text_img.py %1 | detect_text_sizepos.py | gsudo psoperate.py
