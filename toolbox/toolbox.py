'''
This is our universal toolbox for code to be reused in our apps.

TOOLBOX RULES:
- never commit without talking to Thao and Martin

- each function name always starts with "tb_"

- functions for internal use only start with "_" and are not exported

- always add a docstring

- increase TOOLBOX VERSION for each commit, it is also the package version

'''

TOOLBOX_VERSION = "0.2.6"


# --------- IMPORTS ---------
import os
import datetime
from dotenv import load_dotenv
from pathlib import Path
from fractions import Fraction
import json
from typing import Any, Literal, overload
import FlowAPI
import ArkAPI

# --------- FUNC MAIN---------
# Die Overloads legen pro api-Wert den konkreten Rueckgabetyp fest.
# Ohne sie sieht der Aufrufer nur Any und bekommt weder
# Autovervollstaendigung noch Docstrings der API-Klassen. Zur Laufzeit
# haben sie keine Wirkung: typing.overload verwirft die Stubs, es gilt
# allein die letzte Definition.
@overload
def tb_link_api(env_path: Path, api: Literal["ark"]) -> ArkAPI.Ark | None: ...


@overload
def tb_link_api(
    env_path: Path, api: Literal["metadata"]
) -> FlowAPI.Metadata | None: ...


@overload
def tb_link_api(env_path: Path, api: Literal["storage"]) -> None: ...


@overload
def tb_link_api(env_path: Path, api: str) -> Any | None: ...


def tb_link_api(env_path: Path, api: str) -> Any | None:
    '''
    Create and return a Flow API gateway instance for the selected API.

    Supported values for api:
        metadata, ark, storage

    Returns None for an unknown api value and for storage, which is not
    implemented yet.
    '''
    load_dotenv(env_path)

    if api == "metadata":
        return FlowAPI.Metadata.create_gateway_instance(
            os.environ.get("FLOW_USER"), os.environ.get("FLOW_PASSWORD"), os.environ.get("FLOW_HOST")
        )
    elif api == "ark":
        return ArkAPI.Ark.create_instance(
            os.environ.get("ARK_USER"), os.environ.get("ARK_PASSWORD"), os.environ.get("ARK_HOST"),
        )

    elif api == "search":
        return FlowAPI.Search.create_gateway_instance(
            os.environ.get("FLOW_USER"), os.environ.get("FLOW_PASSWORD"), os.environ.get("FLOW_HOST")
        )
    return None


def tb_write_log(log_path: Path, message: str) -> None:
    '''
    Create a log_name file if it does not already exist and append a timestamped message.
    '''
    log_path.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"{timestamp}: {message}\n")


def tb_save_clip_metadata_to_json(save_path: Path, clip_metadata: list[dict[str, Any]]) -> None:
    '''
    Save clip metadata to a JSON file in the current working directory.
    '''
    clip_id = clip_metadata[0]["clip_id"]
    file_name = f"clip_metadata_{clip_id}.json"
    file_path = Path(save_path) / file_name
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(clip_metadata, file, ensure_ascii=False, indent=4)


def tb_get_duration_hours_from_tc(tc_start: str, tc_end: str) -> str | None:
    """Return elapsed hours from two timecodes or None for an invalid pair.

    Accept hh:mm:ss:ff/fps and hh:mm:ss:ff:rate_n/rate_d. An optional nd
    suffix is ignored; HH:MM:SS represent clock time, without drop-frame
    or 24-hour rollover correction.
    """
    if not isinstance(tc_start, str) or not isinstance(tc_end, str):
        return None

    def parse_tc(tc_value: str) -> tuple[Fraction, Fraction] | None:
        tokens = tc_value.strip().split()
        if len(tokens) not in (1, 2) or (len(tokens) == 2 and tokens[1].casefold() != "nd"):
            return None
        body, separator, rate_tail = tokens[0].partition("/")
        parts = body.split(":")
        if not separator or len(parts) not in (4, 5) or not all(
            part.isascii() and part.isdecimal() for part in (*parts, rate_tail)
        ):
            return None

        hours, minutes, seconds, frames = map(int, parts[:4])
        numerator = int(parts[4] if len(parts) == 5 else rate_tail)
        denominator = int(rate_tail) if len(parts) == 5 else 1
        if numerator < 1 or denominator < 1 or minutes >= 60 or seconds >= 60:
            return None
        fps = Fraction(numerator, denominator)
        if frames >= round(fps):
            return None
        time_seconds = Fraction(hours * 3600 + minutes * 60 + seconds) + frames / fps
        return time_seconds, fps

    start = parse_tc(tc_start)
    end = parse_tc(tc_end)
    if start is None or end is None or start[1] != end[1] or end[0] < start[0]:
        return None
    return f"{float((end[0] - start[0]) / 3600):.8f}"


def tb_remove_newline(row: dict[str, Any]) -> dict[str, Any]:
    '''
    Replace newline characters in string values with spaces.
    '''
    cleaned = {}
    for k, v in row.items():
        if isinstance(v, str):
            cleaned[k] = v.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
        else:
            cleaned[k] = v
    return cleaned


def tb_make_path(mainfolder: str, subfolder: str, filename: str) -> Path:
    '''
    Create a folder and return a full path using the filename.
    
    Filemname should include file extension.
    '''
    root = Path(mainfolder) / subfolder
    root.mkdir(parents=True, exist_ok=True)
    fullpath = root / filename
    return fullpath




# --------- KEEP THIS LINE AT THE END ---------
# Explizit gepflegt, nicht ueber dir() erzeugt: ein zur Laufzeit
# gebautes __all__ kann ein Type Checker nicht auswerten, und unter
# Python vor 3.12 bleibt es leer, weil Comprehensions dort einen eigenen
# Scope haben und dir() nur deren lokale Namen liefert. Neue tb_-Funktion:
# hier eintragen.
__all__ = [
    "TOOLBOX_VERSION",
    "tb_get_duration_hours_from_tc",
    "tb_link_api",
    "tb_make_path",
    "tb_remove_newline",
    "tb_save_clip_metadata_to_json",
    "tb_write_log",
]
