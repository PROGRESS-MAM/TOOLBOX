## Git Submodule

Um das Tool-Repository als Submodule hinzuzufügen, verwende:

```bash
git submodule add https://github.com/PROGRESS-MAM/TOOLBOX.git TOOLBOX
git commit -m "Add TOOLBOX as submodule"
git push
```

Wenn du das Submodule später aktualisieren möchtest:

```bash
git submodule update --remote
```

Um das Submodule initial zu laden, wenn es schon im Repository existiert:

```bash
git submodule update --init --recursive
```