@echo off
if not "%STYLE%"=="1" (
    %PYTHON% -m nose.core ^
        --stop ^
        --nocapture ^
        --with-coverage ^
        --cover-package=plyer ^
        %cd%\plyer\tests
)
