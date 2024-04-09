if [ "$(basename "$(pwd)")" = ".github" ]; then
    cd ..
fi

xargs pyright -p .github/pyright-config.json
