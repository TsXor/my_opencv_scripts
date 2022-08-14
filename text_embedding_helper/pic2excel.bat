@echo off && cd %~dp0 && chcp 65001 && cls
echo 别急
extract_text_img.py --input=%1 --output=PIPE | detect_text_sizepos.py --input=PIPE --output=%~dp1%~n1.xlsx
