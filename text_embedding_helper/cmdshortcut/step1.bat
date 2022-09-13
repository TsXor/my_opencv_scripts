@echo off
cd %~dp0
..\procedure.py step1 ^
--op %1 ^
--xl "%~dpn1.xlsx" ^