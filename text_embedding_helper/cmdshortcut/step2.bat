@echo off
cd %~dp0
..\procedure.py step2 ^
--op %1 ^
--xl %~dpn1.xlsx ^
--psd %~dpn1.psd