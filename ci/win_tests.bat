@echo off
if not "%STYLE%"=="1" (
    %PYTHON% -m coverage run ^
        --source %cd%\plyer ^
        -m unittest discover ^
            --start-directory %cd%\plyer\tests ^
            --top-level-directory %cd% ^
            --failfast ^
    && %PYTHON% -m coverage report -m
)
