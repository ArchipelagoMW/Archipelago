if [ "$(basename "$(pwd)")" = ".github" ]; then
    cd ..
fi

pyright -p .github/pyright-config.json
