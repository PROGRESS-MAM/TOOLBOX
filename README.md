# TOOLBOX

Gemeinsame Funktionssammlung für interne Projekte.

## Vorbereitung für Nutzung in anderen Repos

1. In `pyproject.toml` Release-Version anpassen:

   ```toml
   [project]
   version = "x.x.x"
   ```

2. Changes committen und pushen:

   ```bash
   git add -A
   git commit -m "Toolbox als Paket aufsetzen"
   git push
   ```

3. Auf GitHub ein Release mit Tag erstellen - gleiche Version wie in yaml.  

## Nutzung in anderen Repos

1. In deinem Projekt eine `requirements.txt` anlegen:

   ```text
   toolbox @ git+https://github.com/PROGRESS-MAM/TOOLBOX.git@main
   ```

2. Toolbox installieren:

   ```bash
   pip install -r requirements.txt
   ```

3. In deinem Python-Code importieren:

   ```python
   from toolbox import ...
   ```

## Updates in anderen Repos

Bei einem neuen Release die Version in `requirements.txt` anpassen und erneut installieren:

```bash
pip install -r requirements.txt --upgrade
```
