function Dependencies {
    python -m pip install --requirement devrequirements.txt
    python -m pip install .
    echo Plyer version is
    python -c "import plyer;print(plyer.__version__)"
}

function Tests {
    $current_directory = (pwd).Path

    python -m coverage run `
    --source "$current_directory\plyer" `
    -m unittest discover `
    --start-directory "$current_directory\plyer\tests" `
    --top-level-directory "$current_directory" `
    --failfast

    python -m coverage report -m
}
