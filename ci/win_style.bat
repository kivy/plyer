@echo off
if "%STYLE%"=="1" (
    %PYTHON% -m pycodestyle "%cd%" ^
        --exclude=pep8.py,utils.py ^
        --ignore=E402,W503 ^
    && echo off > "%cd%\__init__.py" && echo on ^
    && %PYTHON% -m pylint ^
        --disable=C0103,C0111,C0123,C0200,C0325,C0411,C0412,C1801,E0203 ^
        --disable=E0401,E0602,E0611,E0711,E1003,E1101,E1102,R0201,R0205 ^
        --disable=R0205,R0801,R0903,R0912,R0914,R1702,R1705,R1710,R1711 ^
        --disable=R1714,W0101,W0109,W0150,W0201,W0212,W0221,W0223,W0401 ^
        --disable=W0511,W0601,W0603,W0610,W0611,W0612,W0613,W0614,W0622 ^
        --disable=W0702,W0703 "%cd%"
)
