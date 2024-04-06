if [ "$(basename "$(pwd)")" = ".github" ]; then
    cd ..
fi

xargs mypy --strict --follow-imports=silent --no-warn-unused-ignore --install-types --non-interactive typings < .github/mypy_files.txt
