# TOOLBOX

Gemeinsame Funktionssammlung für interne Projekte.

## Installation

Einmal pro Maschine Flow-API URL linken:

```bash
pip config set global.extra-index-url https://artifacts.editshare.com/artifactory/api/pypi/editshare-pypi-public/simple
```

Danach die Toolbox installieren:

```bash
pip install "toolbox @ git+https://github.com/PROGRESS-MAM/TOOLBOX.git@main"
```

## Verwendung

```python
from toolbox import tb_link_api, tb_write_log

api = tb_link_api(cred_path, "metadata")
tb_write_log(log_path, "Verbindung steht")
```

Oder alle Funktionen mit einmal:

```python
import toolbox
print(toolbox.__version__)      # gleich TOOLBOX_VERSION
```

## Neues Release

1. In `toolbox/toolbox.py` die Version erhöhen:

   ```python
   TOOLBOX_VERSION = "0.1.6"
   ```

2. Changes committen und pushen.

## Updates in anderen Repos

```bash
pip install --force-reinstall --no-deps "toolbox @ git+https://github.com/PROGRESS-MAM/TOOLBOX.git@main"
```
