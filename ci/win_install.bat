@echo off
%PYTHON% -m pip install --requirement devrequirements.txt
%PYTHON% -m pip install .
echo Plyer version is
%PYTHON% -c "import plyer;print(plyer.__version__)"
