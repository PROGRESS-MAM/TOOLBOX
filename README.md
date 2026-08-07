# TOOLBOX

Gemeinsame Funktionssammlung für interne Projekte.

## Vorbereitung für Nutzung in anderen Repos

1. In `pyproject.toml` Release-Version erhöhen:

   ```toml
   [project]
   version = "x.x.x"
   ```

2. Changes committen und pushen
 

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
python -m pip install --upgrade -r requirements.txt
```
