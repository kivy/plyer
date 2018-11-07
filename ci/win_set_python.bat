@echo off
:: choose between Python 2 or 3 from matrix
if "%PY%"=="27" (
    set PYTHON=C:\Python27\python.exe
) else (
    set PYTHON=C:\Python36\python.exe
)

:: cd to Plyer folder and set PYTHONPATH
cd C:\projects\app
set PYTHONPATH=%PYTHONPATH%;%cd%
